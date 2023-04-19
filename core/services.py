import boto3
import os
from botocore.exceptions import ClientError
import logging
from functools import lru_cache

from innotter.settings import (
    AWS_DEFAULT_REGION,
    HOSTNAME_EXTERNAL,
    PORT_EXTERNAL,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_KEY,
    EMAIL_HOST_USER,
    SUBJECT,
    EXPIRATION_TIME,
    BUCKET_NAME,
)
from page.models import Page
from user.models import User


class AWSManager:
    @staticmethod
    @lru_cache
    def get_credentials() -> dict:
        credentials = {
            "endpoint_url": f"http://{HOSTNAME_EXTERNAL}:" f"{PORT_EXTERNAL}",
            "region_name": AWS_DEFAULT_REGION,
            "aws_access_key_id": AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": AWS_SECRET_KEY,
        }

        return credentials

    @staticmethod
    @lru_cache
    def get_client(client_name: str):
        credentials = AWSManager.get_credentials()
        client = boto3.client(
            client_name,
            endpoint_url=credentials["endpoint_url"],
            region_name=credentials["region_name"],
            aws_access_key_id=credentials["aws_access_key_id"],
            aws_secret_access_key=credentials["aws_secret_access_key"],
        )

        if client_name == "ses":
            client.verify_email_identity(EmailAddress=EMAIL_HOST_USER)

        return client

    @staticmethod
    @lru_cache
    def get_resource(resource_name: str):
        credentials = AWSManager.get_credentials()
        resource = boto3.resource(
            resource_name,
            endpoint_url=credentials["endpoint_url"],
            region_name=credentials["region_name"],
            aws_access_key_id=credentials["aws_access_key_id"],
            aws_secret_access_key=credentials["aws_secret_access_key"],
        )

        return resource


class S3Manager:
    @staticmethod
    @lru_cache
    def get_bucket(bucket_name: str):
        s3_client = AWSManager.get_client("s3")

        try:
            bucket = s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    "LocationConstraint": AWS_DEFAULT_REGION
                },
            )

        except s3_client.exceptions.BucketAlreadyOwnedByYou:
            s3_resource = AWSManager.get_resource("s3")
            bucket = s3_resource.Bucket(name=BUCKET_NAME)

        return bucket

    @staticmethod
    def create_presigned_url(
            key: str, expiration: int = int(EXPIRATION_TIME), bucket: str = BUCKET_NAME
    ) -> str:
        s3_client = AWSManager.get_client("s3")

        try:
            response = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=expiration,
            )

        except ClientError as e:
            logging.error(e)
            return None

        return Exception

    @staticmethod
    def upload_file(file_path: str, key: str) -> str:
        bucket = AWSManager.get_bucket(BUCKET_NAME)

        with open(file_path, "rb") as data:
            bucket.put_object(Key=key, Body=data)

        return key


class SESManager:
    @staticmethod
    def send_mail(data: list) -> dict:
        emails_list = list(
            Page.objects.values_list("followers__email", flat=True)
            .distinct()
            .filter(id=data["page"])
        )
        owner = User.objects.get(id=data["owner"])
        msg = f"User {owner.username} created a new post: {data['content']}"
        ses_client = AWSManager.get_client("ses")

        response = ses_client.send_email(
            Source=EMAIL_HOST_USER,
            Destination={"ToAddresses": emails_list},
            Message={
                "Subject": {
                    "Data": SUBJECT,
                },
                "Body": {
                    "Text": {
                        "Data": msg,
                    },
                    "Html": {
                        "Data": f"<h1>{msg}</h1>",
                    },
                },
            },
        )

        return response

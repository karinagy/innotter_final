import boto3
import os
from botocore.exceptions import ClientError
import logging
from functools import lru_cache

from page.models import Page
from user.models import User


class AWSManager:
    @staticmethod
    @lru_cache
    def get_credentials() -> dict:
        credentials = {
            'endpoint_url': f"http://{os.getenv('HOSTNAME_EXTERNAL')}:"
                            f"{os.getenv('PORT_EXTERNAL')}",
            'region_name': os.getenv('AWS_DEFAULT_REGION'),
            'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.getenv('AWS_SECRET_KEY')
        }

        return credentials

    @staticmethod
    @lru_cache
    def get_client(client_name: str):
        credentials = AWSManager.get_credentials()
        client = boto3.client(
            client_name,
            endpoint_url=credentials['endpoint_url'],
            region_name=credentials['region_name'],
            aws_access_key_id=credentials['aws_access_key_id'],
            aws_secret_access_key=credentials['aws_secret_access_key']
        )

        if client_name == 'ses':
            client.verify_email_identity(EmailAddress=os.getenv('EMAIL_HOST_USER'))

        return client

    @staticmethod
    @lru_cache
    def get_resource(resource_name: str):
        credentials = AWSManager.get_credentials()
        resource = boto3.resource(
            resource_name,
            endpoint_url=credentials['endpoint_url'],
            region_name=credentials['region_name'],
            aws_access_key_id=credentials['aws_access_key_id'],
            aws_secret_access_key=credentials['aws_secret_access_key']
        )

        return resource

    @staticmethod
    @lru_cache
    def get_bucket(bucket_name: str):
        s3_client = AWSManager.get_client('s3')

        try:
            bucket = s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': os.getenv('AWS_DEFAULT_REGION')
                }
            )

        except s3_client.exceptions.BucketAlreadyOwnedByYou:
            s3_resource = AWSManager.get_resource('s3')
            bucket = s3_resource.Bucket(name=os.getenv('BUCKET_NAME'))

        return bucket

    @staticmethod
    def create_presigned_url(key: str, expiration: int = int(os.getenv('EXPIRATION_TIME')),
                             bucket: str = os.getenv('BUCKET_NAME')) -> str :
        s3_client = AWSManager.get_client('s3')

        try:
            response = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket,
                        'Key': key},
                ExpiresIn=expiration
            )

        except ClientError as e:
            logging.error(e)
            return None

        return response.replace('http://localstack', 'http://0.0.0.0')

    @staticmethod
    def upload_file(file_path: str, key: str) -> str:
        bucket = AWSManager.get_bucket(os.getenv('BUCKET_NAME'))

        with open(file_path, 'rb') as data:
            bucket.put_object(Key=key, Body=data)

        return key

    @staticmethod
    def send_mail(data: list) -> dict:
        emails_list = list(Page.objects.values_list('followers__email', flat=True).distinct().filter(id=data['page']))
        owner = User.objects.get(id=data['owner'])
        msg = f"User {owner.username} created a new post: {data['content']}"
        ses_client = AWSManager.get_client('ses')

        response = ses_client.send_email(
            Source=os.getenv('EMAIL_HOST_USER'),
            Destination={
                'ToAddresses': emails_list
            },
            Message={
                'Subject': {
                    'Data': os.getenv('SUBJECT'),
                },
                'Body': {
                    'Text': {
                        'Data': msg,
                    },
                    'Html': {
                        'Data': '<h1>' + msg + '</h1>',
                    }
                }
            }
        )

        return response

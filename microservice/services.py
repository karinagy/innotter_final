
import boto3
import os
from functools import lru_cache

from innotter.settings import HOSTNAME_EXTERNAL, PORT_EXTERNAL, AWS_DEFAULT_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_KEY, \
    AWS_DYNAMODB_TABLE_NAME


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
            endpoint_url=credentials['endpoint_url'],
            region_name=credentials['region_name'],
            aws_access_key_id=credentials['aws_access_key_id'],
            aws_secret_access_key=credentials['aws_secret_access_key']
        )

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
    def get_table():
        dynamodb_client = AWSManager.get_client('dynamodb')
        dynamodb_resource = AWSManager.get_resource('dynamodb')

        try:
            table = dynamodb_client.create_table(
                AttributeDefinitions=[
                    {
                        'AttributeName': 'Page',
                        'AttributeType': 'S'
                    },
                ],
                TableName=os.getenv('AWS_DYNAMODB_TABLE_NAME'),
                KeySchema=[
                    {
                        'AttributeName': 'Page',
                        'KeyType': 'HASH'
                    },
                ],

                BillingMode='PAY_PER_REQUEST',
            )

        except dynamodb_client.exceptions.ResourceInUseException:

            table = dynamodb_resource.Table(AWS_DYNAMODB_TABLE_NAME)

        return table

    @staticmethod
    def get_item():
        table = AWSManager.get_table()
        response = table.get_item(
            Key={'AttributeName': {'S': 'Page'}}
        )

        return response

    @staticmethod
    def put_item(page: str):
        table = AWSManager.get_table()
        response = table.put_item(
            Item={
                'Page': page
            }
        )

        return response

    @staticmethod
    def delete_item(page: str):
        table = AWSManager.get_table()
        response = table.delete_item(
            Item={
                'Page': page
            }
        )

        return response

    @staticmethod
    def update_item(page: str):
        table = AWSManager.get_table()
        response = table.update_item(
            Item={
                'Page': page
            }
        )

        return response


class StatisticsService:
    @staticmethod
    def get_statistics():
        return AWSManager.get_item()
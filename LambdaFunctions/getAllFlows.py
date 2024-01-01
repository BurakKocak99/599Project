import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamo = boto3.resource("dynamodb")
table = dynamo.Table("FlowStatus")


def lambda_handler(event, context):
    # TODO implement

    try:

        response = table.scan()
        return {'statusCode': 200,
                'body': json.dumps(response)
                }

    except:
        return {'statusCode': 500,
                'body': "Error while fetching items!"
                }

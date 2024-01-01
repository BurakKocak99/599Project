import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamo = boto3.resource("dynamodb")
table = dynamo.Table("ServiceDetails")


def lambda_handler(event, context):
    # TODO implement

    try:
        print()
        print(event.__class__)
        response = table.scan(FilterExpression=Attr(list(event.keys())[0]).eq(list(event.values())[0]))
        return {'statusCode': 200,
                'body': json.dumps(response)
                }

    except Exception as e:
        print(e)
        return {'statusCode': 500,
                'body': json.dumps(e.__dict__)
                }


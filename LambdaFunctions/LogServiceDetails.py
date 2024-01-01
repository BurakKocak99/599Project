import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamo = boto3.resource("dynamodb")
ServiceDetails_table = dynamo.Table("ServiceDetails")
FlowStatus_table = dynamo.Table("FlowStatus")


def lambda_handler(event, context):
    # TODO implement

    try:
        FlowStatus_reponse = FlowStatus_table.scan(FilterExpression=Attr("ProcessName").eq(event["ProcessName"]))

        if (FlowStatus_reponse["Count"] == 0):  # If new flow is being registered
            FlowStatus_table.put_item(
                Item={"ProcessName": event["ProcessName"], "UpdateStatus": "New", "LastUpdated": event["TimeStamp"]})

        elif (FlowStatus_reponse["Items"][0]["UpdateStatus"] == "New" and event["EOF"] == "True"):
            FlowStatus_table.update_item(Key={'ProcessName': event["ProcessName"]},
                                         UpdateExpression='SET UpdateStatus = :status1',
                                         ExpressionAttributeValues={':status1': "Updated"})

        elif (FlowStatus_reponse["Items"][0]["UpdateStatus"] == "Updated"):  # Discard
            return FlowStatus_reponse


    except  Exception as e:
        print("Error Occured on flow status process", e)
        return {'statusCode': 500,
                'body': json.dumps('Error Occured on flow status process')
                }

    try:
        response = ServiceDetails_table.put_item(Item=event)
        return response

    except Exception as e:
        return {'statusCode': 500,
                'body': json.dumps('Error Occured on Service Details process')
                }


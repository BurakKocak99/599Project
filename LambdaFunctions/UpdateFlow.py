import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamo = boto3.resource("dynamodb")
ServiceDetails_table = dynamo.Table("ServiceDetails")
FlowStatus_table = dynamo.Table("FlowStatus")


def lambda_handler(event, context):
    # TODO implement
    try:  # Get the related items.
        scan_ServiceDetailsResponse = ServiceDetails_table.scan(
            FilterExpression=Attr(list(event.keys())[0]).eq(list(event.values())[0]))
        scan_FlowStatusResponse = FlowStatus_table.scan(
            FilterExpression=Attr(list(event.keys())[0]).eq(list(event.values())[0]))
        print(scan_ServiceDetailsResponse)
        print(scan_FlowStatusResponse)

    except  Exception as e:
        print("Error while scanning the DB!", e)

    if scan_ServiceDetailsResponse["Count"] == 0 and scan_FlowStatusResponse["Count"] == 0:
        return {'statusCode': 200,
                'body': json.dumps("No items were deleted!")}

    for items in scan_ServiceDetailsResponse["Items"]:
        try:
            delete_response_ServiceDetails = ServiceDetails_table.delete_item(
                Key={"ProcessName": items["ProcessName"], "TimeStamp": items["TimeStamp"]})
            print(delete_response_ServiceDetails)
        except Exception as e:
            print("Erroor while deleting!", e, "The item is", items)

            return {'statusCode': 500,
                    'body': json.dumps('Error while deleting item:', items)
                    }

    try:
        print()
        delete_response_FlowStatus = FlowStatus_table.delete_item(
            Key={"ProcessName": scan_FlowStatusResponse["Items"][0]["ProcessName"]})
    except  Exception as e:
        print("Erroor while deleting flow status!", e, "The item is", scan_FlowStatusResponse)
        return {'statusCode': 500,
                'body': json.dumps('Error while deleting flow status!', scan_FlowStatusResponse)
                }
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully deleted!')
    }

import streamlit

import ApiConnection as api
from datetime import datetime
import json

'''
This function returns a string. The output of the api request contains list of items and meta data or the response. By 
query, users can get any data from the response using HeaderType (can be "Items" or "Count" or anything else)
'''


@streamlit.cache_data(ttl=600)
def get_item(Key, Value):
    response = api.get_item(key=Key, value=Value)

    responseBody = json.loads(response.json()['body'])
    responseStatus = response.json()['statusCode']

    if responseStatus == 200 and responseBody['Count'] > 0:
        return responseBody["Items"]
    else:
        raise ValueError("Please enter a valid Key name!")


def get_count(Key, Value):
    response = api.get_item(key=Key, value=Value)
    responseBody = json.loads(response.json()['body'])
    responseStatus = response.json()['statusCode']
    if responseStatus == 200:
        return responseBody["Count"]
    else:
        raise ValueError("Please enter a valid Key name!")


@streamlit.cache_data(ttl=600)
def get_process_count_by_category():
    Operations = {"FERRY": 0, "WMS": 0, "LOGISTICS": 0}
    OperationTypeResponse = api.get_item(key="EOF", value="True")
    OperationTypes = json.loads(OperationTypeResponse.json()['body'])["Items"]
    for type in OperationTypes:
        Operations[type["OperationalCategory"]] = Operations[type["OperationalCategory"]] + 1

    return Operations


@streamlit.cache_data(ttl=600)
def get_all_service_count():
    response = api.get_allItems()
    responseBody = json.loads(response.json()['body'])
    responseStatus = response.json()['statusCode']
    if responseStatus == 200 and responseBody['Count'] > 0:
        return responseBody['Count']
    else:
        raise ValueError("Please enter a valid Key name!")


@streamlit.cache_data(ttl=600)
def get_process_count():
    response = api.get_AllFlows()
    responseBody = json.loads(response.json()['body'])
    responseStatus = response.json()['statusCode']
    if responseStatus == 200 and responseBody['Count'] > 0:
        return responseBody['Count']
    else:
        raise ValueError("Please enter a valid Key name!")


@streamlit.cache_data(ttl=600)
def ServiceAdditionByLastMonth():
    response = api.get_allItems()
    responseBody = json.loads(response.json()['body'])
    responseStatus = response.json()['statusCode']
    if responseStatus == 200:

        ProcessAddedCount = 0
        currentDate = datetime.fromisoformat(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        for items in responseBody["Items"]:
            time_difference = currentDate - datetime.fromisoformat(items["TimeStamp"][:16])

            if time_difference.days < 30:
                ProcessAddedCount = ProcessAddedCount + 1

    return ProcessAddedCount


@streamlit.cache_data(ttl=600)
def FlowAdditionByLastMonth():
    response = api.get_AllFlows()
    responseBody = json.loads(response.json()['body'])
    responseStatus = response.json()['statusCode']
    if responseStatus == 200:
        FlowAddedCount = 0
        currentDate = datetime.fromisoformat(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        for items in responseBody["Items"]:

            time_difference = currentDate - datetime.fromisoformat(items["LastUpdated"][:16])
            if time_difference.days < 30:
                FlowAddedCount = FlowAddedCount + 1

    return FlowAddedCount


@streamlit.cache_data(ttl=600)
def getAllProtocolCount():
    protocol = {"HTTP": 0, "FTP": 0, "AS2": 0}

    response = api.get_allItems()
    responseBody = json.loads(response.json()['body'])
    responseStatus = response.json()['statusCode']

    if responseStatus == 200:
        for items in responseBody["Items"]:

            if "Protocol" in items:
                protocol[items["Protocol"]] = protocol[items["Protocol"]] + 1

    return protocol


@streamlit.cache_data(ttl=600)
def getLineChartData():
    flow_response = api.get_AllFlows()

    flow_response_body = json.loads(flow_response.json()['body'])
    flow_response_Status = flow_response.json()['statusCode']

    if flow_response_Status == 200:
        lineData = []
        tempDic = {}
        date_val = lambda dateTime: dateTime[:10]
        increment = lambda arr, serv_count: [arr[0], arr[1] + 1, arr[2] + serv_count]
        for item in flow_response_body["Items"]:
            Date = date_val(item["LastUpdated"])
            serviceCount = get_count("ProcessName", item["ProcessName"])
            if Date in tempDic:
                tempDic[Date] = increment(tempDic[Date], serviceCount)
            else:
                tempDic[Date] = [Date, 1, serviceCount]

        for values in tempDic.values():
            lineData.append(values)
        return lineData


@streamlit.cache_data(ttl=600)
def getFlows():
    response = api.get_AllFlows()

    response_body = json.loads(response.json()['body'])
    response_Status = response.json()['statusCode']

    if response_Status == 200:
        processList = []
        for item in response_body["Items"]:
            processList.append(item["ProcessName"])

    return processList


def generateMermaid_string(ProcessName):
    items = get_item("ProcessName", ProcessName)

    mermaid_string = """
    \n\n
    graph LR\n"""
    for index in range(len(items)):

        if index != len(items) - 1:
            mermaid_string = mermaid_string + items[index]["ServiceName"] + """ --> """
        else:
            mermaid_string = mermaid_string + items[index]["ServiceName"]

    return mermaid_string


def update_flow(Key, Value):
    response = api.update(key=Key, value=Value)

    response_body = json.loads(response.json()['body'])
    response_Status = response.json()['statusCode']

    if response_Status == 200:
        return "Successfully Deleted!"
    else:
        return "Something went wrong while deleting!"




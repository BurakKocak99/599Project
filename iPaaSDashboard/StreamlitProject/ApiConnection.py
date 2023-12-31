import requests
import json
import streamlit

URL = "https://ghjy6mdoxl.execute-api.us-east-1.amazonaws.com/LogService/Log"



GET_ITEM_URL = URL + "/getItem"
POST_ITEM_URL = URL + "/POST"
GET_ALL_URL = URL + "/getAllServices"
UPDATE_URL = URL + "/UpdateFlow"

GET_ALL_FLOWS = URL + "/getAllFlowStatus"

@streamlit.cache_data(ttl= 600)
def get_item(key, value):
    payload = {key: value}
    return requests.get(url=GET_ITEM_URL, data=json.dumps(payload))


def post_item(service_details):
    return requests.post(url=POST_ITEM_URL, data=json.dumps(service_details))

@streamlit.cache_data(ttl= 600)
def get_allItems():

    return requests.get(url=GET_ALL_URL)


def update(key, value):
    payload = {key: value}

    return requests.post(url=UPDATE_URL, data=json.dumps(payload))

@streamlit.cache_data(ttl= 600)
def get_AllFlows():
    return requests.get(url=GET_ALL_FLOWS)
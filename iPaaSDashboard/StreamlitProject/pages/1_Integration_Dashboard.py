import streamlit as st
import Utils as utils
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", menu_items={
    'Get Help': 'https://www.extremelycoolapp.com/help',
    'Report a bug': "https://www.extremelycoolapp.com/bug",
    'About': "# This is a header. This is an *extremely* cool app!"
})

st.title("Integration Dashboard")

col1_1, col2_1, col3_1 = st.columns(3, gap="small")

col1_2, col2_2 = st.columns(2, gap="large")
getServiceCount = lambda Key, value: utils.get_count(Key, value)

col1_3, col2_3 = st.columns(2, gap="small")

with st.spinner("Please wait while the metrics being fetched!"):
    col1_1.container(border=True).metric(label="Total number of services", value=utils.get_all_service_count(),
                                         delta=utils.ServiceAdditionByLastMonth(),
                                         help= "This metric shows the number of services in use. The delta value represents "
                                               +"the number of services added within this month")
    col2_1.container(border=True).metric(label="Total number of processes", value=utils.get_process_count(),delta = utils.FlowAdditionByLastMonth(),
                                         help="This metric shows the number of Processes in use. The delta value represents "
                                              + "the number of processes added within this month"
                                         )
    col3_1.container(border=True).metric(label="Average Number of of services for each process",
                                         value= format(utils.get_all_service_count() / utils.get_process_count(),'.1f'))


with st.spinner("Please wait while the charts being prepared!"):
    col1_2.subheader("Number of services by operational category ")
    col1_2.bar_chart(
        data={"FERRY": getServiceCount("OperationalCategory", "FERRY"),
              "WMS": getServiceCount("OperationalCategory", "WMS"),
              "LOGISTICS": getServiceCount("OperationalCategory", "LOGISTICS")},
        color=["#c0d651"])

    col2_2.subheader("Number of process by operational category ")
    col2_2.bar_chart(
        data=utils.get_process_count_by_category())

with st.spinner("Please wait while the charts being prepared!"):
    col1_3.subheader("Number of services by Server ")
    col1_3.bar_chart(
        data={"BE": getServiceCount("Server", "BE"), "FE": getServiceCount("Server", "FE")},
        color=["#bd3728"])
    col2_3.subheader("Number of services by Network Protocol")
    col2_3.bar_chart(
        data=utils.getAllProtocolCount(),
        color=["#bd3728"])


with st.spinner("Please wait while the Line Chart being prepared!"):
    st.subheader("Addition of Process/Service over time.")
    df = pd.DataFrame(utils.getLineChartData(), columns=["Dates","ServiceCount","ProcessCount"])


    st.line_chart(df, x="Dates", y=["ServiceCount","ProcessCount"],color=["#d1bc00", "#d91640"])

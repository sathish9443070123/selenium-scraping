import streamlit as pt
from time import sleep
import pandas as pd
import mysql.connector
from mysql import connector
import warnings
import datetime

x = datetime.datetime.now()

warnings.filterwarnings('ignore')



#C:\Users\91944\AppData\Local\Programs\Python\Python310\smartapi-python-main\test

mydbconn = connector.connect( host=" 127.0.0.1", user="root", password="", database="redbus"   )

bus_onwers = ("All", "Govt", "private")
option = pt.selectbox(
    "Select Bus owner type",
    bus_onwers,
)

query =  "SELECT DISTINCT route_name FROM bus_details"
df1 = pd.read_sql(query, con = mydbconn)

option2 = pt.selectbox(
    "Select route",
    df1,
)


condi = ""
if (option != "All"):
    condi = " WHERE route_name = '"+option+"'"

query = "SELECT busname,bustype,departing_time,departing_loc,duration,reaching_time,reaching_loc,seats_available,price,star_rating,trip_id, bus_owner,states,route_name,route_link FROM bus_details" + condi


df = pd.read_sql(query, con = mydbconn)


pt.dataframe(df)




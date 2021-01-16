#!/usr/bin/python3

import sys
import pyTigerGraphBeta as tg


conn = tg.TigerGraphConnection(host="https://<>.i.tgcloud.io",username="",password="",version="3.0.5")

# print(conn.getVer())
# https://iot.i.tgcloud.io/



def schema():
    #  Apply the     
    res = conn.gsql("""
CREATE VERTEX Device (PRIMARY_ID device_id UINT, name STRING, location UINT, tag STRING, serial STRING)
CREATE VERTEX Broker (PRIMARY_ID broker_id UINT, broker_name STRING)
    WITH STATS="outdegree_by_edgetype"
CREATE VERTEX Owner  (PRIMARY_ID city_code UINT, City_Name STRING, Country UINT)
    WITH STATS="none"
CREATE VERTEX Devices_Metrics (PRIMARY_ID dm_id STRING, dm_name STRING, dm_value FLOAT, dm_date DATETIME)
CREATE UNDIRECTED EDGE device_broker (FROM Device, TO Broker)
CREATE UNDIRECTED EDGE owner_devices (FROM Owner, TO Device)
CREATE UNDIRECTED EDGE device_metric (FROM Device, TO Devices_Metrics)
CREATE UNDIRECTED EDGE Connect_through (FROM Device, TO Device, on_cs UINT)
CREATE GRAPH ioT_Graph (*)
""")

def drop():
    res = conn.gsql("drop all")

def data_loader():
    # Loading Job , Loading data 
    pass

def GSQL_Queries():
    # GSQL Queries
    pass



if sys.argv[1] == '1':
    print("Dropping ...")
    drop()    
elif sys.argv[1] == '2':
    print("Inserting ...")
    schema()
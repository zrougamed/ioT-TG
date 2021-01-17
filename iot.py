#!/usr/bin/python3

import sys
from typing import Optional, Any

import pyTigerGraphBeta as tg


conn = tg.TigerGraphConnection(host="http://172.22.0.2",useCert=False,username="tigergraph",password="tigergraph",version="3.0.5",gsPort=14240)
# conn = tg.TigerGraphConnection(host="https://iot.i.tgcloud.io",username="tigergraph",password="tigergraph",version="3.0.5")
# print(conn.getVer())
# https://iot.i.tgcloud.io/
# https://iot.i.tgcloud.io/api/info/schema/style/ioT_Graph


def schema():
    #  Apply the
    res = conn.gsql("""
CREATE GRAPH ioT ()    
CREATE SCHEMA_CHANGE JOB change_schema_of_ioT  FOR GRAPH ioT {
ADD VERTEX Location (PRIMARY_ID Points STRING, Latitude FLOAT, Longitude FLOAT) WITH primary_id_as_attribute="TRUE"; 
ADD VERTEX Measurement (PRIMARY_ID meas_id STRING, dm_name STRING, dm_value FLOAT, dm_date STRING, dm_unit STRING, dm_abv_unit STRING)  WITH primary_id_as_attribute="TRUE"; 
ADD VERTEX Device (PRIMARY_ID device_id STRING, location_id STRING, topic STRING)  WITH primary_id_as_attribute="TRUE"; 
ADD VERTEX Topic (PRIMARY_ID  topic_name STRING, topic_description STRING, topic_type STRING)  WITH primary_id_as_attribute="TRUE";

ADD UNDIRECTED EDGE device_topic (FROM Device, TO Topic);
ADD UNDIRECTED EDGE measurement_topic (FROM Measurement, TO Topic);
ADD UNDIRECTED EDGE device_location (FROM Device, TO Location);
ADD UNDIRECTED EDGE device_measurement (FROM Device, TO Measurement);
    
}
RUN SCHEMA_CHANGE JOB change_schema_of_ioT
DROP JOB change_schema_of_ioT
""")
    for e in res:
        print(e)


def drop():
    res = conn.gsql("drop all")
    for e in res:
        print(e)


def data_loader():
    # Loading Job , Loading data
    res = conn.gsql("""
USE GRAPH ioT
BEGIN
CREATE LOADING JOB load_iot_data FOR GRAPH social {
   DEFINE FILENAME file1="/home/tigergraph/data.csv";

   LOAD file1 TO VERTEX Device VALUES ($"col1", $"col1", $"col2", $"col3", $"col4") USING header="true", separator=",";
   LOAD file2 TO EDGE device_measurement VALUES ($0, $1, $2) USING header="true", separator=",";
}
END
""")
    for e in res:
        print(e)


def data_runner():
    res = conn.gsql("""
RUN LOADING JOB load_iot_data
""")
    for e in res:
        print(e)


def gsql_install():
    # GSQL Queries
    res = conn.gsql("""
USE GRAPH ioT
CREATE QUERY DeviceByLocation(VERTEX<Location> d) {
  Start = {d};
  Result = SELECT tgt
           FROM Start:s-(device_location:e) ->Device:tgt;
  PRINT Result;
}
INSTALL QUERY  DeviceByLocation
""")
    for e in res:
        print(e)


if sys.argv[1] == 'drop':
    print("Dropping ...")
    drop()
elif sys.argv[1] == 'ddl':
    print("DDL ...")
    schema()
elif sys.argv[1] == 'load':
    print('Loading Data ...')
    data_loader()
    print("Running Loading Job ...")
    data_runner()
elif sys.argv[1] == 'query':
    print('Inserting GSQL Queries ...')
    gsql_install()














# coding: utf-8
"""
k_show_streets @is_json=:is_json1
"""
import pyodbc
import json
import my_sql_func
import socket
import os
import logging.config
import logging_yaml

logging_yaml.setup_logging()
#logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__) 
logger.info("unloading of the streets")

connect_file = 'config.ini'
section = 'my_connect' if socket.gethostname().lower() == 'adm' else 'mfc_connect'  # my_connect  mfc_connect

try:
    conn = my_sql_func.create_connection(connect_file, section)
except:
    logger.exception("exception message")
    raise

cursor = conn.cursor()

cursor.execute("exec k_show_streets ")
rows  = cursor.fetchall()
cols = [i[0] for i in cursor.description]

data = {"dataStreets": []}
for item in rows:
    data["dataStreets"].append(dict(zip(cols, item)))

cursor.close()
conn.close()

logger.info("streets have been unloaded")
# =====================================================
print ("Content-type: application/json; charset=utf-8 \r")
print ("\r")
print(json.dumps(data, ensure_ascii=False)) 
#print(json.dumps(data, indent=4, ensure_ascii=False)) 
# =====================================================


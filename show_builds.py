#! c:\python3\python.exe 
# coding: utf-8

"""
k_show_build @street_name1=:street_name1

{"dataBuilds":[ 
{"nom_dom":6,"nom_dom_sort":6},
{"nom_dom":8,"nom_dom_sort":8}]
}

"""
import os
import json
import my_sql_func
import sys
import cgi
import html
import socket
import logging.config
import logging_yaml

logging_yaml.setup_logging()
# logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

street_name_in = ""  # "10 лет Октября ул."
form = cgi.FieldStorage()
street_name_in = form.getvalue("street_name", street_name_in)
street_name = html.escape(street_name_in)

if street_name == "":
    print("Content-type: text/html \n")
    msg_err = "street_name not set " + street_name
    print(msg_err)
    logger.error(msg_err)
    sys.exit(msg_err)

logger.info(f"start {os.path.basename(__file__)} street_name={street_name}")

connect_file = 'config.ini'
section = 'my_connect' if socket.gethostname().lower() == 'adm' else 'mfc_connect'  # my_connect  mfc_connect
try:
    conn = my_sql_func.create_connection(connect_file, section)
except Exception as ex:
    logger.exception("exception message", ex)
    raise
cursor = conn.cursor()

# street_name = '1-я Донская ул.'
params = street_name
try:
    cursor.execute("exec k_show_build @street_name1=?", params)
except Exception as ex:
    logger.exception("exception message", ex)
    raise
rows = cursor.fetchall()
cols = [i[0] for i in cursor.description]

data = {"street_name": street_name, "dataBuilds": []}
for item in rows:
    data["dataBuilds"].append(dict(zip(cols, item)))

cursor.close()
conn.close()
# =====================================================
print("Content-type: application/json; charset=utf-8 \n")
print(json.dumps(data, indent=4, ensure_ascii=False))
# =====================================================

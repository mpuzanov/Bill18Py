#! c:\python3\python.exe 
# coding: utf-8
"""
k_show_kvr @street_name1=:street_name1,@nom_dom1=:nom_dom1
"""
import os, sys
import pyodbc
import json
import my_sql_func
import cgi
import html
import socket
import logging.config
import logging_yaml

logging_yaml.setup_logging()
#logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

street_name_in = ""  # "10 лет Октября ул."
nom_dom_in = ""  # "12"

form = cgi.FieldStorage()
street_name = form.getfirst("street_name", street_name_in)
street_name = html.escape(street_name)
nom_dom = form.getfirst("nom_dom", nom_dom_in)
nom_dom = html.escape(nom_dom)
logger.info(f"start {os.path.basename(__file__)} street_name={street_name}, nom_dom={nom_dom}")
if street_name == "" or  nom_dom=="":
	print("Content-type: text/html \n")
	msg_err="street_name or nom_dom not set"
	print(msg_err)
	logger.error(msg_err)
	sys.exit(msg_err) 

connect_file = 'config.ini'
section = 'my_connect' if socket.gethostname().lower() == 'adm' else 'mfc_connect'  # my_connect  mfc_connect
try:
    conn = my_sql_func.create_connection(connect_file, section)
except:
    logger.exception("exception message")
    raise

cursor = conn.cursor()

params = (street_name, nom_dom)
try:
    cursor.execute("k_show_kvr @street_name1=?,@nom_dom1=?", params)
except:
    logger.exception("exception message")
    raise    
rows = cursor.fetchall()
cols = [i[0] for i in cursor.description]

data = {"street_name": street_name, "nom_dom": nom_dom, "dataKvr": []}
for item in rows:
    data["dataKvr"].append(dict(zip(cols, item)))

cursor.close()
conn.close()    
# =====================================================
print ("Content-type: application/json; charset=utf-8 \n")
print(json.dumps(data, indent=4, ensure_ascii=False)) 
# ====================================================

#! c:\python3\python.exe 
# coding: utf-8
"""
k_counter_del_value @occ=:occ1, @counter_id1=:counter_id1, @id1=:id1
"""
import os, sys
import pyodbc
import json
import my_sql_func
import cgi
import html
import socket
import logging.config

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logger = logging.getLogger('main')

occ_in = ""  # "700204367"
counter_id_in = ""  # "62628"
id_in = ""  # "1307087"

form = cgi.FieldStorage()
occ = form.getfirst("occ", occ_in)
occ = html.escape(occ)
counter_id = form.getfirst("counter_id", counter_id_in)
counter_id = html.escape(counter_id)
id = form.getfirst("id", id_in)
id = html.escape(id)
logger.info(f"start {os.path.basename(__file__)} occ={occ}, counter_id={counter_id}, id={id}")
if occ == "" or  counter_id=="" or id=="":
	print("Content-type: text/html \n")
	msg_err="occ or counter_id or id not set"
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

params = (occ, counter_id, id)
cursor.execute("k_counter_del_value @occ=?, @counter_id1=?, @id1=?", params)
row = cursor.fetchone()  # одна строка
data = {"oper": 'delete value', "id": id, "res": row.res, "strerror": row.strerror,
        "result_add": False if row.res == 0 else True}

cursor.commit()
cursor.close()
conn.close() 

# =====================================================
print("Content-type: application/json; charset=utf-8 \n")
print(json.dumps(data, indent=4, ensure_ascii=False)) 
# =====================================================

# echo "{";
# echo '"id":'.$id1.',';
# echo '"result_add":'.$result_add.'';
# echo "}";

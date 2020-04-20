#! c:\python3\python.exe 
# coding: utf-8
"""
k_counter_add_value @occ=:occ1, @counter_id1=:counter_id1,@inspector_value1=:inspector_value1, 
	@inspector_date1=:inspector_date1, @AppComment=:AppComment"
"""
import os, sys
import pyodbc
import json
import my_sql_func
import cgi
import html
import datetime
import socket
import logging.config
import logging_yaml

logging_yaml.setup_logging()
#logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

occ_in = ""  # "700204367"
counter_id_in = ""  # "62628"
inspector_value_in = ""  # "134"


form = cgi.FieldStorage()
occ = form.getfirst("occ", occ_in)
occ = html.escape(occ)
counter_id = form.getfirst("counter_id", counter_id_in)
counter_id = html.escape(counter_id)
inspector_value = form.getfirst("inspector_value", inspector_value_in)
inspector_value = html.escape(inspector_value)
cur_date = datetime.date.today().strftime("%Y%m%d")
inspector_date = form.getfirst("inspector_date", cur_date)  # текущая дата по умолчанию
inspector_date = html.escape(inspector_date)
logger.info(f"start {os.path.basename(__file__)} occ={occ}, counter_id={counter_id}, inspector_value={inspector_value}")
if occ == "" or  counter_id=="" or inspector_value=="":
	print("Content-type: text/html \n")
	msg_err="occ or counter_id or inspector_value not set"
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

params = (occ, counter_id, inspector_value, inspector_date)

sql = """\
DECLARE @result_add	BIT=0	
EXECUTE k_counter_add_value @occ=?,@counter_id1=?,@inspector_value1=?,@inspector_date1=?,@result_add=@result_add OUT
select result_add=@result_add
"""

try:
    cursor.execute(sql, params)
except:
    logger.exception("exception message")
    raise
row = cursor.fetchone()  # одна строка
# row = cursor.fetchall()
data = {"oper": 'add value', "counter_id": counter_id, "res": row.res, "strerror": row.strerror, "id_new": row.id_new}
# data={"counter_id":counter_id,"strerror":row.strerror}
if cursor.nextset():
    row = cursor.fetchone()
    # print(row)
    data['result_add'] = row[0]

cursor.commit()
cursor.close()
conn.close() 

# =====================================================
print("Content-type: application/json; charset=utf-8 \n")
print(json.dumps(data, indent=4, ensure_ascii=False))
# =====================================================

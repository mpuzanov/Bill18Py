# -*- coding: utf-8 -*-

"""
k_show_occ @occ=:occ1
k_show_counters @occ=:occ1
k_show_counters_value @occ=:occ1, @row1=:KolVal

Для prof-версии
k_show_payings @occ=:occ1
k_show_values_occ @fin_id=Null, @occ=:occ1
"""

import os, sys
import cgi
import html
import json
from datetime import date, datetime
#import simplejson
from decimal import Decimal
import socket
import pyodbc
import my_sql_func
import logging.config

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logger = logging.getLogger('main')

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError("Type %s not serializable" % type(obj))

# cgi.print_environ()
# cgi.print_environ_usage()
# cgi.test()


lic_in = ""  # 45321 45322
pro_in = 0
kolval_in = 6

form = cgi.FieldStorage()
lic = form.getfirst("lic", lic_in)   #
# lic = html.escape(lic)
pro = form.getfirst("pro", pro_in)   #
kolval = form.getfirst("kolval", kolval_in)   #
logger.info(f"start {os.path.basename(__file__)} lic={lic}, pro={pro}, kolval={kolval}")
if lic == "":
    print("Content-type: text/html \n")
    msg_err="lic not set"
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

params = lic
try:
    cursor.execute("exec k_show_occ @occ=?", params)
except:
    logger.exception("exception message")
    raise

row = cursor.fetchone()  # одна строка
if not row:
    data = {"lic": lic, "dataOcc": {}}
else:
    cols = [i[0] for i in cursor.description]
    data = {"lic": lic, "dataOcc": dict(zip(cols, row))}

    # =====================================================
    cursor.execute("{CALL k_show_counters (?)}", params)
    rows = cursor.fetchall()
    cols = [i[0] for i in cursor.description]
    data["dataCounter"] = []
    for item in rows:
        data["dataCounter"].append(dict(zip(cols, item)))
    # =====================================================
    cursor.execute("exec k_show_counters_value @occ=?, @row1=?", (lic, kolval))
    rows = cursor.fetchall()
    cols = [i[0] for i in cursor.description]
    data["dataCounterValue"] = []
    for item in rows:
        data["dataCounterValue"].append(dict(zip(cols, item)))
    # =====================================================
    if pro == 1:
        cursor.execute("exec k_show_payings @occ=?", lic)
        rows = cursor.fetchall()
        cols = [i[0] for i in cursor.description]
        data["dataPaym"] = []
        for item in rows:
            data["dataPaym"].append(dict(zip(cols, item)))
        # =====================================================
        cursor.execute("exec k_show_values_occ @fin_id=Null, @occ=?", lic)
        rows = cursor.fetchall()
        cols = [i[0] for i in cursor.description]
        data["dataValue"] = []
        for item in rows:
            data["dataValue"].append(dict(zip(cols, item)))
        # =====================================================

cursor.close()
conn.close()
# =====================================================
print("Content-type: application/json; charset=utf-8 \r")
print("\r")
print(json.dumps(data, default=json_serial, indent=4, ensure_ascii=False))
# =====================================================

# записываем в файл
# with open('filename.txt', 'w', encoding='utf8') as json_file:
#     json.dump(data, json_file, default=json_serial, indent=4, ensure_ascii=False)

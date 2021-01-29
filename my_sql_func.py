# coding: utf-8
"""
Сервисные функции по взаимодействию с базой данных
"""
import pyodbc
import os
import configparser  # Библиотека для чтения конфигов


def create_connect_str(ini_file, section):
    """
    Формирование строки соединения с SQL server \n
    :ini_file: - файл с параметрами соединения \n
    :section: - секция в ini файле для чтения параметров \n
    :return: строка подключения \n
    """
    config = configparser.ConfigParser()

    ini_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ini_file)
    if not os.path.isfile(ini_file):
        raise RuntimeError(f"Не найден файл {ini_file}")
    # config.read(ini_file, "utf8")
    config.read(ini_file, encoding='utf-8-sig')

    driver = 'DRIVER='+config.get(section, 'driver')
    server = 'SERVER='+config.get(section, 'server')
    port = 'PORT='+config.get(section, 'port')
    database = 'DATABASE='+config.get(section, 'database')
    uid = 'UID='+config.get(section, 'uid')
    pwd = 'PWD='+config.get(section, 'pwd')
    return ';'.join([driver, server, port, database, uid, pwd])


def create_connection(ini_file, section):
    """
    Возврат объекта соединения с SQL server \n
    :ini_file: - файл с параметрами соединения \n
    :section: - секция в ini файле для чтения параметров \n
    :return: строка подключения \n
    """
    config = configparser.ConfigParser()

    ini_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ini_file)
    if not os.path.isfile(ini_file):
        raise RuntimeError(f"Не найден файл {ini_file}")
    # config.read(ini_file, "utf8")
    config.read(ini_file, encoding='utf-8-sig')

    driver = config.get(section, 'driver')
    server = config.get(section, 'server')
    port = config.get(section, 'port')
    database = config.get(section, 'database')
    uid = config.get(section, 'uid')
    pwd = config.get(section, 'pwd')
    str_connect = "Driver="+driver+";Server="+server+";PORT="+port+";Database="+database+";UID="+uid+";PWD="+pwd
    try:
        conn = pyodbc.connect(str_connect, autocommit=True)
        # print(f"Connection to MS SQL Server {server} successful")
    except pyodbc.OperationalError as e:
        print(f"The error '{e}' occurred")
        raise

    return conn


def create_query_from_dict(in_dict):
    res_str = in_dict.get('sql', '')
    if in_dict.get('type', 'sp') == 'sp':   # хранимая процедура
        dict_params = in_dict.get('params', {})
        res_str += ','.join(' {}={}'.format(key, value) for key, value in dict_params.items())
    else:
        dict_params = in_dict.get('params', {})
        for key in dict_params:
            # заменяем имя параметра на значение
            res_str = res_str.replace(key, str(dict_params.get(key)))

    return res_str

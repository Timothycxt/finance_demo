import os

from App.utils.config_helper import get_config_map

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_map = get_config_map()

class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = config_map['app']['secret_key']


def get_db_uri(dbinfo):
    engine = dbinfo.get("ENGINE") or "sqlite"
    drive = dbinfo.get("DRIVER") or "sqlite"
    username = dbinfo.get("USERNAME") or ""
    password = dbinfo.get("PASSWORD") or ""
    host = dbinfo.get("HOST") or ""
    port = dbinfo.get("PORT") or ""
    name = dbinfo.get("NAME") or ""
    return "{}+{}://{}:{}@{}:{}/{}".format(engine, drive, username, password, host, port, name)


# 开发环境配置
class DevelopConfig(Config):
    DEBUG = True
    dbinfo = {
        "ENGINE": "postgresql",
        "DRIVER": "psycopg2",
        "USERNAME": config_map['postgresql']['username'],
        "PASSWORD": config_map['postgresql']['password'],
        "HOST": config_map['postgresql']['host'],
        "PORT": config_map['postgresql']['port'],
        "NAME": config_map['postgresql']['database']
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


# class TestConfig(Config):
#     TESTING = True
#
#     dbinfo = {
#         "ENGINE": "mysql",
#         "DRIVER": "pymysql",
#         "USERNAME": "root",
#         "PASSWORD": "",
#         "HOST": "localhost",
#         "PORT": "3306",
#         "NAME": "flask_demo"
#     }
#
#     SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


# 生产环境配置
# class ProductConfig(Config):
#     PRODUCT = True
#
#     dbinfo = {
#         "ENGINE": "mysql",
#         "DRIVER": "pymysql",
#         "USERNAME": "root",
#         "PASSWORD": "",
#         "HOST": "192.168.0.106",
#         "PORT": "3306",
#         "NAME": "flask_demo"
#     }
#
#     SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


envs = {
    "develop": DevelopConfig,
    # "testing": TestConfig,
    # "pruduct": ProductConfig,
    # "default": DevelopConfig
}

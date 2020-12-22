# 程序入口
import os
from flask_script import Manager
from App import create_app
# from flask_cors import *

env = os.environ.get("FLASK_ENV", "develop")
app = create_app(env)
# CORS(app, supports_credentials=True)  # 设置跨域
manager = Manager(app)

if __name__ == '__main__':
    manager.run()

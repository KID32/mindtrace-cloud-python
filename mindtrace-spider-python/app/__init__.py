from general.nacos_utils import nacos_init
from flask import Flask

app = Flask(__name__)

ip = "127.0.0.1"
port = 34984
# 注册服务
nacos_init(ip=ip, port=port, service_name="mindtrace-spider-python")

import requests
from .nacos_utils import gateway_host

# session设置：登录mindtrace-gateway以通过认证检查
session = requests.Session()
# 登录请求
session.post(f"{gateway_host()}/user/login", json={"username": "juumii", "password": "123456"})

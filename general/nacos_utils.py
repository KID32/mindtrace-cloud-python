import threading
import time

import nacos

service_client = nacos.NacosClient(server_addresses="localhost:8848", namespace="public")


def nacos_init(ip: str, port: int, service_name: str):
    # 注册服务
    service_client.add_naming_instance(service_name=service_name, ip=ip, port=port)

    # 心跳续约
    def send_heartbeat():
        heartbeat = 5
        while True:
            # 发送心跳
            service_client.send_heartbeat(service_name, ip, port)
            # 等待下一个心跳周期
            time.sleep(heartbeat)

    heartbeat_thread = threading.Thread(target=send_heartbeat, daemon=True)
    heartbeat_thread.start()


def serv_host(service: dict) -> str:
    return f"http://{service['hosts'][0]['ip']}:{service['hosts'][0]['port']}"


def gateway_host() -> str:
    mindtrace_gateway: dict = service_client.list_naming_instance("mindtrace-gateway")
    return serv_host(mindtrace_gateway)

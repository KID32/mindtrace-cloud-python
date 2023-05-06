import json
import random
import os

import requests

gateway_host = "http://localhost:34443"
def generate(knodes: list[dict]):
    session = requests.Session()
    user_info = {
        "username": f"user{random.randint(0,10000)}",
        "password": "123456"
    }
    user_result = session.post(url=f"{gateway_host}/user/register", json=user_info).json()
    login = session.post(url=f"{gateway_host}/user/login", json=user_info)
    user_id = user_result["data"]
    root_id = session.get(url=f"{gateway_host}/core/user/{user_id}/root").json()
    id_mapping: dict = {-1: root_id}
    for knode in knodes:
        branch_url = f"{gateway_host}/core/knode/{id_mapping[knode['stem']]}/branch?title="
        branch = session.post(url=branch_url).json()
        update_url = f"{gateway_host}/core/knode/{branch['id']}"
        session.post(url=update_url, json={"title": knode["title"]})
        id_mapping[knode["id"]] = int(branch["id"])


def get_files_in_folder(folder_path):
    # 初始化文件列表
    file_list = []
    # 遍历指定目录下的所有文件和子目录
    for root, dirs, files in os.walk(folder_path):
        # 遍历当前目录下的所有文件
        for file in files:
            # 获取文件的完整路径
            file_path = os.path.join(root, file)
            # 将文件路径添加到文件列表中
            file_list.append(file_path)
    # 返回文件列表
    return file_list

if __name__ == '__main__':
    data_list = get_files_in_folder("./data/knodes")
    for data in data_list:
        with open(data, "r") as data_file:
            try:
                generate(json.load(data_file))
            except:
                pass


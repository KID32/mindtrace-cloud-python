import os

import requests
import numpy as np


api_key = os.getenv("OPENAI_API_KEY")
endpoint = "https://api.openai.com/v1/embeddings"
model = "text-embedding-ada-002"

dimension = 1536
def get_feature_vector(text):
    r"""
    :param text: 字符串或字符串数组均可
    :return: numpy array , 2维, shape=(n,1536)
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    params = {
        "model": model,
        "input": text
    }
    resp = requests.post(url=endpoint, json=params, headers=headers)
    resp_data = resp.json()["data"]
    return np.array([resp_data[i]["embedding"] for i in range(0, len(resp_data))])


if __name__ == '__main__':
    pass

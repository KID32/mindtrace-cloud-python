import requests
from bs4 import BeautifulSoup
import re
import json
from . import headers


def resolve(url: str) -> dict:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        script = soup.find("script")
        while script is not None:
            initial_state_pattern = re.compile(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', re.DOTALL)
            initial_state_match = initial_state_pattern.search(script.text)

            if initial_state_match:
                initial_state_json = initial_state_match.group(1)
                initial_state_dict = json.loads(initial_state_json)

                # 提取有用数据
                up_data_keys = ["mid", "name"]
                up_data = {k: initial_state_dict["upData"][k] for k in up_data_keys}
                video_data_keys = ["aid", "bvid", "cid", "duration", "title"]
                video_data = {k: initial_state_dict["videoData"][k] for k in video_data_keys}
                page_data_keys = ["duration", "page", "part"]
                page_data = [{k: page[k] for k in page_data_keys} for page in initial_state_dict["videoData"]["pages"]]
                target_data = {
                    "upData": up_data,
                    "videoData": video_data,
                    "pages": page_data
                }

                return target_data

            script = script.next_element
    return json.loads(response.json())

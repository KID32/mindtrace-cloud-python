import json
import os
import threading
from flask import Flask

from general.session_utils import session
from .service.word_similarity.gpt_embeddings import get_feature_vector
from .service.ann.faiss_ann import add_to_index, save_index, add_to_index_batch
from general.nacos_utils import nacos_init, gateway_host
from general.mq_utils import *

# 创建Flask应用实例
app = Flask(__name__)
# 注册服务
nacos_init(ip="127.0.0.1", port=31595, service_name="mindtrace-knode-similarity-python")

def get_chain_style_title(knode_id) -> str:
    resp: list[str] = session.get(f"{gateway_host()}/core/knode/{knode_id}/chainStyleTitle").json()
    if resp.__contains__("ROOT"):
        resp.remove("ROOT")
    resp.reverse()
    title = " ".join(resp)
    return title if title != "" else " EMPTY "


# 处理 knode update 消息：更新索引库，为了提高效率，每20条数据批量进行
abspath = os.path.abspath(os.path.dirname(__file__))
cache_path = os.path.join(abspath, "cache.json")
with open(cache_path, "r") as cache_file_read:
    cache: list = json.load(cache_file_read)
def on_knode_update(ch, method, properties, body):
    print(f"Received message: {body.decode('utf-8')}")
    data = json.loads(body.decode("utf-8"))
    title = get_chain_style_title(data["id"])
    if title != "":
        cache.append(title)
    if len(cache) > 20:
        with app.app_context():
            features = get_feature_vector([get_chain_style_title(knode_id) for knode_id in cache])
            mapping = {cache[i]: features[i] for i in range(0, len(cache))}
            add_to_index_batch(mapping)
            save_index()
        cache.clear()
    with open(cache_path, "w") as cache_file_write:
        json.dump(cache, cache_file_write)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue=update_knode_event_mq, on_message_callback=on_knode_update)
# 消费update knode信息的线程
def start_consumer():
    # ... set up connection, channel, exchange, queues, and bindings ...
    print('Waiting for messages...')
    channel.start_consuming()
consumer_thread = threading.Thread(target=start_consumer)
consumer_thread.start()




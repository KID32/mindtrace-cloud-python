import json
import threading
from flask import Flask
from .service.word_similarity.bert_word_similarity import get_feature_vector
from general.nacos_utils import nacos_init
from general.mq_utils import channel

# 创建Flask应用实例
app = Flask(__name__)
# 注册服务
nacos_init(ip="127.0.0.1", port=31595, service_name="mindtrace-knode-similarity-python")


# 处理 knode update 消息：视情况更新knode feature
def on_knode_update(ch, method, properties, body):
    from .service.persistent import knode_feature as record
    print(f"Received message: {body.decode('utf-8')}")
    data = json.loads(body.decode("utf-8"))
    title = record.get_chain_style_title(data["createBy"], data["id"])
    if title != "":
        with app.app_context():
            record.set_knode_feature(int(data["id"]), get_feature_vector(title))
    ch.basic_ack(delivery_tag=method.delivery_tag)
# MQ路由配置
exchange_name = "knode_event_exchange"
mq_name = "update_event_mq"
routing_key_update = "update"
channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)
channel.queue_declare(queue=mq_name, durable=True)
channel.queue_bind(queue=mq_name, exchange=exchange_name, routing_key=routing_key_update)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=mq_name, on_message_callback=on_knode_update)
# 消费update knode信息的线程
def start_consumer():
    # ... set up connection, channel, exchange, queues, and bindings ...
    print('Waiting for messages...')
    channel.start_consuming()
consumer_thread = threading.Thread(target=start_consumer)
consumer_thread.start()




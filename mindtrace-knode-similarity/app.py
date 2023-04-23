import json
import numpy as np
from app import app
import app.service.persistent.knode_feature as record
from app.service.word_similarity.bert_word_similarity import get_feature_vector
from flask import request
from sklearn.metrics.pairwise import cosine_similarity


@app.route("/debug")
def hello_world():
    record.set_knode_feature(1, np.array([1, 2, 3]))
    print(record.get_knode_feature(1).feature)
    return str(record.get_knode_feature(1))


@app.route("/<int:knode_id>", methods=["POST"])
def set_knode_feature(knode_id: int):
    record.set_knode_feature(int(knode_id), get_feature_vector(request.json["chainStyleTitle"]))
    return get_knode_feature(knode_id)


@app.route("/<int:knode_id>", methods=["GET"])
def get_knode_feature(knode_id: int):
    return json.dumps(record.get_knode_feature(knode_id).feature.tolist())


@app.route("/user/<int:fst_user_id>/knode/<int:fst_id>/user/<int:snd_user_id>/knode/<int:snd_id>")
def get_knode_similarity(fst_user_id: int, fst_id: int, snd_user_id: int, snd_id: int):
    fst = record.get_knode_feature(fst_id)
    snd = record.get_knode_feature(snd_id)
    if fst is None:
        record.set_knode_feature(fst_id, get_feature_vector(record.get_chain_style_title(fst_user_id, fst_id)))
    if snd is None:
        record.set_knode_feature(snd_id, get_feature_vector(record.get_chain_style_title(snd_user_id, snd_id)))
    return str(cosine_similarity(fst.feature, snd.feature))


if __name__ == '__main__':
    app.run(port=31595)

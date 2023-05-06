import json
from app import app, get_chain_style_title
from app.service.word_similarity.gpt_embeddings import get_feature_vector
from app.service.ann.faiss_ann import add_to_index_batch, save_index
from flask import request
from app.service.ann.faiss_ann import get_ann_knode_ids, get_feature_by_knode_id


@app.route("/debug")
def hello_world():
    return "hello world"

@app.route("/knode/<int:knode_id>/similar")
def get_nearest_neighbors(knode_id: int):
    count: int = int(request.args.get("count"))
    knode_feature = get_feature_by_knode_id(knode_id)
    if knode_feature is not None:
        return json.dumps(get_ann_knode_ids(knode_feature.feature, count))
    else:
        return "[]"

@app.route("/index", methods=["DELETE"])
def clear_index():
    pass

@app.route("/index", methods=["POST"])
def add_index():
    data: dict = request.json
    ids: list[int] = data["knodeIds"]
    chunk_size = 100
    chunks = [ids[i:i + chunk_size] for i in range(0, len(ids), chunk_size)]
    for chunk in chunks:
        features = get_feature_vector([get_chain_style_title(knode_id) for knode_id in chunk])
        mapping = {chunk[i]: features[i] for i in range(0, len(chunk))}
        add_to_index_batch(mapping)
    save_index()
    return ""

if __name__ == '__main__':
    app.run(port=31595)



import json
import faiss
import numpy as np
from ..utils import FeatureVector
from . import index, mapping, feature_mapping, index_src, mapping_src, feature_mapping_src

def get_feature_by_knode_id(knode_id):
    return np.array(feature_mapping[knode_id])


def get_ann_knode_ids(feature: FeatureVector, count: int) -> list[int]:
    return [mapping[str(i)] for i in get_ann_indices(feature, count)[0] if mapping.keys().__contains__(str(i))]


def get_ann_indices(feature: FeatureVector, count: int):
    return index.search(feature, count)[1]


def add_to_index(feature: FeatureVector, knode_id: int) -> None:
    index.add(feature)
    mapping[index.ntotal] = knode_id
    feature_mapping[knode_id] = feature.tolist()


def add_to_index_batch(id_feature_mapping: dict) -> None:
    r"""
    :param id_feature_mapping: 如{"15495132546": [ ... ], ...}
    :return: None
    """
    items = id_feature_mapping.items()
    matrix = np.vstack([feature for (knode_id, feature) in items])
    cur = index.ntotal
    index.add(matrix)
    for knode_id, feature in items:
        mapping[cur] = knode_id
        feature_mapping[knode_id] = feature
        cur += 1


def save_index():
    faiss.write_index(index, index_src)
    with open(mapping_src, 'w') as mapping_file:
        json.dump(mapping, mapping_file, ensure_ascii=False, indent=4)
    with open(feature_mapping_src, 'w') as feature_mapping_file:
        json.dump(feature_mapping_file, feature_mapping_file, ensure_ascii=False, indent=4)


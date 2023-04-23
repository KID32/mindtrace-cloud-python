import pickle
from typing import Tuple
import numpy as np

from general.session_utils import session
from general.nacos_utils import gateway_host
from general.mysql_utils import connect
from ... import app

# 连接数据库
database = connect(app, "mindtrace_knode_similarity")

# 类型声明
FeatureVector = np.ndarray[np.float32, Tuple[int]]


class KnodeFeature(database.Model):
    knode_id = database.Column(database.BigInteger, primary_key=True, nullable=False)
    feature_blob = database.Column(database.LargeBinary, nullable=False)

    @property
    def feature(self) -> FeatureVector:
        return pickle.loads(self.feature_blob)

    @feature.setter
    def feature(self, value):
        if value is not None:
            self.feature_blob = pickle.dumps(value)

    def __repr__(self):
        return f'<KnodeFeature {self.knode_id}>'


# add + update
def set_knode_feature(knode_id, feature: FeatureVector):
    knode_feature: KnodeFeature = KnodeFeature.query.get(knode_id)
    if knode_feature:
        knode_feature.feature = feature
        database.session.commit()
    else:
        new_knode_feature = KnodeFeature(knode_id=knode_id, feature=feature)
        database.session.add(new_knode_feature)
        database.session.commit()


# 删除记录
def delete_knode_feature(knode_id):
    knode_feature = KnodeFeature.query.get(knode_id)
    if knode_feature:
        database.session.delete(knode_feature)
        database.session.commit()


# 查询记录
def get_knode_feature(knode_id) -> KnodeFeature:
    return KnodeFeature.query.get(knode_id)


# 查询所有记录
def get_all_knode_features():
    return KnodeFeature.query.all()


def get_chain_style_title(user_id, knode_id) -> str:
    resp = session.get(f"{gateway_host()}/core/user/{user_id}/knode/{knode_id}/chainStyleTitle").json()
    try:
        title = ""
        for txt in resp["data"]:
            title = title + " " + txt
        return title
    except KeyError:
        return ""

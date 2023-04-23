import torch
from transformers import BertTokenizer, BertModel

# 加载预训练的BERT模型和分词器
model_name = "bert-base-multilingual-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)


def get_feature_vector(text):
    # 对文本进行分词和编码
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    # 输入模型并获得输出
    with torch.no_grad():
        outputs = model(**inputs)
    # 提取句子嵌入（对所有单词嵌入求平均）
    return outputs.last_hidden_state.mean(dim=1).numpy()

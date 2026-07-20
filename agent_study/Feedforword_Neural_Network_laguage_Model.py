"""
前馈神经网络语言模型
"""

import numpy as np


"""
通过np.array()将含多个值的列表转换为一个数学意义上的向量
例子:
vec = np.array([0.9,0.8]) #从[0.9,0.8] --> [0.9 0.8](代表二维空间的一个坐标)
"""

#嵌入向量 -->将每个词映射到空间坐标
embeddings = {
    "king": np.array([0.9, 0.8]),
    "queen": np.array([0.9, 0.2]),
    "man": np.array([0.7, 0.9]),
    "woman": np.array([0.7, 0.3])
}

#求两个向量余弦相似度
def cosine_similarity(vec1, vec2):
    """
    dot是点积
    点积越大，两个向量的夹角越小，方向越近
    点积越小，向量差距越大

    np.linalg.norm 等于向量模长
    """
    dot_product = np.dot(vec1, vec2)
    norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    return dot_product / norm_product #返回余弦相似度 就是余弦值

#king - man + woman
result_vec = embeddings["king"] - embeddings["man"] + embeddings["woman"]

#计算这个向量和queen的cosine_similarity
sim = cosine_similarity(result_vec, embeddings["queen"])

print(f"king - man - woman 的结果向量 : {result_vec}")
print(f"该结果与‘queen'的相似度 : {sim:.4f} ")
"""
这说明了如果经过训练的模型 每个向量会由语义在里面 也就解决了N——gram模型的泛化能力差的问题
但是比没有解决上下文的问题 --> 就是没有记忆能力
"""


import torch
import faiss
import numpy as np

# 加载嵌入
embedding_save_path = "output/best_embeddings.pth"
h_item = torch.load(embedding_save_path)  # shape: (num_items, embedding_dim)
if h_item.is_cuda:
    h_item = h_item.cpu()
# 将嵌入加载到 FAISS 索引
item_embeddings = h_item.numpy().astype(np.float32)  # FAISS 需要 float32 格式
dimension = item_embeddings.shape[1]  # 嵌入维度
index = faiss.IndexFlatL2(dimension)  # 使用 L2 距离的索引
index.add(item_embeddings)

# 定义推荐函数
def recommend(item_id, top_k=10):
    """
    基于物品 ID，返回最相似的 K 个物品。
    Args:
        item_id: 待查询物品 ID
        top_k: 返回的推荐物品数量
    Returns:
        推荐物品的 ID 列表
    """
    item_vector = item_embeddings[item_id].reshape(1, -1)  # 查询物品的嵌入
    distances, indices = index.search(item_vector, top_k)  # 查询最近邻
    return indices.flatten().tolist()

# 示例：推荐与物品 42 最相似的 10 个物品
recommended_items = recommend(item_id=42, top_k=10)
print("Recommended items:", recommended_items)

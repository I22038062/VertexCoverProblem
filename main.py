from pyqubo import Binary, Constraint
from dwave.samplers import SimulatedAnnealingSampler
import networkx as nx

#讀取測試資料
file_path = "/content/drive/MyDrive/Colab Notebooks/keller4.mis"  #改成任意路徑
edges = []
with open(file_path, "r") as f:
    for i, line in enumerate(f):
        if i == 0:
            continue  #skip header line
        u, v = map(int, line.strip().split()[1:])
        edges.append((u, v))

#建立NetworkX圖
G = nx.Graph()
G.add_edges_from(edges)

#建構QUBO模型
#建立變數：對每個頂點建立二元變數（是否被選為覆蓋集成員,1表示被選擇作為子集的一部份，0表示不選擇）
variables = {v: Binary(f"x{v}") for v in G.nodes}

#建立Hamiltonian
A = 3.0  #約束權重（對不合法邊的懲罰）
B = 1.0  #目標權重（最小化選取節點數）

#每條邊至少一端要被選進覆蓋集 => (1 - x_u)(1 - x_v)
H_constraints = sum(
    Constraint((1 - variables[u]) * (1 - variables[v]), label=f"edge_{u}_{v}")
    for u, v in G.edges
)

#目標函數：最小化選進覆蓋集的節點數
H_objective = sum(variables[v] for v in G.nodes)

#總能量函數
H = A * H_constraints + B * H_objective

#編譯並轉換為QUBO
model = H.compile()
qubo, offset = model.to_qubo()

#使用模擬退火解決QUBO
sampler = SimulatedAnnealingSampler()
sampleset = sampler.sample_qubo(qubo, num_reads=1000)
best_sample = sampleset.first.sample
best_energy = sampleset.first.energy + offset

#擷取覆蓋集
cover_set = [int(v[1:]) for v, val in best_sample.items() if val == 1]

#顯示結果
print("找到的覆蓋集大小:", len(cover_set))
print("覆蓋頂點集合:", sorted(cover_set))
print("Hamiltonian Energy:", best_energy)

#額外驗證：確認是否為合法覆蓋集
def is_valid_vertex_cover(G, cover):
    return all(u in cover or v in cover for u, v in G.edges)

print("是否為合法覆蓋集:", is_valid_vertex_cover(G, set(cover_set)))

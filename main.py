from pyqubo import Binary, Constraint
from dwave.samplers import SimulatedAnnealingSampler
import networkx as nx

#Ū�����ո��
file_path = "/content/drive/MyDrive/Colab Notebooks/keller4.mis"  #�令���N���|
edges = []
with open(file_path, "r") as f:
    for i, line in enumerate(f):
        if i == 0:
            continue  #skip header line
        u, v = map(int, line.strip().split()[1:])
        edges.append((u, v))

#�إ�NetworkX��
G = nx.Graph()
G.add_edges_from(edges)

#�غcQUBO�ҫ�
#�إ��ܼơG��C�ӳ��I�إߤG���ܼơ]�O�_�Q�אּ�л\������,1��ܳQ��ܧ@���l�����@�����A0��ܤ���ܡ^
variables = {v: Binary(f"x{v}") for v in G.nodes}

#�إ�Hamiltonian
A = 3.0  #�����v���]�藍�X�k�䪺�g�@�^
B = 1.0  #�ؼ��v���]�̤p�ƿ���`�I�ơ^

#�C����ܤ֤@�ݭn�Q��i�л\�� => (1 - x_u)(1 - x_v)
H_constraints = sum(
    Constraint((1 - variables[u]) * (1 - variables[v]), label=f"edge_{u}_{v}")
    for u, v in G.edges
)

#�ؼШ�ơG�̤p�ƿ�i�л\�����`�I��
H_objective = sum(variables[v] for v in G.nodes)

#�`��q���
H = A * H_constraints + B * H_objective

#�sĶ���ഫ��QUBO
model = H.compile()
qubo, offset = model.to_qubo()

#�ϥμ����h���ѨMQUBO
sampler = SimulatedAnnealingSampler()
sampleset = sampler.sample_qubo(qubo, num_reads=1000)
best_sample = sampleset.first.sample
best_energy = sampleset.first.energy + offset

#�^���л\��
cover_set = [int(v[1:]) for v, val in best_sample.items() if val == 1]

#��ܵ��G
print("��쪺�л\���j�p:", len(cover_set))
print("�л\���I���X:", sorted(cover_set))
print("Hamiltonian Energy:", best_energy)

#�B�~���ҡG�T�{�O�_���X�k�л\��
def is_valid_vertex_cover(G, cover):
    return all(u in cover or v in cover for u, v in G.edges)

print("�O�_���X�k�л\��:", is_valid_vertex_cover(G, set(cover_set)))

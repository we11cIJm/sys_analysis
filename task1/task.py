import sys, csv
import numpy as np

def main():
    path, root = sys.argv[1], sys.argv[2]
    E = [tuple(row) for row in csv.reader(open(path))]
    nodes = sorted({u for u, v in E} | {v for u, v in E} | {root})
    idx = {n : i for i, n in enumerate(nodes)}
    N = len(nodes)
    A = np.zeros((N, N), int)
    for u, v in E: A[idx[u], idx[v]] = 1

    R = A.copy()
    for k in range(N):
        R |= (R[:, k, None] & R[None, k, :])
    R_direct = A
    R_indirect = R & ~A
    r1 = R_direct
    r2 = r1.T
    r3 = R_indirect
    r4 = r3.T

    co = np.zeros((N, N),int)
    for p in nodes:
        children = [idx[v] for u, v in E if u==p]
        for i in children:
            for j in children:
                if i != j : co[i, j]=1
    print((A, r1, r2, r3, r4, co))

if __name__=="__main__":
    main()

from typing import Tuple
import math

def main(s: str, e: str) -> Tuple[float, float]:
    lines = [x.strip() for x in s.strip().splitlines() if x.strip()]
    edges = []
    for ln in lines:
        a, b = [x.strip() for x in ln.split(",")]
        edges.append((a, b))
    nodes = set([e])
    for a, b in edges:
        nodes.add(a); nodes.add(b)
    n = len(nodes)
    if n <= 1:
        return 0.0, 0.0

    children = {}
    parent = {}
    for a, b in edges:
        children.setdefault(a, []).append(b)
        parent[b] = a

    r1 = set(edges)
    r2 = {(b, a) for a, b in r1}

    r3 = set()
    for v in nodes:
        u = parent.get(v)
        d = 1
        while u is not None:
            if d >= 2:
                r3.add((u, v))
            u = parent.get(u)
            d += 1

    r4 = {(b, a) for a, b in r3}

    r5 = set()
    for p, ch in children.items():
        m = len(ch)
        for i in range(m):
            for j in range(i + 1, m):
                a, b = ch[i], ch[j]
                r5.add((a, b)); r5.add((b, a))

    rels = (r1, r2, r3, r4, r5)
    out = [{u: 0 for u in nodes} for _ in range(5)]
    for i, R in enumerate(rels):
        for a, b in R:
            if a in nodes and b in nodes and a != b:
                out[i][a] += 1

    den = n - 1
    H = 0.0
    for u in nodes:
        for i in range(5):
            l = out[i][u]
            if l:
                p = l / den
                H -= p * math.log(p, 2)

    c = 1.0 / (math.e * math.log(2.0))
    Href = c * n * 5
    h = H / Href if Href else 0.0
    return round(H, 1), round(h, 1)


if __name__ == '__main__':
    import pandas as pd

    df = pd.read_csv("task2.csv", header=None)
    s = "\n".join(df[0].astype(str) + "," + df[1].astype(str))

    H, h = main(s, "e")
    print(H, h)
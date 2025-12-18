import json, ast, re

def _loads(x):
    if not isinstance(x, str):
        return x
    try:
        return json.loads(x)
    except Exception:
        try:
            return ast.literal_eval(x)
        except Exception:
            return ast.literal_eval(re.sub(r",\s*([\]\}])", r"\1", x))

def main(a_json: str, b_json: str) -> str:
    A, B = _loads(a_json), _loads(b_json)

    def norm(r):
        return [[str(y) for y in x] if isinstance(x, (list, tuple)) else [str(x)] for x in r]

    A, B = norm(A), norm(B)

    def k(s):
        return (0, int(s)) if s.isdigit() else (1, s)

    objs = sorted({y for cl in A + B for y in cl}, key=k)
    n = len(objs)
    idx = {o: i for i, o in enumerate(objs)}
    posA = {o: i for i, cl in enumerate(A) for o in cl}
    posB = {o: i for i, cl in enumerate(B) for o in cl}

    YA = [[1 if posA[objs[i]] >= posA[objs[j]] else 0 for j in range(n)] for i in range(n)]
    YB = [[1 if posB[objs[i]] >= posB[objs[j]] else 0 for j in range(n)] for i in range(n)]

    core = []
    for i in range(n):
        for j in range(i + 1, n):
            if (YA[i][j] & YB[i][j]) == 0 and (YA[j][i] & YB[j][i]) == 0:
                core.append((i, j))

    C = [[YA[i][j] & YB[i][j] for j in range(n)] for i in range(n)]
    for i, j in core:
        C[i][j] = C[j][i] = 1

    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a

    for i in range(n):
        for j in range(i + 1, n):
            if C[i][j] and C[j][i]:
                union(i, j)

    comps = {}
    for o in objs:
        comps.setdefault(find(idx[o]), []).append(o)

    clusters = [sorted(v, key=k) for v in comps.values()]
    reps = [min(cl, key=k) for cl in clusters]
    repi = [idx[r] for r in reps]
    m = len(clusters)

    better = [0] * m
    for p in range(m):
        for q in range(m):
            if p != q and C[repi[p]][repi[q]] and not C[repi[q]][repi[p]]:
                better[p] += 1

    order = sorted(range(m), key=lambda t: (better[t], k(reps[t])))
    res = [clusters[t][0] if len(clusters[t]) == 1 else clusters[t] for t in order]
    return json.dumps(res, ensure_ascii=False)


if __name__ == "__main__":
    with open("json_data/Ранжировка  A.json", encoding="utf-8") as f:
        a = f.read()
    with open("json_data/Ранжировка  B.json", encoding="utf-8") as f:
        b = f.read()
    print(main(a, b))

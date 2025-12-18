import json, ast, re
import sys


def _loads(x):
    if not isinstance(x, str): return x
    try: return json.loads(x)
    except Exception:
        try: return ast.literal_eval(x)
        except Exception: return ast.literal_eval(re.sub(r",\s*([\]\}])", r"\1", x))

def _clean_points(pts):
    m = {}
    for a, b in pts:
        a, b = float(a), float(b)
        m[a] = max(m.get(a, -1e18), b)
    return sorted(m.items())

def _mfs(s):
    d = _loads(s)
    if isinstance(d, dict): d = next(iter(d.values()))
    return {str(t["id"]): _clean_points(t["points"]) for t in d}

def _mu(pts, x):
    x = float(x)
    if x <= pts[0][0]: return pts[0][1]
    if x >= pts[-1][0]: return pts[-1][1]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        if x1 <= x <= x2:
            if x2 == x1: return max(y1, y2)
            return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
    return 0.0

def _leftmost_ge(pts, a):
    if a <= 0: return pts[0][0]
    if pts[0][1] >= a: return pts[0][0]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        if y1 >= a: return x1
        if y1 < a <= y2 and y2 != y1:
            return x1 + (a - y1) * (x2 - x1) / (y2 - y1)
    return pts[-1][0] if pts[-1][1] >= a else None

def main(temp_mf_json: str, heat_mf_json: str, rules_json: str, t: float) -> float:
    T = _mfs(temp_mf_json)
    S = _mfs(heat_mf_json)
    rules = _loads(rules_json)

    syn_in = {"нормально": "комфортно"}
    syn_out = {"слабо": "слабый", "умеренно": "умеренный", "интенсивно": "интенсивный"}

    mu_t = {k: _mu(v, t) for k, v in T.items()}
    smin = min(p[0] for pts in S.values() for p in pts)

    best = []
    max_mu = 0.0
    for a, b in rules:
        a, b = str(a), str(b)
        a = syn_in.get(a, a)
        b = syn_out.get(b, b)
        if a not in mu_t or b not in S:
            continue
        alpha = float(mu_t[a])
        h = max(y for _, y in S[b])
        beta = alpha if alpha < h else h
        if beta > max_mu + 1e-12:
            max_mu = beta
            best = [(beta, S[b])]
        elif abs(beta - max_mu) <= 1e-12:
            best.append((beta, S[b]))

    if max_mu <= 0 or not best:
        return float(smin)

    xs = []
    for _, pts in best:
        x = _leftmost_ge(pts, max_mu)
        if x is not None:
            xs.append(x)
    return float(min(xs) if xs else smin)


if __name__ == "__main__":
    with open("json_data/функции-принадлежности-температуры.json", encoding="utf-8") as f:
        t_mf = f.read()
    with open("json_data/функции-принадлежности-управление.json", encoding="utf-8") as f:
        h_mf = f.read()
    with open("json_data/функция-отображения.json", encoding="utf-8") as f:
        rules = f.read()

    print(main(t_mf, h_mf, rules, 19))

import csv


def main():
    path = "task0.csv"
    adj = {}
    with open(path, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            u, v = row
            if u not in adj:
                adj[u] = []
            if v not in adj:
                adj[v] = []
            adj[u].append(v)
            adj[v].append(u)

    table = []
    for node in sorted(adj.keys(), key=int):
        table.append([node] + sorted(adj[node], key=int))

    for row in table:
        print(row)


if __name__ == "__main__":
    main()
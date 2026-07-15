import json
from fractions import Fraction

def solve(filename):
    with open(filename) as f:
        data = json.load(f)

    keys = data['keys']
    n = keys['n']
    k = keys['k']

    points = []
    for key, value in data.items():
        if key == 'keys':
            continue
        x = int(key)
        base = int(value['base'])
        y = int(value['value'], base)
        points.append((x, y))
    
    points.sort()
    selected = points[:k]

    secret = Fraction(0)
    for i in range(k):
        xi, yi = selected[i]
        term = Fraction(yi)
        for j in range(k):
            if i == j:
                continue
            xj, _ = selected[j]
            term *= Fraction(-xj, xi - xj)
        secret += term

    print(f"{filename}: {secret}")

solve("test_case_1.json")
solve("test_case_2.json")

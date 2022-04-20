import csv
import os
from collections import Counter

ct = Counter()
other_ct = Counter()

for YEAR in [2021, 2022]:

    dir = f'data/{YEAR}/extracted'

    for file in os.listdir(dir):
        filename = f"{dir}/{file}"

        reader = csv.DictReader(open(filename))

        for row in reader:
            voted_by_proxy = row["Voted"].replace("(", "").replace(")", "").strip()
            if 'Lawson' in voted_by_proxy:
                other_ct.update(row.keys())
            ct.update([voted_by_proxy])

with open('data/count_of_proxies.csv', 'w') as f:
    c = csv.writer(f)
    c.writerow(['Proxy', 'Count'])

    for proxy, cou in ct.items():
        c.writerow([proxy, cou])

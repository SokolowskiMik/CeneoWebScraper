import os
import json

files = os.listdir('app/static/stats')
product_opinion_list = []
for f in files:
    with open(f"app/static/stats/{f}", 'r', encoding='utf-8') as jsf:
        js = json.load(jsf)
    product_opinion_list.append((f.split('.')[0],js))

print(product_opinion_list)
print()
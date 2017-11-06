# -*- coding: utf-8 -*-
import json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime
import sys

mpl.style.use('seaborn-poster')

if len(sys.argv) != 2:
    print('usage: python mileage_chart.py mileage_json', file=sys.stderr)
    sys.exit(1)

datfn = sys.argv[1]
pngfn = datfn[0:datfn.rindex('.')] + '.png'

with open(datfn) as f:
    miledata = json.loads(f.read())

monmile = dict()

for d in miledata:
    dt = datetime.datetime.strptime(d, '%Y-%m-%d')
    dt = dt.replace(day = 1)
    if not dt in monmile: monmile[dt] = 0.0
    monmile[dt] = monmile[dt] + miledata[d]

x = sorted(monmile.keys())
y = list(map(lambda dt: monmile[dt], x))
nmons = 3.0
y2 = np.convolve(y, np.ones(nmons)/nmons, mode='valid')

width=31

fig, ax = plt.subplots()
ax.bar(x, y, width, color='#95d0fc', alpha=0.5, label='月間走行距離')
ax.plot(x[2:], y2, color='#0343df', label='移動平均(3ヵ月)')
ax.set_ylabel("月間走行距離(km)")

ax.legend(loc=0)

ax.grid()

fig.set_size_inches(16.0, 6.0)
fig.savefig(pngfn)
#plt.show()

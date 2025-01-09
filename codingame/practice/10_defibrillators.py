'''

https://www.codingame.com/training/easy/defibrillators

'''

import math


class Defib:
    def __init__(self, data):
        
        t = data.split(';')
        
        self.idd = t[0]
        self.name = t[1]
        self.address = t[2]
        self.phone = t[3]
        self.lon = float(t[4].replace(',', '.'))
        self.lat = float(t[5].replace(',', '.'))
        
    def set_dist(self, dis):
        self.dis = dis


lon = float(input().replace(',', '.'))
lat = float(input().replace(',', '.'))
n = int(input())

defibs = []
for i in range(n):
    defib = Defib(input())

    x = (defib.lon - lon) * math.cos((defib.lat + lat) / 2)
    y = (defib.lat - lat)
    d = math.sqrt(x*x + y*y) * 6371
    
    defib.set_dist(d)
    defibs.append(defib)

min_dis = math.inf
for defib in defibs:
    if defib.dis < min_dis:
        min_dis = defib.dis
        min_name = defib.name

print(min_name)

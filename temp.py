import json
import math
from pathlib import Path

def f(a,b):
    return a/b

prod = 1
max_p = 0.99999
n = 50
for i in range(n):

    prod *= (365-i)/365

print(1-prod)
print(i)

a = 1
b = -1
c = -506

d = b**2 - a*4*c
print(-b/(2*a) + math.sqrt(d)/(2*a))

print(1-(364/365)**50)
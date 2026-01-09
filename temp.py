import json
import math
from pathlib import Path

def f(a,b):
    return a/b

prod = 1
max_p = 0.9999
n = 1000
for i in range(n):
    prod *= (365-i)/365
    if (1-prod)>max_p:
        print(i)
        break
print(i)
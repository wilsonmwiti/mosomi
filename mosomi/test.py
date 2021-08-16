from math import floor
from string import ascii_lowercase
from django.template.defaultfilters import upper

n = 701
m = 702
i = 0
row = floor(n/m)
max_column = 0
if row > 0:
    max_column = row * 702
else:
    max_column += 702

b = 0
while n > 702:
    n -= 702
else:
    b = n

column = b
test_list = []
L = list(ascii_lowercase) + [letter1+letter2 for letter1 in ascii_lowercase for letter2 in ascii_lowercase]
print(row + 1, upper(L[column - 1]))
print(len(L))
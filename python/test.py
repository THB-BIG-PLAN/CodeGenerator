import itertools

set1 = {1, 2}
set2 = {1, 2}
set3 = {1, 2}
set4 = {1, 2}
set5 = {9, 10}
set6 = {11, 12}
set7 = {13, 14}
set8 = {15, 16}
set9 = {17, 18}

sets = [set1, set2, set3, set4, set5, set6, set7, set8, set9]

cartesian_product = list(itertools.product(*sets))

print(cartesian_product)
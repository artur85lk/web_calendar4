words = input().split()
tab = []
conter = -1
for i in words:
    conter += 1
    if conter == 0:
        tab.append(i)
    else:
        tab.append(i.capitalize())
    conter += 1
print("".join(tab))

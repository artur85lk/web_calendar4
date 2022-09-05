number = input().split()
what_size = len(number)
counter = 0
for i in number:
    if i == "A":
        counter += 1
procent = 1 / what_size * counter
print(round(procent, 2))

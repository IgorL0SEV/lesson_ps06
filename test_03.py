data = [
    [100, 110, 320],
    [400, 500, 600],
    [150, 230, 140]
]

list = []

for row in data:
    for item in row:
        if item > 190:
            list.append(item)



print(list)

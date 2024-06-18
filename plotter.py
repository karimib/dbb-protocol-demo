import csv

import matplotlib.pyplot as plt

data = []
x = [i for i in range(10000)]

with open('output.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    # Write each row in the list to the file
    for row in reader:
        data.append(int(row[0]))

plt.plot(x, data)
plt.show()
import matplotlib.pyplot as plt
import csv

x=[]
y=[]

with open('telemetry-2021-06-20-08.csv', 'r') as csvfile:
    plots= csv.reader(csvfile, delimiter=',')
    for row in plots:
        xNum = float(row[41])
        yNum = float(row[42])
        if(xNum < 1 and yNum < 1):
            x.append(yNum)
            y.append(xNum)


plt.plot(x,y, marker='o', label='')

plt.title('Data from the CSV File: People and Expenses')

plt.xlabel('Number of People')
plt.ylabel('Expenses')
print(x)
plt.show()
import matplotlib.pyplot as plt
import csv

x=[]
y=[]
fig = plt.figure()
ax = fig.add_subplot(111)

with open('bno1-5.csv', 'r') as csvfile:
    plots= csv.reader(csvfile, delimiter=',')
    i = 0
    for row in plots:
        yNum = float(row[10])
        xNum = float(row[11])
        if(xNum < 1 and yNum < 1):
            x.append(xNum)
            y.append(yNum)
        i = i + 1
        if i % 4 == 0:
            plt.plot(x,y, marker='o', label=i)
            for xy in zip(x, y):                                       # <--
                ax.annotate('(%s, %s)' % xy, xy=xy, textcoords='data') # <--

            x = []
            y = []




plt.title('Data from the CSV File: bno1-5')

plt.xlabel('Column 10 - z')
plt.ylabel('Column 11 - y')
print(x)
plt.grid()
plt.show()
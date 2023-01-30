import matplotlib.pyplot as plt

origin = (0, 0)
destinations = [(100, 100, 5), (200, 200, 8), (300, 300, 12)] 
deliveries = calculate_deliveries(destinations, 6)

x = [origin[0]]
y = [origin[1]]
colors = ['red']
for delivery in deliveries:
    x.append(delivery[0])
    y.append(delivery[1])
    x.append(origin[0])
    y.append(origin[1])
    colors.append('blue')
    colors.append('red')

plt.scatter(x, y, c=colors)
plt.show()

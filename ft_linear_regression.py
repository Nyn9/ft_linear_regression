import matplotlib.pyplot as plt

theta0 = 0
theta1 = 0
learningRate = 0.0001

def estimatePrice(mileage):
	return theta0 + (mileage * theta1)

for epoch in range(500001):
	m = 0
	sumtheta0 = 0
	sumtheta1 = 0
	with open('data.csv') as file:
		next(file)
		for line in file:
			split = line.strip().split(',')
			if not split or len(split) < 2:
				continue
			m += 1
			km = int(split[0]) / 1000
			price = int(split[1])
			sumtheta0 += estimatePrice(km) - price
			sumtheta1 += (estimatePrice(km) - price) * km
	theta0 -= learningRate * 1/m * sumtheta0
	theta1 -= learningRate * 1/m * sumtheta1
	if epoch % 100 == 0:
		print(f"Epoch {epoch}: theta0 = {theta0}, theta1 = {theta1}")

with open('theta', 'w') as file:
	file.write(f"{theta0},{theta1}")

x = []
y = []

with open('data.csv') as file:
	next(file)
	for line in file:
		line = line.strip().split(',')
		if not line or len(line) < 2:
			continue
		x.append(int(line[0]) / 1000)
		y.append(int(line[1]))

predicted_prices = [estimatePrice(km) for km in x]
plt.scatter(x, y, color='blue', label='Données réelles')
plt.plot(x, predicted_prices, color='red', label='Régression linéaire')
plt.xlabel('Kilométrage (en milliers de km)')
plt.ylabel('Prix (en euros)')
plt.title('Régression linéaire du prix en fonction du kilométrage')
plt.show()
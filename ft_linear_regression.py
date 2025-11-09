import pandas as pd
import matplotlib.pyplot as plt


theta0 = 0
theta1 = 0


def load_file(filename: str) -> pd.DataFrame:
	"""Load a CSV file into a pandas DataFrame."""
	try:
		file = pd.read_csv(filename)

		m = file['km']
		p = file['price']

		if len(m) != len(p) or len(m) == 0:
			raise ValueError("Invalid file format: 'km' and 'price' columns must have the same non-zero length.")

		return file
	except Exception as e:
		print(f"Error loading file: {e}")
		return None


def estimate_price(mileage) :
	"""Estimate price with the mileage"""

	print(theta0, theta1)
	return (theta0 + theta1 * mileage)


def linear_regression(file: pd.DataFrame) -> None:
	"""Calculate linear regression"""
	global theta0, theta1
	learning_rate = 0.000001

	if file is None:
		return

	mileage = file['km']
	price = file['price']


	m = len(price)

	# for i in range(m):
	# 	print(mileage[i], price[i])

	for epoch in range(2):
		sumT0 = sum(estimate_price(mileage[i]) - price[i] for i in range(m))
		sumT1 = sum((estimate_price(mileage[i]) - price[i]) * mileage[i] for i in range(m))

		print("------------")

		# print(f"Epoch {epoch}: theta0 = {theta0}, theta1 = {theta1}, sumT0 = {sumT0}, sumT1 = {sumT1}")
		theta0 -= learning_rate * (sumT0 / m)
		theta1 -= learning_rate * (sumT1 / m)


def draw_data(file: pd.DataFrame) -> None:
	"""Draw the data and the linear regression line"""
	if file is None:
		return

	mileage = file['km']
	price = file['price']

	plt.scatter(mileage, price, color='blue', label='Data points')
	plt.plot(mileage, estimate_price(mileage), color='red', label='Regression line')
	plt.xlabel('Mileage (km)')
	plt.ylabel('Price ($)')
	plt.title('Linear Regression: Price vs Mileage')
	plt.legend()
	if plt.get_backend().lower().startswith('agg'):
		out = 'regression.png'
		plt.savefig(out, dpi=150, bbox_inches='tight')
		print(f"Plot saved to {out}")
	else:
		plt.show()
	plt.close()


def main():
	file = load_file('data.csv')
	linear_regression(file)
	print(f"theta0: {theta0}, theta1: {theta1}")
	# draw_data(file)


if __name__ == "__main__":
	main()
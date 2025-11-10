import pandas as pd
import argparse
import os
import matplotlib.pyplot as plt


theta0 = 0
theta1 = 0
rmse_tab = []
parser = argparse.ArgumentParser()


def get_real_theta(file) -> tuple[float, float]:
	km_max, km_min = file['km'].max(), file['km'].min()
	p_max, p_min = file['price'].max(), file['price'].min()

	theta1_real = theta1 / (km_max - km_min) * (p_max - p_min)
	theta0_real = theta0 * (p_max - p_min) + p_min - theta1_real * km_min
	print(f"Theta0 : {theta0_real} / Theta1 : {theta1_real}")
	return theta0_real, theta1_real


def load_file(filename: str) -> pd.DataFrame | None:
	"""Load a CSV file into a pandas DataFrame."""
	try:
		file = pd.read_csv(filename)

		m = file['km']
		p = file['price']

		if len(m) != len(p) or len(m) == 0:
			raise ValueError("Invalid file format: 'km' and 'price' columns must have the same non-zero length.")

		if any(not str(x).isdigit() for x in p):
			raise ValueError("At least one value is not a positive number")

		return file
	except Exception as e:
		print(f"Error loading file: {e}")
		return None


def estimate_price(mileage):
	"""Estimate price with the mileage"""
	return theta0 + (theta1 * mileage)


def linear_regression(file: pd.DataFrame) -> None:
	"""Calculate linear regression"""
	global theta0, theta1
	learning_rate = 0.1
	last_cost = float('inf')
	args = parser.parse_args()

	mil_min, mil_max = file['km'].min(), file['km'].max()
	price_min, price_max = file['price'].min(), file['price'].max()

	mil = (file['km'] - mil_min) / (mil_max - mil_min)
	price = (file['price'] - price_min) / (price_max - price_min)

	m = len(price)

	for epoch in range(500000):
		sumT0 = sum(estimate_price(mil[i]) - price[i] for i in range(m))
		sumT1 = sum((estimate_price(mil[i]) - price[i]) * mil[i] for i in range(m))

		theta0 -= learning_rate * (sumT0 / m)
		theta1 -= learning_rate * (sumT1 / m)

		p_real = estimate_price(mil) * (price_max - price_min) + price_min
		rmse = ((sum((p_real - file['price'])**2) / m))**0.5
		rmse_tab.append(rmse)

		cost = sum((estimate_price(mil[i]) - price[i])**2 for i in range(m)) / (2*m)

		if args.verbose:
			print(f"Epoch {epoch} :")
			get_real_theta(file)
			print(f"RMSE : {rmse}")
			print("------------")

		if last_cost - cost < 1e-9:
			print(f"Number of epochs : {epoch}")
			break
		last_cost = cost

	print(f"RMSE = {rmse}")


def draw_data(file: pd.DataFrame) -> None:
	"""Draw the data and the linear regression line"""
	args = parser.parse_args()
	m = file['km']
	p = file['price']

	m_max, m_min = m.max(), m.min()
	p_max, p_min = p.max(), p.min()

	m_norm = (file['km'] - m_min) / (m_max - m_min)

	real_estimate_price = p_min + estimate_price(m_norm) * (p_max - p_min)

	plt.scatter(m, p, color='blue', label='Data points')
	plt.plot(m, real_estimate_price, color='red', label='Regression line')
	plt.xlabel('Mileage (km)')
	plt.ylabel('Price ($)')
	plt.title('Linear Regression: Price vs Mileage')
	plt.legend()
	if not plt.get_backend().lower().startswith('agg'):
		try:
			plt.show()
		except KeyboardInterrupt:
			plt.close()
	if args.save:
		out = 'graph/regression.png'
		if not os.path.exists("graph"):
			os.makedirs("graph")
		plt.savefig(out, dpi=150, bbox_inches='tight')
		print(f"Graph saved to {out}")
	plt.close()


def draw_rmse() -> None:
	"""Draw the Root Mean Square Error graph"""
	args = parser.parse_args()
	plt.plot(rmse_tab)
	plt.xlabel("Epoch")
	plt.ylabel("RMSE ($)")
	if not plt.get_backend().lower().startswith('agg'):
		try:
			plt.show()
		except KeyboardInterrupt:
			plt.close()
	if args.save:
		out = 'graph/rmse.png'
		if not os.path.exists("graph"):
			os.makedirs("graph")
		plt.savefig(out, dpi=150, bbox_inches='tight')
		print(f"Graph saved to {out}")
	plt.close()


def stock_values(file) -> None:
	"""Store theta values in 'theta' file."""

	theta0_real, theta1_real = get_real_theta(file)

	try:
		data = {
			'theta0': theta0_real,
			'theta1': theta1_real
		}
		f = pd.Series(data)
		f.to_json('data/theta.json')
	except Exception as e:
		print(f"Error saving theta values: {e}")


def set_args():
	parser.add_argument("-v", "--verbose", action="store_true", help="Show the detailled information")
	parser.add_argument("-g", "--graph", type=str, choices=["d", "r", "rd", "dr"], help="Show the choosen graph")
	parser.add_argument("-s", "--save", action="store_true", help="Save the choosen graph")


def main():
	set_args()
	args = parser.parse_args()
	file = load_file('data/data.csv')
	if file is None:
		return
	linear_regression(file)
	stock_values(file)
	if args.graph and 'd' in args.graph:
		draw_data(file)
	if args.graph and 'r' in args.graph:
		draw_rmse()


if __name__ == "__main__":
	main()

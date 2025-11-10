import pandas as pd


def estimatePrice(mileage: int, theta0: float, theta1: float) -> float:
	"""Estimate price with the mileage"""
	return theta0 + (mileage * theta1)


def load_theta() -> tuple[float, float]:
	"""Load theta values from the 'theta' file."""
	try:
		data = pd.read_json('data/theta.json', typ='series')
		theta0 = float(data['theta0'])
		theta1 = float(data['theta1'])
		print(f"Loaded theta values: theta0 = {theta0}, theta1 = {theta1}")
		return theta0, theta1
	except Exception as e:
		print(f"Error loading theta values: {e}")
		print("Using default theta values of 0.0.")
		return 0.0, 0.0


def main():
	theta0, theta1 = load_theta()
	while True:
		try:
			mileage = input("Entrez le kilométrage ou 'exit' pour quitter : ")
			if mileage.lower() == 'exit':
				break
			mileage = int(mileage)
			if mileage < 0:
				print("Le kilométrage ne peut pas être négatif.")
				continue
		except ValueError:
			print("Veuillez entrer un nombre valide.")
			continue
		except EOFError:
			print("\nFin de l'entrée.")
			return
		price = estimatePrice(mileage, theta0, theta1)
		print(f"Le prix estimé pour {mileage} km est : {price}")


if __name__ == "__main__":
	main()

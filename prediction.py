def estimatePrice(mileage):
	with open('theta', 'r') as file:
		theta = file.readline().strip().split(',')
		theta0 = float(theta[0])
		theta1 = float(theta[1])
	return theta0 + (mileage * theta1)

while True:
	try:
		mileage = input("Entrez le kilométrage (en km) ou 'exit' pour quitter : ")
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
		break
	price = estimatePrice(mileage / 1000)
	print(f"Le prix estimé pour {mileage} km est : {price}")
# Check if input is valid number, make int to float by adding .0 or check if entered string is correct float
def manageInput(number):
	if number.count(",") > 1 or not number.replace(",","",1).isdigit():
			return -1.1
	return float(number.replace(",",".",1))

print("Started Typer")

#Guess if i want comma separated numbers, I have to enter String, then convert comma to dot
while True:
	values = []
	basics = []
	print("Enter your numbers and \"finished\" to end")

	number = input("")
	while number not in ["f","fi","finished", "finish"]:
		if number in ["e","exit"]:
			exit()
		if manageInput(number) != -1.1:
			basics.append(manageInput(number))
			values.append(round(manageInput(number)*1.1,2))
		else:
			print("No valid value!")
		number = input("")
	print("\nOld Value -> Value * 1,1")
	for i in range(len(basics)):
		print(str(basics[i])+ ((8-len(str(basics[i])))*" ")+"->   "+str(values[i]))
	print("")
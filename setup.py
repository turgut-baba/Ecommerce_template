import json

with open('aspects.json') as json_file:
	data = json.load(json_file)

	name_index = 0

	with open('Ecommerce_Template/settings.py', 'r') as settings:
		read_data = settings.readlines()

		for line in settings:
			name_index += 1
			if line == 'STORE_NAME = ""':
				break

	read_data[name_index] = 'STORE_NAME = "' + data['Store name'] + '"'

	with open('Ecommerce_Template/settings.py', 'w') as settings:
		settings.writelines(read_data)


for i in range(2):
	print("Hi")
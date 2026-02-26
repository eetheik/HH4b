import json

with open("nanoindex_v15_scouting.json","r") as file:
	jsonData = json.load(file)

count_dict = {}

for years, overall_signal_cat in jsonData.items():
	count_dict[years] = {}
	for cat, subcats in overall_signal_cat.items():
		count_dict[years][cat] = {}
		for subcat, lists in subcats.items():
			count_dict[years][cat][subcat] = len(lists)

with open("output.json", "w") as outputFile:
    json.dump(count_dict, outputFile, indent = 4)

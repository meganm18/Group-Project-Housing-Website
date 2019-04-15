# code taken from https://www.youtube.com/watch?v=Uze9SEeETA0


import csv, json
csvFilePath = "apartment_data.csv"
jsonFilePath = "apartment_data.json"


data = {}
with open(csvFilePath) as csvFile:
    csvReader = csv.DictReader(csvFile)
    for csvRow in csvReader:
        apartment_name = csvRow['Apartment Name']
        data[apartment_name] = csvRow


with open(jsonFilePath, "w") as jsonFile:
    jsonFile.write(json.dumps(data,indent=4))


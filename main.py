import requests
import pprint as pp
import csv
link = "https://new.moykassir.ru/api/nomenclature?page=1&limit=50&include_nested_categories=true"

headers = {
    #'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvbmV3Lm1veWthc3Npci5ydVwvYXBpXC9hdXRoXC9yZWZyZXNoIiwiaWF0IjoxNzA5MDI1NTIyLCJleHAiOjE3MDkwMzY0NzYsIm5iZiI6MTcwOTAzMjg3NiwianRpIjoick9ubmF6OGl5U1hIVDVaaCIsInN1YiI6MzQ2MTUsInBydiI6IjIzYmQ1Yzg5NDlmNjAwYWRiMzllNzAxYzQwMDg3MmRiN2E1OTc2ZjciLCJlbWFpbCI6Im1tdkBobGNvbXBhbnkucnUifQ.f5MFX_9CQ_w8k9XqN8KfL33UE3Ff6viVORPfHHSTQvU'
}

headlines = ['TYPE','NUM', 'PARENT_CODE', 'NAME', 'MEASURE_UNIT', 'UNIT_WEIGHT', 'ENERGY', 'FIBER', 'FAT', 'CARBOHYDRATE', 'PRICE', 'CATEGORY']
n = 0
response = requests.get(link, headers=headers)
nomenclature = response.json()
print(response)
resultNum = [#{'type': '',
#               'NUM': '',
#               'PARENT_CODE': '',
#               'NAME': '',
#               'MEASURE_UNIT': '',
#               'UNIT_WEIGHT': '',
#               'ENERGY': '',
#               'FIBER': '',
#               'FAT': '',
#               'CARBOHYDRATE': '',
#               'PRICE': '',
#               'CATEGORY': ''
                 ]

print(resultNum)


def AppendGoods(resultNum, numenlature):
    i = 0
    for i in range(0, len(numenlature['items'])):
        # #resultNum[i]['type'] = "Goods"
        # resultNum[i]['NUM'] = numenlature['items'][i]['id']
        # resultNum[i]['PARENT_CODE'] = numenlature['items'][i]['category_id']
        # resultNum[i]['NAME'] = numenlature['items'][i]['name']
        # resultNum[i]['MEASURE_UNIT'] = numenlature['items'][i]['uom']['name']
        # resultNum[i]['UNIT_WEIGHT'] = numenlature['items'][i]['weight_gram']
        # resultNum[i]['ENERGY'] = ""
        # resultNum[i]['FIBER'] = ""
        # resultNum[i]['FAT'] = numenlature['items'][i]['fats']
        # resultNum[i]['CARBOHYDRATE'] = numenlature['items'][i]['carbohydrates']
        # resultNum[i]['PRICE'] = numenlature['items'][i]['price']
        # resultNum[i]['CATEGORY'] = numenlature['items'][i]['category']['name']
        resultNum.append({'TYPE': 'Goods',
                          'NUM': numenlature['items'][i]['id'],
                          'PARENT_CODE': numenlature['items'][i]['category_id'],
                          'NAME': numenlature['items'][i]['name'],
                          'MEASURE_UNIT': numenlature['items'][i]['uom']['name'],
                          'UNIT_WEIGHT': numenlature['items'][i]['weight_gram'],
                          'ENERGY': '',
                          'FIBER': '',
                          'FAT': numenlature['items'][i]['fats'],
                          'CARBOHYDRATE': numenlature['items'][i]['carbohydrates'],
                          'PRICE': numenlature['items'][i]['price'],
                          'CATEGORY': numenlature['items'][i]['category']['name']})

    return resultNum


resultNum = AppendGoods(resultNum, nomenclature)
for i in resultNum:
    print(i)
print(len(resultNum))
print(len(nomenclature['items']))
print("TEST ______________________")
print(nomenclature['items'][1]['name'])

with open ("nomenclature.csv", 'w', encoding='utf-8') as file:
    file_writer = csv.writer(file, delimiter=";", lineterminator="\r")
    file_writer.writerow(headlines)
    for i in resultNum:
        file_writer.writerow(i.values())
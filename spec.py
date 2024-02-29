import requests
import pprint as pp
import csv

def GetRequest(link, headers):
    response = requests.get(link, headers=headers)
    print(response)
    return response

headlines = ['PRODUCT_CODE', 'ITEM_CODE', 'ITEM_GROSS_WEIGHT', 'ITEM_NET_WEIGHT', 'ITEM_OUT_WEIGHT', 'TECHNOLOGY',
             'AMOUNT', 'DATE_FROM', 'WRITEOFF_TYPE']

headersSpec = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvbmV3Lm1veWthc3Npci5ydVwvYXBpXC9hdXRoXC9yZWZyZXNoIiwiaWF0IjoxNzA5MTAwMjk1LCJleHAiOjE3MDkxMTkyNTIsIm5iZiI6MTcwOTExNTY1MiwianRpIjoiZEYwZ0M1eTZUQUE5M3RnbCIsInN1YiI6MzQ2MTUsInBydiI6IjIzYmQ1Yzg5NDlmNjAwYWRiMzllNzAxYzQwMDg3MmRiN2E1OTc2ZjciLCJlbWFpbCI6Im1tdkBobGNvbXBhbnkucnUifQ.Jfht7l3ZjypN6NS8ebgQp_YxymS06DS7_FPziHA_91g'
}

def writeFile(resultSpec, headlines):
    with open('specification.csv', 'w', encoding='utf-8') as file:
        file_writer = csv.writer(file, delimiter=";", lineterminator="\r")
        file_writer.writerow(headlines)
        for row in resultSpec:
            file_writer.writerow(row.values())


with open('help.txt', 'r', encoding='utf-8') as file:
    k = file.read().splitlines()
    resultSpec = []
    for i in range(0, len(k)):
        linkSpec = "https://new.moykassir.ru/api/nomenclature/ingredients/" + k[i]
        print(i, " ", len(k))
        Spec = GetRequest(linkSpec, headersSpec).json()
        for j in range(0, len(Spec['consists']['ingredients'])):
            if Spec['consists']['ingredients'][j]['weightOnBase'] is None or Spec['consists']['ingredients'][j]['weightOneOnBase'] is None:
                Weight = None
            else:
                Weight = Spec['consists']['ingredients'][j]['weightOnBase'] / Spec['consists']['ingredients'][j]['weightOneOnBase']
            resultSpec.append({'PRODUCT_CODE': Spec['consists']['nomId'],
                               'ITEM_CODE': Spec['consists']['ingredients'][j]['nom_id'],
                               'ITEM_GROSS_WEIGHT': '',
                               'ITEM_NET_WEIGHT': Spec['consists']['ingredients'][j]['amount'],
                               'ITEM_OUT_WEIGHT': Weight,
                               'TECHNOLOGY': Spec['consists']['technology'],
                               'AMOUNT': '',
                               'DATE_FROM': Spec['consists']['date_from'],
                               'WRITEOFF_TYPE': ''})
            writeFile(resultSpec, headlines)

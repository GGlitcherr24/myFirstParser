import requests
import pprint as pp
import csv


def GetRequest(link, headers):
    response = requests.get(link, headers=headers)
    print(response)
    return response


def AppendSpec(resultSpec, Spec):
    for i in range(0, len(Spec['items'])):

        print(i)
    return resultSpec


headlines = ['PRODUCT_CODE', 'ITEM_CODE', 'ITEM_GROSS_WEIGHT', 'ITEM_NET_WEIGHT', 'ITEM_OUT_WEIGHT', 'TECHNOLOGY',
             'AMOUNT', 'DATE_FROM', 'WRITEOFF_TYPE']

headersSpec = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvbmV3Lm1veWthc3Npci5ydVwvYXBpXC9hdXRoXC9yZWZyZXNoIiwiaWF0IjoxNzA5MTAwMjk1LCJleHAiOjE3MDkxMTQzNDQsIm5iZiI6MTcwOTExMDc0NCwianRpIjoibG5DUXJMbEdqNEs2dG1NUSIsInN1YiI6MzQ2MTUsInBydiI6IjIzYmQ1Yzg5NDlmNjAwYWRiMzllNzAxYzQwMDg3MmRiN2E1OTc2ZjciLCJlbWFpbCI6Im1tdkBobGNvbXBhbnkucnUifQ.MsHPqUu5Ko-z07cJ1cH5YrHusfurY68ane50HmcKFWM'
}

count = 0


def writeFile(resultSpec, headlines):
    with open('specification.csv', 'w', encoding='utf-8') as file:
        file_writer = csv.writer(file, delimiter=";", lineterminator="\r")
        file_writer.writerow(headlines)
        for i in resultSpec:
            file_writer.writerow(i.values())


with open('help.txt', 'r', encoding='utf-8') as file:
    k = file.readlines()
    resultSpec = []
    for i in range(0, len(k)):
        linkSpec = 'https://new.moykassir.ru/api/nomenclature/ingredients/' + str(k[i])
        Spec = GetRequest(linkSpec, headersSpec).json()
        print(Spec['consist'])
        for j in range(0, len(Spec['ingredients'])):
            Weight = Spec['consist']['ingredients'][j]['weightOnBase'] / Spec['consist']['ingredients'][j]['weightOneOnBase']
            resultSpec.append({'PRODUCT_CODE': Spec['consist']['nomId'],
                               'ITEM_CODE': Spec['consist']['ingredients'][j]['nom_id'],
                               'ITEM_GROSS_WEIGHT': Spec['consist']['ingredients'][j],
                               'ITEM_NET_WEIGHT': Spec['consist']['ingredients'][j]['amount'],
                               'ITEM_OUT_WEIGHT': Spec['consist']['ingredients'][j]['weightOnBase'] / Weight,
                               'TECHNOLOGY': Spec['consist']['technology'],
                               'AMOUNT': '',
                               'DATE_FROM': Spec['consist']['date_from'],
                               'WRITEOFF_TYPE': ''})
    writeFile(resultSpec, headlines)


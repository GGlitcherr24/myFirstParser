import requests
import pprint as pp
import csv

def GetRequest(link, headers):
    response = requests.get(link, headers=headers)
    print(response)
    return response

headers = {
    'Authorization': ''
}
headlines = ['PRODUCT_CODE', 'ITEM_CODE', 'ITEM_GROSS_WEIGHT', 'ITEM_NET_WEIGHT', 'ITEM_OUT_WEIGHT', 'TECHNOLOGY',
             'AMOUNT', 'DATE_FROM', 'WRITEOFF_TYPE']

def writeFile(resultSpec, headlines):
    with open('specification2.csv', 'w', encoding='utf-8') as file:
        file_writer = csv.writer(file, delimiter=";", lineterminator="\r")
        file_writer.writerow(headlines)
        for row in resultSpec:
            file_writer.writerow(row.values())

def GetArticles():
    with open('helpSpec.txt', 'r', encoding='utf-8') as file:
        k = file.read().splitlines()
        resultSpec = []
        resultSpec = AppendSpec(resultSpec,k)

def AppendSpec(resultSpec, k):
    for i in range(0, len(k)):
        linkSpec = "https://new.moykassir.ru/api/nomenclature/ingredients/" + k[i]
        print(i, " ", len(k))
        Spec = GetRequest(linkSpec, headers).json()
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

def main(header):
    headers['Authorization'] = header
    GetArticles()
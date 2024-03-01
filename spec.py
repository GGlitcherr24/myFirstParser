import requests
import pprint as pp
import csv


# Получаем запрос
def GetRequest(link, headers):
    response = requests.get(link, headers=headers)
    return response


# токен авторизации
headers = {
    'Authorization': ''
}
# Заголовки файла
headlines = ['PRODUCT_CODE', 'ITEM_CODE', 'ITEM_GROSS_WEIGHT', 'ITEM_NET_WEIGHT', 'ITEM_OUT_WEIGHT', 'TECHNOLOGY',
             'AMOUNT', 'DATE_FROM', 'WRITEOFF_TYPE']


# Запись файла
def writeFile(resultSpec, headlines):
    with open('specification.csv', 'w', encoding='utf-8') as file:
        file_writer = csv.writer(file, delimiter=";", lineterminator="\n")
        file_writer.writerow(headlines)
        for row in resultSpec:
            file_writer.writerow(row.values())


# Берем id из вспомогающего файла, созданного при выгрузке номенклатуры
def GetArticles():
    with open('helpSpec.txt', 'r', encoding='utf-8') as file:
        k = file.read().splitlines()
        resultSpec = []
        resultSpec = AppendSpec(resultSpec, k)


# Заполняем словарь данными из запроса
def AppendSpec(resultSpec, k):
    for i in range(0, len(k)):
        linkSpec = "https://new.moykassir.ru/api/nomenclature/ingredients/" + k[i]
        Spec = GetRequest(linkSpec, headers).json()
        Date = Spec['consists']['date_from']
        Date = Date[:-6]
        for j in range(0, len(Spec['consists']['ingredients'])):
            if Spec['consists']['ingredients'][j]['weightOnBase'] is None or Spec['consists']['ingredients'][j][
                'weightOneOnBase'] is None:
                Weight = None
            else:
                Weight = Spec['consists']['ingredients'][j]['weightOnBase'] / Spec['consists']['ingredients'][j][
                    'weightOneOnBase']
            if Spec['consists']['technology'] == None:
                Tech = ''
            else:
                Tech = Spec['consists']['technology'].replace('\n', '')
            resultSpec.append({'PRODUCT_CODE': Spec['consists']['nomId'],
                               'ITEM_CODE': Spec['consists']['ingredients'][j]['nom_id'],
                               'ITEM_GROSS_WEIGHT': '',
                               'ITEM_NET_WEIGHT': Spec['consists']['ingredients'][j]['amount'],
                               'ITEM_OUT_WEIGHT': Weight,
                               'TECHNOLOGY': Tech,
                               'AMOUNT': '',
                               'DATE_FROM': Date,
                               'WRITEOFF_TYPE': ''})
            writeFile(resultSpec, headlines)


def main(header):
    headers['Authorization'] = header
    print("Подготовка файла спецификации")
    GetArticles()

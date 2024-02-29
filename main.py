import requests
import pprint as pp
import csv
import sys

headers = {
    'Authorization': ''
}
headlines = ['TYPE', 'NUM', 'PARENT_CODE', 'NAME', 'MEASURE_UNIT', 'UNIT_WEIGHT', 'ENERGY', 'FIBER', 'FAT', 'CARBOHYDRATE', 'PRICE', 'CATEGORY']

def GetRequest(link, headers):
    response = requests.get(link, headers=headers)
    print(response)
    return response.json()

def main():
    resultNom, resultCat = [], []
    i = 1
    while True:
        link = "https://new.moykassir.ru/api/nomenclature?page=" + str(i) + "&limit=50&include_nested_categories=true"
        nomenclatureGoods = GetRequest(link, headers=headers)
        if nomenclatureGoods['pager']['hasNext'] == True:
            resultNom = AppendGoods(resultNom, nomenclatureGoods)
        else:
            resultNom = AppendGoods(resultNom, nomenclatureGoods)
            break
    nomenclatureCategory = GetRequest("https://new.moykassir.ru/api/categories?need_hierarchy=true", headers=headers)
    resultCat = AppendCat(resultCat, nomenclatureCategory)
    WriterFile(resultNom, resultCat)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        headers['Authorization'] = 'Bearer ' + sys.argv[1]
    main()

def AppendGoods(resultNum, numenlature):
    for i in range(0, len(numenlature['items'])):
        resultNum.append({'TYPE': 'GOODS',
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
                          'CATEGORY': numenlature['items'][i]['type']})
        print(i)
    return resultNum

def AppendCat(resultCat, category):
    for i in range(0, len(category['items'])):
        resultCat.append({'TYPE': 'GROUP',
                          'NUM': category['items'][i]['id'],
                          'PARENT_CODE': '',
                          'NAME': category['items'][i]['name'],
                          'MEASURE_UNIT': '', 'UNIT_WEIGHT': '', 'ENERGY': '', 'FIBER': '', 'FAT': '',
                          'CARBOHYDRATE': '', 'PRICE': ''})

    return resultCat

# for i in range(1,9):
      #linkNom = "https://new.moykassir.ru/api/nomenclature?page=" + str(i) + "&limit=50&include_nested_categories=true"
#     print(linkNom)
#     nomenclature = GetRequest(linkNom, headersNom).json()
#     resultNom = AppendGoods(resultNom, nomenclature)
# category = GetRequest(linkCat, headersCat).json()
# print(category['items'][0])
# resultCat = AppendCat(resultCat, category)
# for i in resultNom:
#     print(i)
# print(len(resultNom))
# print(len(nomenclature['items']))
# print("TEST ______________________")
# print(nomenclature['items'][1]['name'])

def WriterFile(resultNom, resultCat):
    with open("nomenclature.csv", 'a', encoding='utf-8') as file:
        file_writer = csv.writer(file, delimiter=";", lineterminator="\r")
        file_writer.writerow(headlines)
        for i in resultNom:
            file_writer.writerow(i.values())
        for i in resultCat:
            file_writer.writerow(i.values())


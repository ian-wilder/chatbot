import requests
myText = input("What do you want translated? ")

payload = {'key': 'trnsl.1.1.20190117T132741Z.eb29b4e0109365dc.2bbd22b38b491ee6da903085ed4e941c6ab051d0', 'text': myText, 'lang':'en-ru'}
r = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate', params=payload)

print(r.text)

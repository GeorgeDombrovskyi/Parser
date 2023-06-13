# import csv
#
#
# with open('myJS.js', 'a') as file:
#     writer = csv.writer(file)
#
#     writer.writerow(
#         (
#             "let txt = 'my txt from file';let txt_ru = 'my ru text from file';function tryThis(){try{document.getElementById('ua-txt').innerHTML=txt}catch{console.log('ua ne zagryjen')};try{document.getElementById('ru-txt').innerHTML=txt_ru}catch{console.log('ru ne zagryjen')};};tryThis();",
#         )
#     )

import os
import csv


def dirback():
    m = os.getcwd()
    n = len(m.split('/')[1])
    y = m[0: -n]
    os.chdir(y)


# os.mkdir('toto')
print(os.getcwd())
os.chdir('toto')
print('1: ', os.getcwd())
print('2: ', os.getcwd())
dirback()
print('3:: ',os.getcwd())



# with open('myJS.js', 'a') as file:
#     writer = csv.writer(file)
#
#     writer.writerow(
#         (
#             "let txt = 'my txt from file';let txt_ru = 'my ru text from file';function tryThis(){try{document.getElementById('ua-txt').innerHTML=txt}catch{console.log('ua ne zagryjen')};try{document.getElementById('ru-txt').innerHTML=txt_ru}catch{console.log('ru ne zagryjen')};};tryThis();",
#         )
#     )
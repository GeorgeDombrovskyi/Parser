import csv


with open('myJS.js', 'a') as file:
    writer = csv.writer(file)

    writer.writerow(
        (
            "let txt = 'my txt from file';let txt_ru = 'my ru text from file';function tryThis(){try{document.getElementById('ua-txt').innerHTML=txt}catch{console.log('ua ne zagryjen')};try{document.getElementById('ru-txt').innerHTML=txt_ru}catch{console.log('ru ne zagryjen')};};tryThis();",
        )
    )


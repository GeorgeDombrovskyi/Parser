import csv

import bs4
import requests
import xlsxwriter
import os


# ------------------------------------------------------ MAIN SOURCES ------------------------------------------------------

main_url = 'https://autoprotect.ua/'
headers = {'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}

data_article = [['Артикул']]
data_name = [['Назва']]
data_stock = '0'  # - Запаси
data_avail = '0'  # - В наявності
data_cost = '0'  # - Звичайна ціна
data_brand = [['Позначки']]  # - Бренд товару
data_img_link = [['Зображення']]
data_analogs = [['Пропозиція товарів']]  # - Аналоги
data_original_details = [['Оригінальні  номери']]
data_another_cars = [['Застосовність до автомобілів']]
data_details_information = [['Технічні характеристики']]
data_combine_information = [['Опис']]

combine_ua_origin = []
combine_ua_inform = []
combine_ua_cars = []


cars_list = ['ACURA', 'ALFA ROMEO', 'AUDI', 'ASTON MARTIN', 'BMW', 'BUICK',
             'BENTLEY', 'BYD',  'CADILLAC', 'CHERY',  'CHEVROLET', 'CHRYSLER',  'CITRO"EN', 'CUPRA', 'DACIA',
             'DAEWOO', 'DS', 'DAIHATSU', 'DODGE', 'FIAT', 'FORD',  'GEELY',  'GAZ',
             'GMC', 'GENERAL MOTORS', 'GREAT WALL',  'HONDA', 'HUMMER', 'HYUNDAI',
             'INFINITI',  'ISUZU', 'IVECO', 'JAGUAR',  'JEEP', 'JAC', 'KIA', 'LADA', 'LANCIA', 'LANDWIND (JMC)',
             'LAND ROVER', 'LDV',  'LIFAN', 'LEXUS',  'MAN',  'MAZDA', 'MASERATI',  'MERCEDES-BENZ',
             'MG', 'MINI',  'MITSUBISHI', 'NISSAN',  'OPEL', 'PEUGEOT', 'PORSCHE', 'PONTIAC',
             'RAM', 'RENAULT', 'ROVER',  'SAAB', 'SCION', 'SEAT', 'SKODA', 'SMART', 'SSANGYONG',  'SCANIA',
             'SUBARU', 'SUZUKI',  'TOYOTA', 'VW',  'VOLVO',  'ЗАЗ',  'ГАЗ',  'УАЗ']


article_mme = [['product_sku']]
make_mme = [['make']]
model_mme = [['model']]
engine_mme = [['engine']]
combine_mme =[['product_sku', 'make', 'model', 'engine']]




page_parsing = '/catalog/tormoznoj_baraban'
data_category = 'Uncategorized, Автозапчастини, Автозапчастини > Гальмівна система, Автозапчастини > Гальмівна система > Гальмові елементи > Гальмівний барабан, Автозапчастини > Гальмівна система > Гальмові'


def get_soup(url):
    res = requests.get(url, headers)
    return bs4.BeautifulSoup(res.text, 'html.parser')


first_categories_page = get_soup(main_url + page_parsing)

name_product = ''
article_product = ''


# --- EXAMPLE FOR SEARCHING ON OUR SITE
# <a href="/shop/product-tag/090/">Аналог</a>
# http://localhost/shop/?s=nd+666&post_type=product


# --- MAKE A FOLDERS: CATEGORY, IMG, CARS CSV
category_folder_name = f"{page_parsing.split('/')[-1]}"
os.mkdir(category_folder_name)
os.chdir(category_folder_name)

img_folder_name = "IMG_folder"
os.mkdir(img_folder_name)

cars_csv_folder_name = "CSV_cars"
os.mkdir(cars_csv_folder_name)


# ------------------------------------------------------ DEFS AREA ------------------------------------------------------

# --- GO BACK ONE FOLDER (like "cd ..")
def dirback():
    m = os.getcwd()
    n = len(m.split('/')[-1])
    y = m[0: -n]
    os.chdir(y)
    return None


# --- PRODUCT NAME
def product_names(params):
    try:
        product_name = params.find('h1').find('span').find(string=True).strip()
        data_name.append([product_name])
    except: data_name.append([''])


# --- PRODUCT IMG AND ITS SOURCES
def product_img(params):
    print('-- Start IMG function')
    try:
        os.chdir(img_folder_name)

        img_link = params.find('div', class_='ccard-img').find('img')['src']
        file_name = str(img_link).split('/')[-1]
        img_data = requests.get(img_link).content

        with open(file_name, 'wb') as handler:
            handler.write(img_data)

        img_source = f'http://car-details.in.ua/wp-content/uploads/{category_folder_name}/' + file_name
        data_img_link.append([img_source])

    except: data_img_link.append([''])
    dirback()


# --- PRODUCT BRAND
def product_brand(params):
    try:
        brand = params.find('div', class_='ccard-pbrand').find('a').find(string=True).strip()
        data_brand.append([brand])
    except: data_brand.append([''])


# --- PRODUCT ARTICLE
def product_article(params):
    try:
        article = params.find('div', class_='ccard-part').find('b').find(string=True).strip()
        data_article.append([article])
    except: data_article.append([''])


# --- PRODUCT ORIGINAL DETAILS
def product_original_details(params):
    combine_ua_origin.clear()
    try:
        original_details_area = params.find('div', class_='item-oenmbrs-list').findAll('li')
        original_details_list = ''
        for original_details_area in original_details_area:
            original_details_list = original_details_list + original_details_area.text + '\n'

        combine_ua_origin.append("<div style='border:solid; border-color:#ed7583'></div><b>Оригінальні (конструкторські) номери:</b><div style='line-height: "
                                 "1.2; column-count:4'><br>" + original_details_list + "</div>")

        data_original_details.append([original_details_list])

    except:
        combine_ua_origin.append('')
        data_original_details.append([''])

def save_csv_cars(params_name):
    try:
        os.chdir(cars_csv_folder_name)
        with open(f'{params_name}.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerows(
                combine_mme
            )
    except: print('SAVE-CSV-CARS  -- something went WRONG!')
    dirback()


def save_main_csv(params_name):
    num = len(data_article)
    print('OUR NUM  -  ', num)

    with open(f'{params_name}.csv', 'a') as file:
        for w in range(0, num):
            writer = csv.writer(file)
            writer.writerow(
                [
                    data_article[w][0],
                    data_name[w][0],
                    data_brand[w][0],
                    data_combine_information[w][0],
                    data_analogs[w][0],
                    data_stock,
                    data_avail,
                    data_cost,
                    data_category,
                    data_img_link[w][0]
                ]
            )


def define_car(param_another, param_article):

    try:
        for check in cars_list:
            x = param_another.find(check)
            if x != -1:

                param_another = param_another.replace(check, '')
                # print('PARAM - ', param_another)
                param_another = param_another.split(':')
                # print('PARAM - ', param_another)


                combine_mme.append([param_article, check, param_another[0], param_another[1]])
                # print('111 -- ', combine_mme)
                # print('OUR COMBINE  -  ', combine_mme)
                # article_mme.append([param_article])
                # make_mme.append([check])
                # model_mme.append([param_another[0]])
                # engine_mme.append([param_another[1]])
                break
            elif check == 'УАЗ':
                print('check is - ', check)
                print('----- NOTHING HERE ----', param_another)



    except: print('DEF define Car goimg wrong')

# --- ANOTHER CARS
def another_cars(params, params_name):
    try:
        auto_list_area = params.find('div', class_="item-modifications-list").findAll('li')

        article = params.find('div', class_='ccard-part').find('b').find(string=True).strip()
        print('y nas v spiske - ', len(combine_mme))

        if len(combine_mme) < 10000 :
            for auto_list_area in auto_list_area:
                # print('start FOR auto_list_area')
                another_auto = auto_list_area.text
                # print('another_auto = ', another_auto)
                define_car(another_auto, article)
        else:
            print('ZAWLI ZA 10000')

            save_csv_cars(article)

            combine_mme.clear()

            combine_mme.append(['product_sku', 'make', 'model', 'engine'])

            for auto_list_area in auto_list_area:
                another_auto = auto_list_area.text
                define_car(another_auto, article)

    except: None


# --- DETAILS INFORMATION
def details_information(params):
    try:
        combine_ua_inform.clear()

        data_inform = ''
        information_area_name = params.findAll('div', class_="cc-tech-td-pn")
        information_area_value = params.findAll('div', class_="cc-tech-td-val")
        num = len(information_area_value)

        start = 0
        for list in range(1, num+1):
            data_inform = data_inform + "<tr><td style='text-align:center'>" + information_area_name[start].text + \
                          "</td><td style='width:50%; text-align:center'>" + \
                          information_area_value[
                start].text + "</td></tr>" + '\n'
            start = start+1

        combine_ua_inform.append("<div style='border:solid; border-color:#ed7583'></div><p  " \
                      "style='text-align:center'><b>Технічні характеристики</b></p><table style='font-size:15px; line-height: 1;'><tbody>" + data_inform +\
                      "</tbody></table>")

        data_details_information.append([data_inform])

    except:
        combine_ua_inform.append('')
        data_details_information.append([''])


# --- COMBINE ALL DATA
def data_combine():
    combiner = combine_ua_inform[0] + '\n' + combine_ua_origin[0]
    data_combine_information.append([combiner])


# --- ANALOGS
def analogs(params):
    try:
        analogs_area = params.find('div', class_='div-tbl tbl-ccard-analog').findAll('div', class_='tbl-tr')
        analogs_list= ''
        for analogs_area in analogs_area:
            src = analogs_area.find('a')['href']
            parse = get_soup(src)
            try:
                article = parse.find('div', class_='ccard-part').find('b').find(string=True).strip()
                analogs_list = analogs_list + article +', '
            except:
                None
        data_analogs.append([analogs_list])

    except: data_analogs.append([''])





# ------------------------------------------------------ MAIN AREA ------------------------------------------------------

def main():

    first_categories_page = get_soup(main_url + page_parsing)
    page_amont = int(first_categories_page.find('div', class_="cpages").findAll('li')[-1].find(string=True))
    print(page_amont)
    for page_num in range(1, page_amont+1):
        categories_page = get_soup(f'{main_url + page_parsing}/p_{page_num}')
        print('START - ', page_num)

        # params_name = f'{page_parsing.split("/")[-1]}_p_{page_num}'
        # print('our name  ', params_name)
        all_products_links = categories_page.findAll('p', class_='p-model')
        for all_products_links in all_products_links:
            product_link = all_products_links.find('a')['href']

            params_name = f'{product_link.split("/")[-1]}'
            print('our name  ', params_name)

            open_product_page = get_soup(product_link)

            # --- OUR FUNCTIONS
            product_names(open_product_page)
            product_article(open_product_page)
            product_brand(open_product_page)
            product_img(open_product_page)
            product_original_details(open_product_page)
            another_cars(open_product_page, params_name)
            details_information(open_product_page)
            analogs(open_product_page)
            data_combine()



        save_csv_cars(params_name)
    save_main_csv(category_folder_name)






if __name__ == '__main__':
    main()
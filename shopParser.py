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
data_category = 'Автозапчастини, Автозапчастини > Гальмівна система, Автозапчастини > Гальмівна система > Гальмові елементи > Гальмівні диски, Автозапчастини > Гальмівна система > Гальмові елементи'
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


cars_list = ['ACURA',  'ALFA ROMEO', 'AUDI', 'ASTON MARTIN', 'BMW', 'BUICK', 'BYD', 'CADILLAC', 'CHERY', 'CHEVROLET', 'CHRYSLER', 'CITROEN', 'DACIA',
             'DAEWOO', 'DAIHATSU', 'DODGE', 'FIAT', 'FORD', 'GEELY', 'GENERAL MOTORS', 'GREAT WALL', 'HONDA', 'HUMMER', 'HYUNDAI', 'INFINITI', 'ISUZU',
             'IVECO', 'JAGUAR', 'JEEP', 'KIA', 'LADA', 'LANCIA', 'LAND ROVER', 'LEXUS', 'LINKOLN', 'MAZDA', 'MERCEDES', 'MG', 'MINI', 'MITSUBISHI', 'OPEL',
             'PEUGEOT', 'PORSCHE', 'RENAULT', 'ROVER', 'SAAB', 'SEAT', 'SKODA', 'SMART', 'SSANGYONG', 'SUBARU', 'SUZUKI', 'TATA', 'TOYOTA', 'VAG',
             'VW' 'VOLKSWAGEN', 'VOLVO', 'ЗАЗ', 'ГАЗ', 'МОСКВИЧ', 'УАЗ']


article_mme = [['product_sku']]
make_mme = [['make']]
model_mme = [['model']]
engine_mme = [['engine']]





page_parsing = '/catalog/komplekt_napravlyayushhej_supporta'

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

        img_source = 'http://localhost/shop/wp-content/uploads/products_img/' + file_name
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
    print('start origin')
    combine_ua_origin.clear()
    try:
        print('start TRY')
        original_details_area = params.find('div', class_='item-oenmbrs-list').findAll('li')
        # print(original_details_area)
        original_details_list = ''
        for original_details_area in original_details_area:
            original_details_list = original_details_list + original_details_area.text + '\n'

        combine_ua_origin.append("<div style='border:solid; border-color:#ed7583'></div><b>Оригінальні (конструкторські) номери:</b><div style='line-height: "
                                 "1.2'><br>" + original_details_list + "</div>")

        data_original_details.append([original_details_list])

    except:
        print('start EXCEPT')
        combine_ua_origin.append('')
        data_original_details.append([''])


# --- ANOTHER CARS
def another_cars(params, params_name):
    art = [['art']]
    car = [['car']]

    try:
        auto_list_area = params.find('div', class_="item-modifications-list").findAll('li')
        print('how much - ', len(auto_list_area))

        article = params.find('div', class_='ccard-part').find('b').find(string=True).strip()

        for auto_list_area in auto_list_area:
            print('start FOR auto_list_area')
            another_auto = auto_list_area.text
            print('another_auto = ', another_auto)

            for check in cars_list:
                print('start FOR cars_list')
                x = another_auto.find(check)
                print('we are looking for  - ', check, ' in \n', another_auto)
                if x != -1:
                    print('est')
                    first = check
                    another_auto = another_auto.replace(check, '')
                    another_auto = another_auto.split(':')
                    second = another_auto[0]
                    third = another_auto[1]
                    print('111 --- ', first)
                    print('222 --- ', second)
                    print('333 --- ', third)
                    break
                else:
                    print('----- NOTHING HERE ----')


            car.append([another_auto])
            art.append([article])
            # another_auto_list_txt = another_auto_list_txt + another_auto + '\n'

        # with xlsxwriter.Workbook(article + '.xlsx') as workbook:
        #     worksheet = workbook.add_worksheet()
        #     for row_num, info in enumerate(art):
        #         worksheet.write_row(row_num, 0, info)
        #     for row_num, info in enumerate(car):
        #         worksheet.write_row(row_num, 1, info)

    except:
        combine_ua_cars.append('')
        data_another_cars.append([''])


# --- DETAILS INFORMATION
def details_information(params):
    try:
        combine_ua_inform.clear()

        print('------ start details information ------')
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
    print('start data combine')
    print('info -- ', combine_ua_inform[0])
    print('origin -- ', combine_ua_origin[0])
    print('ccars -- ', combine_ua_cars[0])

    # data_combine_information.clear()
    combiner = combine_ua_inform[0] + '\n' + combine_ua_origin[0] + '\n' + f"<div style='border:solid; border-color:#ed7583;'></div><b  " \
                                                                                         f"style='font-size:19px; color: #515151;'>Підходить до таких " \
                                                                                         f"авто:</b> <div id='iframeId' style='display:none'>" + \
               combine_ua_cars[0] + "</div> <button id='see-more'>Дивитись всі авто</button><script> let button = " \
                                                                                         f"document.getElementById('see-more'); let frame = " \
                                                                                         f"document.getElementById('iframeId');function go()" \
                                                                                         "{ frame.style.display='block';};button.addEventListener('click', " \
                                                                                         "go);</script>"

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

# --- MAKE EXCEL FILE
def make_xlsx():
    with xlsxwriter.Workbook(page_parsing.split('/')[-1]+'.xlsx') as workbook:
        worksheet = workbook.add_worksheet()
        for row_num, info in enumerate(data_name):
            worksheet.write_row(row_num, 0, info)
        for row_num, info in enumerate(data_article):
            worksheet.write_row(row_num, 1, info)
        for row_num, info in enumerate(data_brand):
            worksheet.write_row(row_num, 2, info)
        for row_num, info in enumerate(data_img_link):
            worksheet.write_row(row_num, 3, info)
        for row_num, info in enumerate(data_original_details):
            worksheet.write_row(row_num, 4, info)
        for row_num, info in enumerate(data_another_cars):
            worksheet.write_row(row_num, 5, info)
        for row_num, info in enumerate(data_details_information):
            worksheet.write_row(row_num, 6, info)
        for row_num, info in enumerate(data_combine_information):
            worksheet.write_row(row_num, 7, info)
        for row_num, info in enumerate(data_analogs):
            worksheet.write_row(row_num, 8, info)



# ------------------------------------------------------ MAIN AREA ------------------------------------------------------

def main():

    first_categories_page = get_soup(main_url + page_parsing)
    page_amont = int(first_categories_page.find('div', class_="cpages").findAll('li')[-1].find(string=True))
    for page_num in range(1, 2):
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
            # product_names(open_product_page)
            # product_article(open_product_page)
            # product_brand(open_product_page)
            # product_img(open_product_page)
            # product_original_details(open_product_page)
            another_cars(open_product_page, params_name)
            # details_information(open_product_page)
            # analogs(open_product_page)
            # data_combine()

        # make_xlsx()





if __name__ == '__main__':
    main()
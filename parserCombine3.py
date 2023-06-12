import bs4
import requests
import xlsxwriter
import csv
import os
# import translate

# For UA version
main_url = 'https://autoprotect.ua/'
headers = {'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}

data_name = [['Назва']]
data_article = [['Артикул']]
data_brand = [['Бренд']]
data_img_link = [['Шлях до картинки']]
data_original_details = [['Оригінальні  номери']]
data_another_cars = [['Застосовність до автомобілів']]
data_details_information = [['Технічні характеристики']]
data_combine_information = [['Опис']]

combine_ua_origin = []
combine_ua_inform = []
combine_ua_cars = []




# <a href="/shop/product-tag/090/">Аналог</a>

page_parsing = '/catalog/komplekt_napravlyayushhej_supporta'

def get_soup(url):
    res = requests.get(url, headers)
    return bs4.BeautifulSoup(res.text, 'html.parser')


first_categories_page = get_soup(main_url + page_parsing)

name_product = ''
article_product = ''



# def txt_trans(text):
#     print('we are start')
#     try:
#         t = translate.Translator(from_lang='ru', to_lang='uk')
#         print(t.translate(text))
#
#     except:
#         print('wrong')


#  PRODUCT NAME
def product_names(params):
    try:
        product_name = params.find('h1').find('span').find(string=True).strip()
        data_name.append([product_name])
    except: data_name.append([''])

#  PRODUCT IMG AND ITS SOURCES
def product_img(params):
    try:
        img_link = params.find('div', class_='ccard-img').find('img')['src']
        file_name = str(img_link).split('/')[-1]
        img_data = requests.get(img_link).content

        with open(file_name, 'wb') as handler:
            handler.write(img_data)

        img_source = 'http://localhost/shop/wp-content/uploads/products_img/' + file_name
        data_img_link.append([img_source])
        print(file_name)
    except: data_img_link.append([''])



    # GO TO PRODUCT PAGE for another information

#  PRODUCT BRAND
def product_brand(params):
    try:
        brand = params.find('div', class_='ccard-pbrand').find('a').find(string=True).strip()
        data_brand.append([brand])
    except: data_brand.append([''])

# PRODUCT ARTICLE
def product_article(params):
    try:
        article = params.find('div', class_='ccard-part').find('b').find(string=True).strip()
        data_article.append([article])
    except: data_article.append([''])

# PRODUCT ORIGINAL DETAILS
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

# ANOTHER CARS
def another_cars(params, params_name):
    try:
        combine_ua_cars.clear()

        another_auto_list_txt = ''
        auto_list_area = params.find('div', class_="item-modifications-list").findAll('li')

        for auto_list_area in auto_list_area:
            another_auto = auto_list_area.text
            another_auto_list_txt = another_auto_list_txt + another_auto + '\n'

        data_another_cars.append([another_auto_list_txt])
        combine_ua_cars.append(another_auto_list_txt)
    except:
        combine_ua_cars.append('')
        data_another_cars.append([''])


# DETAILS INFORMATION
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



# MAKE EXCEL FILE
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

            #  PRODUCT NAME
            product_names(open_product_page)

            #  PRODUCT ARTICLE
            product_article(open_product_page)

            #  PRODUCT BRAND
            product_brand(open_product_page)

            #  PRODUCT IMG
            product_img(open_product_page)

            # PRODUCT ORIGINAL DETAILS
            product_original_details(open_product_page)

            # ANOTHER CARS FOR THIS DETAIL
            another_cars(open_product_page, params_name)

            # INFORMATION ABOUT DETAILS
            details_information(open_product_page)

            # COMBINE FUNCTION FOR -- information, Original, Another Cars
            data_combine()

        make_xlsx()





if __name__ == '__main__':
    main()
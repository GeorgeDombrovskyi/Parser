import xlsxwriter
import bs4
import requests


def make_xlsx():
  with xlsxwriter.Workbook(page_parsing.split('/')[-1] + '.xlsx') as workbook:
    worksheet = workbook.add_worksheet()
    for row_num, info in enumerate(data_name):
      worksheet.write_row(row_num, 0, info)

def get_soup(url):
  return bs4.BeautifulSoup(url, 'html.parser')

f = open("./9090.html", encoding="utf8")
page = get_soup(f)

look_len = len(page.text.split('\n'))
look = page.text.split('\n')


def main():
  cl = int(look_len)
  for calc in range(0, look_len):
    li = look[cl-1]
    li = li.replace(',', '-')
    try:
      li = li.replace('VW', 'VW,')
      li = li.replace('Дизель', ', Дизель')
      li = li.replace('бензин', ', бензин')
      print(li)
    except: None
    cl = cl - 1

if __name__ == '__main__':
  main()
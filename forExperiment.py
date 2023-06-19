import os
# car = 'VOLVO 90 145 (930_): бензин 1.8 i.e. 16V (930.A1A) AR 32201 ( 144 л.с., 106 kw )'
#
#
# cars_list = ['ACURA',  'ALFA ROMEO', 'AUDI', 'BMW', 'CADILLAC', 'CHERY', 'CHEVROLET', 'CHRYSLER', 'CITROEN', 'DACIA', 'DAEWOO', 'DAIHATSU', 'DODGE', 'FIAT',
#           'FORD',
#      'GEELY', 'HONDA', 'HUMMER', 'HYUNDAI', 'INFINITI', 'IVECO', 'JAGUAR', 'JEEP', 'KIA', 'LAND ROVER', 'LEXUS', 'MAZDA', 'MERCEDES', 'MINI', 'MITSUBISHI',
#      'NISSAN', 'NISSAN', 'OPEL', 'PEUGEOT', 'PORSCHE', 'RENAULT', 'ROVER', 'SAAB', 'SEAT', 'SKODA', 'SMART', 'SSANGYONG', 'SUBARU', 'SUZUKI', 'TOYOTA',
#      'VOLKSWAGEN', 'VOLVO']
#
#
# article_mme = [['product_sku']]
# make_mme = [['make']]
# model_mme = [['model']]
# engine_mme = [['engine']]
#
# num = 0
#
# for check in cars_list:
#     x = car.find(cars_list[num])
#     print('we are looking for  - ', cars_list[num] ,' in \n', car)
#     if x != -1:
#         print('est')
#         first = cars_list[num]
#         car = car.replace(cars_list[num], '')
#         car = car.split(':')
#         second = car[0]
#         third = car[1]
#         print(first)
#         print(second)
#         print(third)
#         break
#     else:
#         print('----- NOTHING HERE ----')
#         num = num + 1
#
#
# print('the end')


num = 0
list = ['a', 'b', 'c', 'd']

def fun():
    for check in list:
        print(num)
        num = num + 1

fun()


# dt_a = [['a']]

# dt_a.append(['bb'])
# dt_a.clear()
# dt_a.append(['a'])
# print(dt_a)







# def dirback():
#     we_here = os.getcwd()
#     need_cut = len(we_here.split('/')[-1])
#     will_be = we_here[0: -need_cut]
#     os.chdir(will_be)
#
# dirback()
#coding: utf-8

import sys
import requests
import datetime
import cx_Oracle
from   bs4 import BeautifulSoup


#-----Winter Roads dictionary----------------
zimniki_sprav = {'Подъезд к п. Тулень':1,
                'Ельники - Хайрюзовка':2,
                'Шиверский - Хребтовый':3,
                'Обход Богучан':4,
                'Мендельский - Малая Кеть':5,
                'Промбор - Проточное':6,
                'Маталассы - Никифоровка':7,
                'Черемушки - Тюлюпта':8,
                '"Черемушки - Тюлюпта" - Березовая':9,
                'Обход Енисейска':10,
                'Енисейск-Ярцево-Ворогово-Бор':11,
                'Высокогорский - Усть-Ангарск':12,
                'Ярцево - Сым':13,
                '"Енисейск - Ярцево - Ворогово - Бор" - Луговатка':14,
                'Усть-Кемь - Новоназимово':15,
                'Ялань - Маковское':16,
                'Таежный - граница с Эвенкией':17,
                'Аксеново - 45 км а.д. "Новая Недокура - граница с Иркутской областью"':18,
                'Ирба - Бидея':19,
                'Тагара - Таежный':20,
                'Тагара - Яркино':21,
                'Новая Недокура - граница с Иркутской областью':22,
                'Момотово-Захаровка-Стрелка':23,
                'Кирсантьево - Устье - Машуковка':24,
                'Ильинка - Южная Тунгуска':25,
                'Тиличеть-Кедровый':26,
                'Южная Тунгуска - Сосновка':27,
                'Мендельский-Малая Кеть':28,
                'Кетский - Чайда':29,
                'Кирсантьево-Устье-Машуковка':30,
                'Тасеево - Усть-Кайтым':31,
                'Роща-Пинчино':32,
                'Никольское-Речка':33,
                'Бор-Верхнеимбатск':34,

}

#--------Rayon codes dictionary-------------------
rayon_sprav = {
    'Туруханский':   '04254000000',
    'Уярский':       '04257501000',
    'Тасеевский':    '04252000000',
    'Пировский':     '04245000000',
    'Нижнеингашский':'04239000000',
    'Мотыгинский':   '04235000000',
    'Казачинский':   '04220000000',
    'Кежемский':     '04224000000',
    'Енисейский':    '04215000000',
    'Балахтинский':  '04204000000',
    'Бирилюсский':   '04206000000',
    'Богучанский':   '04209000000',
    'Абанский':      '04201000000',
    'Иланский':      '04218000000',
}


#----State dictionary-----------
status_sprav = {
    'Открыта':1,
    'Закрыта':2,
    

}


# URL for data download
pereprava_url = 'http://ois.krudor.ru/oi/'


def generate_zimnik_records():
    """Generate Winter roads data"""
    # Oracle server parameters
    ora_user  = 'm4c'
    ora_pass  = 'm4c'
    ora_ip    = '195.112.255.99'
    ora_port  =  1521
    ora_SID   = 'oracle11'
    oratable = 'data_test'

    # Get current data
    today = datetime.date.today().strftime("%Y-%m-%d")

    # Download Crudor data page
    html = requests.get(pereprava_url, auth=('mchs_monitoring','kyDCc0')).content        
    soup = BeautifulSoup(html, "html.parser")

    
    #*********************WINTER ROADS**************************************************
    tab_zimnik = soup.find_all("table", { "id" : "winter_in_plan_list" }).pop()
    trs = tab_zimnik.find_all('tr')

    
    
    # Connect to Oracle
    dsn_tns = cx_Oracle.makedsn(ora_ip, ora_port, ora_SID)
    db  = cx_Oracle.connect(ora_user, ora_pass, dsn_tns)
    cur = db.cursor()

    
    # Iterate over data table
    counter=0
    for tr in trs:
        tr_len = len(tr.find_all('td')) 
        if tr_len==1 or tr_len<4: 
            continue

        else:
            row=[]
            for i in range(0,4):
                cell = tr.find_all('td')[i].text.lstrip().rstrip().encode('utf8')
                row.append(cell)
            
            
            rayon,descr,title,status = row
            a = rayon.find('(')
            b = rayon.find(')')        
            rayon = rayon[a+1:b]
            

            # Get zimnik_id
            try:
                zimnik_id = zimniki_sprav[title]
            except KeyError:
                sys.exit(1)

            # Get status_id
            try:
                status_id = status_sprav[status]
            except KeyError:
                sys.exit(1)
                
            # Check is this the first row for this date and road ID
            query = """select count(*) from %s where id_zimn=%s and dt=to_date('%s', 'yyyy-mm-dd')""" % (oratable,zimnik_id, today)
            cur.execute(query)
            n = cur.fetchone()[0]
            
            if n==0: 
                print 'make insert'
                query = """insert into %s (id_zimn,id_state,dt) values (%s,%s,to_date('%s', 'yyyy-mm-dd'))""" % (oratable,zimnik_id,status_id,today)
            else:
                print 'make update'
                query = """update %s set id_state=%s  where id_zimn=%s and dt=to_date('%s', 'yyyy-mm-dd')""" % (oratable, status_id, zimnik_id, today)

            # Do query 
            cur.execute(query)
        

    # Close connection
    db.commit()
    cur.close()
    db.close()




# Generate DB records for winter roads...
generate_zimnik_records()


# # Подгружаем всю страницу КРУДОР
# html = requests.get(pereprava_url, auth=('mchs_monitoring','kyDCc0')).content        
# soup = BeautifulSoup(html, "html.parser")


# #**************************ПЕРЕПРАВЫ************************************************
# # Получаем объекты из таблицы Переправа
# tab_pereprava = soup.find_all("table", { "id" : "bridges_in_plan_list" }).pop()
# trs = tab_pereprava.find_all('tr')

# # Массив распарсенных значений из таблицы Переправа
# rows = []
# # Итерируем по таблице Переправа
# for tr in trs:
#     if len(tr.find_all('td'))==1: 
#         continue
#     else:
#         try:
#             row=[]
#             for i in range(0,8):
#                 cell = tr.find_all('td')[i].text.lstrip().rstrip().encode('utf8')
#                 row.append(cell)
#             rows.append(row) 
#         except:
#             pass
            

# print 'Save pereprava to file...'
# write_to_excel(rows,prefix+'pereprava.xls')



# #*********************ЗИМНИКИ*****************************************************
# # Получаем объекты из таблицы Зимники
# tab_zimnik = soup.find_all("table", { "id" : "winter_in_plan_list" }).pop()
# trs = tab_zimnik.find_all('tr')

# # Массив распарсенных значений из таблицы Переправа
# rows = []
# # Итерируем по таблице Переправа
# for tr in trs:
#     if len(tr.find_all('td'))==1: 
#         continue
#     else:
#         try:
#             row=[]
#             for i in range(0,4):
#                 cell = tr.find_all('td')[i].text.lstrip().rstrip().encode('utf8')
#                 row.append(cell)
#             rows.append(row) 
#         except:
#             pass
            

# print 'Save zimniki to file...'
# write_to_excel(rows,prefix+'zimniki.xls')


# #************************ДТП**********************************************
# # Получаем объекты из таблицы ДТП
# tab_dtp = soup.find_all("table", { "id" : "dtp_list" }).pop()
# trs = tab_dtp.find_all('tr')

# # Массив распарсенных значений из таблицы ДТП
# rows = []
# # Итерируем по таблице ДТП
# for tr in trs:
#     if len(tr.find_all('td'))==1: 
#         continue
#     else:
#         try:
#             row=[]
#             for i in range(0,13):
#                 cell = tr.find_all('td')[i].text.lstrip().rstrip().encode('utf8')
#                 row.append(cell)
#             rows.append(row) 
#         except:
#             pass
            

# print 'Save DTP to file...'
# write_to_excel(rows,prefix+'dtp.xls')


# #************************ЧС**********************************************
# # Получаем объекты из таблицы ЧС
# tab_chs = soup.find_all("table", { "id" : "chs_list" }).pop()
# trs = tab_chs.find_all('tr')

# # Массив распарсенных значений из таблицы ЧС
# rows = []
# # Итерируем по таблице ЧС
# for tr in trs:
#     if len(tr.find_all('td'))==1: 
#         continue
#     else:
#         try:
#             row=[]
#             for i in range(0,12):
#                 cell = tr.find_all('td')[i].text.lstrip().rstrip().encode('utf8')
#                 row.append(cell)
#             rows.append(row) 
#         except:
#             pass
            

# print 'Save CHS to file...'
# write_to_excel(rows,prefix+'chs.xls')

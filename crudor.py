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

#------Crossroads dictionary------
crossroad_sprav = {
    'Покотеево - Хиндичет_0+001_Ледовая':1,
    'Ангарский-Иркинеево-Артюгино_22+065_Ледовая':2,
    'Манзя-Каменка_0+100_Ледовая':223,
    'Манзя-Каменка_3+854_Ледовая':4,
    'Бирилюссы-Биктимировка_1+364_Понтонная':245,
    'Бирилюссы-Биктимировка_1+364_Ледовая':225,
    'Бирилюссы-Биктимировка_1+364_Паромная':7,
    'Шпагино 2-Подкаменка_28+400_Ледовая':226,
    'Шпагино 2-Подкаменка_28+400_Паромная':227,
    'Шуточкино-Зачулымка-Сахарное_3+660_Понтонная':229,
    'Шуточкино-Зачулымка-Сахарное_3+660_Ледовая':228,
    'Шуточкино-Зачулымка-Сахарное_3+660_Паромная':230,
    'Большая Косуль-Казанка_9+404_Понтонная':231,
    'Большая Косуль-Казанка_9+404_Ледовая':232,
    'Красный Завод-Вагино_0+011_Ледовая':233,
    'Красный Завод-Вагино_0+011_Понтонная':234,
    'Большой Кантат-Предивинск_20+309_Ледовая':235,
    'Большой Кантат-Предивинск_20+309_Паромная':236,
    'Епишино-Северо-Енисейский_0+066_Ледовая':237,
    'Епишино-Северо-Енисейский_0+066_Паромная':238,
    'Мотыгино-Широкий Лог_140+100_Ледовая':252,
    'Мотыгино-Широкий Лог_140+100_Паромная':253,
    'Жеблахты-Ивановка_0+959_Понтонная':239,
    'Жеблахты-Ивановка_0+959_Ледовая':240,
    'Каратузское-Старая Копь_5+849_Паромная':242,
    'Каратузское-Старая Копь_5+849_Ледовая':241,
    'Н.Болтурино-Н.Недокура_24+190_Ледовая':244,
    'Н.Болтурино-Н.Недокура_24+190_Паромная':243,
    'Момотово-Широково_0+000_Паромная':246,
    'Момотово-Широково_0+000_Ледовая':99,
    'Мотыгино-Широкий Лог_13+900_Ледовая':222,
    'Мотыгино-Широкий Лог_13+900_Паромная':248,
    'Рыбное - Устье (Слюдрудник - Машуковка)_24+400_Ледовая':249,

}


#----Crossroads status dictionary-----
crossroad_status_sprav = {
    'Открыта':1,
    'Закрыта':2,    

}


#-----Crossroads types dictionary-----
crossroad_types_sprav = {
    'Ледовая':1,
    'Паромная':2,
    'Понтонная':3,    

}


# URL for data download
pereprava_url = 'http://ois.krudor.ru/oi/'


def generate_winterroad_records():
    """Generate Winter roads data"""
    # Oracle server parameters
    ora_user  = 'm4c'
    ora_pass  = 'm4c'
    ora_ip    = '195.112.255.99'
    ora_port  =  1521
    ora_SID   = 'oracle11'
    oratable  = 'data_winterroad'

    # ora_user  = 'm4c'
    # ora_pass  = 'm4c'
    # ora_ip    = '172.16.128.159'
    # ora_port  =  1521
    # ora_SID   = 'oracle11'
    # oratable  = 'data_winterroad'

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
            query = """select count(*) from %s where idat_winterroad=%s and rdate=to_date('%s', 'yyyy-mm-dd')""" % (oratable,zimnik_id, today)
            cur.execute(query)
            n = cur.fetchone()[0]
            
            if n==0: 
                print 'make insert to the winterroad table'
                query = """insert into %s (idat_winterroad,idat_winterroad_stat,rdate) values (%s,%s,to_date('%s', 'yyyy-mm-dd'))""" % (oratable,zimnik_id,status_id,today)
            else:
                print 'make update to the winterroad table'
                query = """update %s set idat_winterroad_stat=%s  where idat_winterroad=%s and rdate=to_date('%s', 'yyyy-mm-dd')""" % (oratable, status_id, zimnik_id, today)

            # Do query 
            cur.execute(query)
        

    # Close connection
    db.commit()
    cur.close()
    db.close()




def generate_crosswater_records():
    """Generate River bridges data"""
    # Oracle server parameters
    ora_user  = 'm4c'
    ora_pass  = 'm4c'
    ora_ip    = '195.112.255.99'
    ora_port  =  1521
    ora_SID   = 'oracle11'
    oratable  = 'data_crosswater'

    # ora_user  = 'm4c'
    # ora_pass  = 'm4c'
    # ora_ip    = '172.16.128.159'
    # ora_port  =  1521
    # ora_SID   = 'oracle11'
    # oratable  = 'data_crosswater'

    # Get current data
    today = datetime.date.today().strftime("%Y-%m-%d")

    # Download Crudor data page
    html = requests.get(pereprava_url, auth=('mchs_monitoring','kyDCc0')).content        
    soup = BeautifulSoup(html, "html.parser")


    #**************************CROSSROAD TABLE*****************************************
    # Obtain data from crossroad page
    tab_pereprava = soup.find_all("table", { "id" : "bridges_in_plan_list" }).pop()
    trs = tab_pereprava.find_all('tr')

    # Connect to Oracle
    dsn_tns = cx_Oracle.makedsn(ora_ip, ora_port, ora_SID)
    db  = cx_Oracle.connect(ora_user, ora_pass, dsn_tns)
    cur = db.cursor()


    # Arrange of parsed data
    rows = []
    # Iterate over crossroad data chunk
    for tr in trs:
        if len(tr.find_all('td'))==1: 
            continue
        else:
            try:
                row=[]
                for i in range(0,8):
                    cell = tr.find_all('td')[i].text.lstrip().rstrip().encode('utf8')
                    row.append(cell)
                rows.append(row)

                ray   = row[0]
                obj   = row[1]
                dist  = row[2]
                ctype = row[3]
                river = row[4]
                city  = row[5]
                gruz  = row[6]
                obj_state = row[7]
                
                # Generate key for crossroad value
                key = '%s_%s_%s' % (obj,dist,ctype)
                try:
                    crossroad_id = crossroad_sprav[key]
                    crossroadstate_id = crossroad_status_sprav[obj_state] 
                    #print 'Pereprava id - %s, pereprava_state id - %s, date - %s' % (crossroad_id, crossroadstate_id, today)
                    
                    # Check is this the first row for this date and road ID
                    query = """select count(*) from %s where idat_crosswater=%s and rdate=to_date('%s', 'yyyy-mm-dd')""" % (oratable,crossroad_id, today)
                    cur.execute(query)
                    n = cur.fetchone()[0]
                    
                    if n==0: 
                        print 'make insert to the crosswater table'
                        query = """insert into %s (idat_crosswater,idat_crosswater_stat,rdate) values (%s,%s,to_date('%s', 'yyyy-mm-dd'))""" % (oratable,crossroad_id,crossroadstate_id,today)
                    else:
                        print 'make update to the crosswater table'
                        query = """update %s set idat_crosswater_stat=%s  where idat_crosswater=%s and rdate=to_date('%s', 'yyyy-mm-dd')""" % (oratable, crossroadstate_id, crossroad_id, today)

                    # Do query 
                    cur.execute(query)

                except:
                    pass
            except:
                pass
                
    # Close connection
    db.commit()
    cur.close()
    db.close()



# Generate DB records for winter roads...
generate_winterroad_records()

# Generate DB records for crosswater ...
generate_crosswater_records()



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
            

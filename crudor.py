#coding: utf-8

import xlwt
import requests
import datetime
from   lxml import etree
from   bs4 import BeautifulSoup


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
                'Кетский - Чайда':28,
                'Кирсантьево-Устье-Машуковка':29,
                'Тасеево - Усть-Кайтым':30,
                'Роща-Пинчино':31,
                'Никольское-Речка':32,
                'Бор-Верхнеимбатск':33,

}

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

status_sprav = {
    'Закрыта':0,
    'Открыта':1,

}


# URL шаблон для подгрузки данных
pereprava_url = 'http://ois.krudor.ru/oi/'
prefix = '/home/valera/crudor/'
#prefix = '/home/ivb/crudor/'


def write_to_excel(items, fname):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Лист'.decode('utf8'))

    row = 0
    for item in items:
        cell = 0
        for elem in item:
            ws.write(row, cell, elem.decode('utf8'))
            cell+=1
        row+=1

    # Сохраняем в Excel
    wb.save(fname)



def generate_xml():
    """Generate XML data files"""

    # Подгружаем всю страницу КРУДОР
    html = requests.get(pereprava_url, auth=('mchs_monitoring','kyDCc0')).content        
    soup = BeautifulSoup(html, "html.parser")

    
    #*********************ЗИМНИКИ*****************************************************
    # Получаем объекты из таблицы Зимники
    tab_zimnik = soup.find_all("table", { "id" : "winter_in_plan_list" }).pop()
    trs = tab_zimnik.find_all('tr')

    # Generate XML document...
    print '\nGenerate XML document...'
    root = etree.Element('zimnik_list')

    
    # Итерируем по таблице Переправа
    zimnik_id = 1

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
            
            
            zimnik = etree.SubElement(root, "zimnik", id=str(zimnik_id))
  
            try:
                #print '\nold title2 - %s' % (title)
                title = str(zimniki_sprav[title])
                #print 'new title2 - %s' % (title)
            except:
                title = 'unknown'
            
            try:
                rayon_okato = str(rayon_sprav[rayon])
            except:
                rayon_okato = 'unknown'
            
            try:
                status = str(status_sprav[status])
            except:
                status = 'unknown'


            etree.SubElement(zimnik, "title").text  = title.decode('utf-8')
            etree.SubElement(zimnik, "rayon").text  = rayon_okato.decode('utf-8')
            etree.SubElement(zimnik, "status").text = status.decode('utf-8')

            # Next zimnik ID
            zimnik_id+=1



    #-----------------------Save to XML file----------------------
    today = datetime.date.today().strftime("%Y%m%d")
    out = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True)
    xml_out = open('crudor_%s.xml' % (today), 'w')
    xml_out.write(out)
    xml_out.close()



    

if __name__=='__main__':
    
    generate_xml()

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

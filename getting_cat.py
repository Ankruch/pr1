#!/usr/bin/env python
# -*- coding: utf-8 -*-

# запускается в виде mapper-a в MapReduce job, вход =строчки с доменным именем woman.ru \n avito.ru \n gazeta.ru
#  пример вывода: google.ru	Hi-Tech	Поисковые системы	Интернет

import sys
from bs4 import BeautifulSoup
import requests

reload(sys)
sys.setdefaultencoding('utf8')


def main():

    for line in sys.stdin:
        if line: # line = доменное имя, типа woman.ru, avito.ru, gazeta.ru
            url_s = u'https://yandex.ru/yaca/yca/cy/'+line.strip()
            l1= BeautifulSoup(requests.get(url_s).text).text
            if l1.find(u'Войти Каталог') > 0:  #если существует в каталоге Яндекс
                piece =  l1[l1.find(u'Войти Каталог'):][13:] #ищем начало нужной строки, вырезаем кусок
                if re.findall(r'\d',piece)!=[]: #вырезаем перечисление каталогов через /, последняя запись слитно
                    cat = re.split(re.findall(r'\d',piece)[0],piece)[0]
                    pre_results = cat.split(u" /") #формируем массив записей каталогов, последняя запись там может быть 
                    #записана слитно как / Hi-Tech / ИнтернетПоисковые системы - таким образом это вытаскивает BS
                    results = []
                    for cat1 in pre_results:
                        cat1 = cat1.strip()
                        if  (cat1 != u"СМИ")  and re.search(ur'[А-Я]',cat1[1:-1]): #если это слитная запись, то разделяем
                            position = re.search(ur'[А-Я]',cat1[1:-1]).start()
                            results.append(cat1[position+1:])
                            results.append(cat1[:position+1])
                        else:
                            results.append(cat1)
        
                    #выводим в map
                    results_str = '' 
                    for cat in results:
                    if cat:
                        if results_str:
                            results_str =  results_str + '/t' + cat
                        else:
                            results_str =  cat    
                    print line + '/t' +results_str
if __name__ == "__main__":
    main()


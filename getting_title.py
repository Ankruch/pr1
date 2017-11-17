#!/usr/bin/env python
# -*- coding: utf-8 -*-

# запускалось в виде mapper-а Hadoop-а, на вход подаются строки, содержащие доменные имена
# выход вида доменное имя табуляция список лемматизированных слов из title через пробел
# пример выхода afisha.ru	 афиша сходить москва

import sys
import requests
from nltk.tokenize import RegexpTokenizer
from pymystem3 import Mystem
import nltk

# encoding=utf8
reload(sys)
sys.setdefaultencoding('utf8')


def main():
    stop_words1  = nltk.corpus.stopwords.words('english')
    stop_words2 = nltk.corpus.stopwords.words('russian')
    sw  = [u"наша", u'наш', u'мой', u'бесплатный', u'quot']
    m = Mystem()
    for line in sys.stdin: # line это доменное имя, типа woman.ru, gazeta.ru, sport.ru
        title = ''
        body=''
        url_s = u'http://'+line.strip() #формируем url
      try:
         body= requests.get(url_s,timeout=3).text.lower() #запрос на выкачивание url
      except:
         pass
      if body.find(u'<title>')> 0: #ищем title
         title = body[body.find(u'<title>')+7 : body.find(u'</title>') ] 
         if (title.strip() !=u'""') and (title.strip() !=u''):
             title = title.replace("\t"," ").replace('\n'," ") #заменяем все служебные символы внутри title
             tokenizer = RegexpTokenizer(u'[A-Za-zА-Яа-яёЁ]+') 
             tokens = tokenizer.tokenize(title) #токенизируем
             lemms = ''
             for i in tokens:
                 if len(i)>2:
                     lemma = m.lemmatize(i)[0] #лемматизируем токен
                     if not (lemma in stop_words1 or lemma in stop_words2 or lemma in sw):
                        lemms = lemms + ' '+ lemma #формируем итоговую строку
             if lemms.strip():
                 print line.strip() + u'\t'+ lemms + u'\n'
        


if __name__ == "__main__":
    main()

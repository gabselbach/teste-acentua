import os
import re
import pandas as pd
import time
import requests
import spacy
import json
from spacy.tokenizer import Tokenizer
from bs4 import BeautifulSoup
from unicodedata import normalize 
def faz_busca(token):
  dataNova=[]
  valorTime=0
  count=0
  for k in token:
    count+=1
    valorTime+=1
    t=0
    busca = normalize('NFKD', str(k)).encode('ASCII','ignore').decode('ASCII')
    page = requests.get('http://www.portaldalinguaportuguesa.org/index.php?action=syllables&act=list&search='+busca)
    soup = BeautifulSoup(page.text, 'html.parser')
    palavras = soup.find_all('td',{'title':'Palavra'}) 
    classe=''
    value=0
    if(not palavras):
      #Para palavras que estejam no plural
      novo=busca[:-1]
      page = requests.get('http://www.portaldalinguaportuguesa.org/index.php?action=syllables&act=list&search='+busca)
      soup = BeautifulSoup(page.text, 'html.parser')
      palavras = soup.find_all('td',{'title':'Palavra'}) 
      if(not palavras):
        temp = {
        'PALAVRAANT':k,
        'PALAVRAVOP':'NAN',
        'SILABA': 'NAN',
        'CLASSE':'NAN',
        'MONOSSILABA':0
        }
        dataNova.append(temp)
      else:
        value=1
    elif(palavras or value==1):
      aux=0
      for i in palavras:
        link=re.sub('<[^>]+?>', '', str(i.find('a')))
        pala = i.text.replace(" ",'').split('\n')[0]
        palavraNormalizada = normalize('NFKD', link).encode('ASCII','ignore').decode('ASCII')
        if(palavraNormalizada == busca):
          forte =  re.sub('<[^>]+?>', '', str(i.find('u')))
          silaba = pala.split(')')[1]
          silsepara = silaba.split('·')
          if(len(silsepara)==1):
            mono=1
          else:
            mono=0

          oxi=''
          paro=''
          propa=''
          for j in range(len(silsepara)-1, -1, -1):
            if(aux==0):
              oxi= silsepara[j] + oxi
            elif(aux==1):
              paro = silsepara[j] + paro
            elif(aux==2):
              propa= silsepara[j] + propa
            aux+=1
          if(oxi==forte):
            classe='oxítona'
          elif(paro==forte):
            classe='paroxítona'
          elif(propa==forte):
            classe='proparoxítona'
          temp = {
              'PALAVRAANT':k,
              'PALAVRAVOP':link,
              'SILABA':silaba,
              'CLASSE':classe,
              'MONOSSILABA':mono
          }
          dataNova.append(temp)
          t=1
          break
        if(t==1):
          break   
  return dataNova
texto = 'hoje o ceu esta tao lindo'
nlp = spacy.load("pt_core_news_sm")
conteudo = nlp(texto)
#print(conteudo,'\n\n')
retorno =faz_busca(conteudo)
for j in len(retorno):
    print(j)
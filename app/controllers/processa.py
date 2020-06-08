import os
import re
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
from unicodedata import normalize
from flask_cors import CORS
from flask import render_template
from app import app
from urllib import request
cors = CORS(app, resource={r"/*":{"origins": "*"}})


def faz_busca(token):
  dataNova=[]
  busca = normalize('NFKD', str(token)).encode('ASCII','ignore').decode('ASCII')
  page = requests.get('http://www.portaldalinguaportuguesa.org/index.php?action=syllables&act=list&search='+busca)
  soup = BeautifulSoup(page.text, 'html.parser')
  palavras = soup.find_all('td',{'title':'Palavra'}) 
  classe=''
  palavracerta=''
  if(not palavras):
    temp = {
    'PALAVRA':busca,
    'SILABA': 'NAN',
    'CLASSE':'NAN'
    }
    dataNova.append(temp)
  else:
    pal=''
    oxi=''
    paro =''
    propa =''
    forte =''
    silaba =''
    classe=''
    aux=0
    for i in palavras:
      link=re.sub('<[^>]+?>', '', str(i.find('a')))
      pala = i.text.replace(" ",'').split('\n')[0]
      palavraNormalizada = normalize('NFKD', link).encode('ASCII','ignore').decode('ASCII')
      if(palavraNormalizada == busca):
        forte =  re.sub('<[^>]+?>', '', str(i.find('u')))
        silaba = pala.split(')')[1]
        silsepara = silaba.split('·')
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
            'PALAVRA':link,
            'SILABA':silaba,
            'CLASSE':classe
        }
        dataNova.append(temp)
        break  
  return dataNova
@app.route('/handle_data', methods=['POST'])
def handle_data():
    texto = request.form['texto']
    titulo = request.form['titulo']
    #Fazer o processamento
    #return render_template('processa.html',retorno = retorno)
    # your code
    # return a response

@app.route('/VOP')
def VOP():
  retorno =faz_busca('fertil')
  return render_template('processa.html',retorno = retorno)
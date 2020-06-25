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
#from flask_cors import CORS
from flask import render_template
from app import app
from flask import request
#cors = CORS(app, resource={r"/*":{"origins": "*"}})

def Verbos(palavra):
  propa = re.compile(r'^(.*).amos$|ssemos$') 
  paro = re.compile(r'^(.*).eis$|reis$|sseis')
  oxi = re.compile(r'^(.*).ara$|ira$|rao$|ras$') # ra e ras com problema 
  palavra = normalize('NFKD', palavra).encode('ASCII','ignore').decode('ASCII')
  if(propa.search(palavra)):
    return "proparoxítona"
  elif(paro.search(palavra)):
    return "paroxítona"
  elif(oxi.search(palavra)):
    return "oxítona"
  else:
    return 0
  return 0
def terminacao(palavra,classe):
  mono = re.compile(r'^(.*).a$|as$|a$|as$|e$|es$|o$|os$')
  oxi =  re.compile(r'^(.*).a$|as$|e$|es$|o$|os$|em$|ens$')
  paro =  re.compile(r'^(.*).i$|is$|us$|r$|l$|x$|n$|um$|uns$|ão$|ãos$|ã$|ãs$|ps$|on$|ons$')
  acento = re.compile('à|[á-ú]|ê|ô|ã|õ|í') 
  x='';
  monon =0
  oxin =0
  paron=0
  propan=0
  totalp = 0
  outro = 0
  nan = 0
  acen=0
  noxi=0
  nparo=0
  nmono=0
  j = palavra
  x = normalize('NFKD', palavra).encode('ASCII','ignore').decode('ASCII')
  #if(acento.search(str(j))):
  if(classe=='oxítona'):
    if(oxi.search(str(x))):
      return "oxítona"
  elif(classe=='paroxítona'):  
    if(paro.search(j)):
      return "paroxítona"
  elif(classe=='proparoxítona'):
    return "proparoxítona"
  return 0
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
    if(not palavras):
      temp = {
      'PALAVRAVOP':k,
      'PALAVRAANT':k,
      'SILABA': 'NAN',
      'CLASSE':'NAN'
      }
      dataNova.append(temp)
    else:
      aux=0
      for i in palavras:
        link=re.sub('<[^>]+?>', '', str(i.find('a')))
        pala = i.text.replace(" ",'').split('\n')[0]
        palavraNormalizada = normalize('NFKD', link).encode('ASCII','ignore').decode('ASCII')
        if(palavraNormalizada == busca):
          forte =  re.sub('<[^>]+?>', '', str(i.find('u')))
          silaba = pala.split(')')[1]
          silsepara = silaba.split('·')
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
              'PALAVRAVOP':link,
              'PALAVRAANT':k,
              'SILABA':silaba,
              'CLASSE':classe
          }
          dataNova.append(temp)
          t=1
          break
        if(t==1):
          break   
  return dataNova
@app.route('/handle_data', methods=['POST'])
def handle_data():
  texto = request.form.get('texto')
  titulo = request.form['titulo']
  cleantext = re.compile('<.*?>|[!-.:-@]')
  texto = re.sub(cleantext, '', texto)
  nlp = spacy.load("pt")
  conteudo = nlp(texto)
  texto = conteudo.text.split()
  retorno =faz_busca(texto)
  for j in range(len(retorno)):
    num = Verbos(retorno[j]['PALAVRAANT'])
    if(num==0):
      retorno[j]['REGRAVERB']="palavra não verbo"
    else:
      retorno[j]['REGRAVERB']=num
    num = terminacao(retorno[j]['PALAVRAANT'],retorno[j]['CLASSE'])
    if(num==0):
      retorno[j]['REGRANaoVERB']="Terminação não bate com a regra"
    else:
      retorno[j]['REGRANaoVERB']= num
  return render_template('mostraconteudo.html',titulo = titulo,texto = retorno)
@app.route('/VOP')
def VOP():
  lista={'fertil','amor','aviao','insuficiencia','quente','amavamos'}
  retorno =faz_busca(lista)
  rt = retorno.copy()
  for i in rt:
    num = Verbos(i['PALAVRAANT'])
    if(num==0):
      i['REGRAVERB']="palavra não verbo"
    else:
      i['REGRAVERB']=num
    num = terminacao(i['PALAVRAANT'],i['CLASSE'])
    if(num==0):
      i['REGRANaoVERB']="Terminação não bate com a regra"
    else:
      i['REGRANaoVERB']= num
  return render_template('processa.html',retorno = rt)
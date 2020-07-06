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


def Monossilaba(palavra):
  mono = {'já','tão'}
  for x in mono:
    pala =  normalize('NFKD', x).encode('ASCII','ignore').decode('ASCII')
    if(palavra==pala):
      return "Monossílaba que deve receber acento. Você escreveu ",palavra, " mas o correto seria ",x," "
  return 0 
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
  monossílaba = re.compile(r'^(.*).a$|as$|a$|as$|e$|es$|o$|os$')
  oxítona     =  re.compile(r'^(.*).a$|as$|e$|es$|o$|os$|em$|ens$')
  paroxítona  =  re.compile(r'^(.*).i$|is$|us$|r$|l$|x$|n$|um$|uns$|ão$|ãos$|ã$|ãs$|ps$|on$|ons$')
  
  
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
    if(oxítona.search(str(x))):
      return "Palavra classificada como oxítona, pela sílaba mais forte e terminação"
  elif(classe=='paroxítona'):  
    if(paroxítona.search(j)):
      return "Palavra classificada como paroxítona, pela sílaba mais forte e terminação"
  elif(classe=='proparoxítona'):
    return "Palavra classificada como proparoxítona, pela sílaba mais forte"
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
    if(not palavras or len(k)==1):
      temp = {
      'PALAVRAANT':k,
      'PALAVRAVOP':'NAN',
      'SILABA': 'NAN',
      'CLASSE':'NAN',
      'FORTE': 'NAN',
      'MONOSSILABA':0
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
              'FORTE': normalize('NFKD', str(forte)).encode('ASCII','ignore').decode('ASCII'),
              'MONOSSILABA':mono
          }
          dataNova.append(temp)
          t=1
          break
        if(t==1):
          break
      if(t!=1):
        temp = {
        'PALAVRAANT':k,
        'PALAVRAVOP':'NAN',
        'SILABA': 'NAN',
        'CLASSE':'NAN',
        'FORTE': 'NAN',
        'MONOSSILABA':0
        }
        dataNova.append(temp) 
  return dataNova
@app.route('/handle_data', methods=['POST'])
def handle_data():
  texto = request.form.get('texto')
  titulo = request.form['titulo']
  cleantext = re.compile('<.*?>|[!-.:-@]')
  texto = re.sub(cleantext, '', texto)
  nlp = spacy.load("pt_core_news_sm")
  conteudo = nlp(texto)
  texto = conteudo.text.split()
  retorno =faz_busca(texto)
  inicio = time.time()
  for j in range(len(retorno)):
    if(retorno[j]['PALAVRAVOP']=='NAN'):
      retorno[j]['REGRAVERB'] =  Verbos(retorno[j]['PALAVRAANT'])
      retorno[j]['REGRANaoVERB'] = 0
    else:
      retorno[j]['REGRAVERB'] =  Verbos(retorno[j]['PALAVRAANT'])
      retorno[j]['REGRANaoVERB'] = terminacao(retorno[j]['PALAVRAANT'],retorno[j]['CLASSE'])

    if(retorno[j]['REGRAVERB']==0 and retorno[j]['REGRANaoVERB']==0 and retorno[j]['PALAVRAVOP']=='NAN' ):
      retorno[j]['n']= 'palavra não classificada'

  final=time.time()
  t = final-inicio
  return render_template('mostraconteudo.html',titulo = titulo,texto = retorno,t=t)
@app.route('/VOP')
def VOP():
  lista={'fertil','amor','aviao','insuficiencia','quente','amavamos','hoje','tao','o'}
  retorno =faz_busca(lista)
  rt = retorno.copy()
  t = len(lista)
  return render_template('processa.html',retorno = retorno,t=t)
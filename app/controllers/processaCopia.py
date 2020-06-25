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
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
#cors = CORS(app, resource={r"/*":{"origins": "*"}})


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
      'PALAVRA':busca,
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
  
  return render_template('mostraconteudo.html',titulo = titulo,texto = texto)
@app.route('/VOP')
def VOP():
  lista={'fertil','amor','avião','insuficiencia','quente'}
  retorno =faz_busca(lista)
  data = pd.DataFrame(retorno)
  return render_template('processa.html',retorno = retorno)
@app.route('/RARA')
def RARA():
  lista ='avião'
  return render_template('novo.html',retorno = lista)
@app.route('/PROCE')
def PROCE():
  lista={'fertil','amor','avião','insuficiencia','quente'}
  retorno =faz_busca(lista)
  data = pd.DataFrame(retorno)
  for (i,row) in data.iterrows():
    p = row['PALAVRA']
    c = row['CLASSE']
  return render_template('processa.html',retorno = retorno)
@app.route('/RER')
def RER():
  texto = 'Quinze anos! é a idade das primeiras palpitações, a idade dos sonhos, a idade das ilusões amorosas, a idade de Julieta; é a flor, é a vida, e a esperança, o céu azul, o campo verde, o lago tranqüilo, a aurora que rompe, a calhandra que canta, Romeu que desce a escada de seda, o último beijo que as brisas da manhã ouvem e levam, como um eco, ao céu.'
  tokenizer = RegexpTokenizer('\w+|\$[\d\.][\d\.]+|\S+/[, ]')
  tre =  word_tokenize(str(texto))
  return render_template('token.html',retorno = tre)
def Verbos(palavra):
  propa = re.compile(r'^(.*).amos$|ssemos$') 
  paro = re.compile(r'^(.*).eis$|reis$|sseis')
  oxi = re.compile(r'^(.*).ara$|ira$|rao$|ras$') # ra e ras com problema 
  palavra = normalize('NFKD', palavra).encode('ASCII','ignore').decode('ASCII')
  if(propa.search(palavra)):
    return 1
  elif(paro.search(palavra)):
    return 2
  elif(oxi.search(palavra)):
    return 3
  else:
    #print('não entrou em regra de acentuação de verbo\n')
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
  if(acento.search(str(j))):
    if(classe=='oxítona'):
      if(oxi.search(str(x))):
        return 1
    elif(classe=='paroxítona'):  
      if(paro.search(j)):
        return 2
        #data.at[i,"REGRA"]="Regra por terminação paroxítona"
    elif(classe=='proparoxítona'):
      return 3
      #data.at[i,"REGRA"]="Regra todo proparoxítona é acentuada"
  return 0
import os
import re
import pandas as pd
import time
import requests
import spacy
import nltk
from spacy.tokenizer import Tokenizer
from bs4 import BeautifulSoup
from unicodedata import normalize
from flask import render_template
from app import app
from flask import request
from re import match as re_match
from re import compile as re_compile
import re
nltk.download('stopwords')
def isdigit(s):
  comp = re_compile("^\d+?\.\d+?$")    
  if comp.match(s) is None:
    return s.isdigit()
  return True
def Monossilaba(palavra):
  excessao = { 'essa','ouro','ao','ela','do','se','para','boi','de','oi','ei','e','é','um','flor','ler','leu','mas','pai','meu','dor','bem','bom','luz','mar','mau','sol','trem','vez','voz','sim','ar','oi','cor','mel','dom','sul','mil','sons','tu','que','vi','ver','vou'}
  mono = {'pá','má','lá','cá','chás','já','há','fãs','lã','sã','pé','ré','vê','lê','sê','dê','crê','mês','três','fé','pó','só','nó','dó','cós','pôs','pós','nós','vós','réis','méis','géis','dói','mói','rói','sóis','vós','cão','são','fã','há','fãs','chá','nós','mãe','pão','mão','lá','pé','céu','tão'}
  x = normalize('NFKD', palavra).encode('ASCII','ignore').decode('ASCII').lower()
  for y in mono:
    if(x== normalize('NFKD', y).encode('ASCII','ignore').decode('ASCII').lower()):
      return "Palavra classificada como monossílaba"
  if(x in excessao):
    return 0
  else:
    monossílaba = re.compile(r'^(.*).a$|as$|e$|es$|o$|os$|ei$|eu$|oi$')
    if(monossílaba.search(str(x)) or x in mono ):
      return "Palavra classificada como monossílaba, e deve ser acentuada pela regra da terminação"
    return 0
def Verbos(palavra,retorno):
  propa = re.compile(r'^(.*).amos$|ssemos$') 
  paro = re.compile(r'^(.*).reis$|sseis') # eis tem que ver o que vai ser feito
  oxi = re.compile(r'^(.*).ara$|ira$|rao$|aras$') # ra e ras com problema 
  vogal = re.compile(r'[a|e|i|o|u]$')
  vogal2 = re.compile(r'^.[a|e|i|o|u]$')
  pattern = '^(.*).[amamos|ssemos|eis|reis|sseis|rao|ara|aras]$'
  result = re.match(pattern, palavra)
  acento = re.compile('à|[á-ú]|ê|ô|ã|õ|í') 
  if(acento.search(palavra)):
    return 0
  else:
    if result:
      if(oxi.search(palavra)):
        forte = ' '.join(re.findall(r'.{3}$',palavra))
        if(vogal.search(forte[0])):
          forte = forte[1:]
      else:
        result = re.split('amos|ssemos|eis|reis|sseis|ara|aras', palavra)
        if(oxi.search(palavra)):
          if(result[1]=='ara' or result[1]=='aras'):
            forte = ' '.join(result[1][1:])
          else:  
            forte = ' '.join(result[1])
        else:
          if(vogal.search(result[0])):
            forte = ' '.join(re.findall(r'.{2}$',result[0]))
          else:
            forte = ' '.join(re.findall(r'.{2}$',re.sub(r'\w$','',result[0])))
      retorno['FORTE']=forte      
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
  oxítona     =  re.compile(r'^(.*).a$|as$|e$|es$|o$|os$|em$|ens$|eis$|eu$|eus$|oi$|ois$')
  #|i$|is$|us$|u$| oxitona com vogal antes
  paroxítona  =  re.compile(r'^(.*).i$|is$|us$|r$|l$|x$|n$|um$|uns$|ão$|ãos$|ã$|ãs$|ps$|on$|ons$')
  #nao se acentuada ei oi
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
  comuns = set()
  dataNova=[]
  valorTime=0
  count=0
  acento = re.compile('à|[á-ú]|ê|ô|ã|õ|í') 
  for k in token:
    count+=1
    valorTime+=1
    t=0
    busca = normalize('NFKD', str(k).lower()).encode('ASCII','ignore').decode('ASCII')
    if(len(busca)>3 and (not isdigit(busca))):
      page = requests.get('http://www.portaldalinguaportuguesa.org/index.php?action=syllables&act=list&search='+busca)
      soup = BeautifulSoup(page.text, 'html.parser')
      palavras = soup.find_all('td',{'title':'Palavra'}) 
      classe=''
      if(not palavras or len(k)==1):
        if(not palavras and busca[len(busca) -1]=='s' ):
          ultimaletra = busca[:-1] 
          page = requests.get('http://www.portaldalinguaportuguesa.org/index.php?action=syllables&act=list&search='+ultimaletra)
          soup = BeautifulSoup(page.text, 'html.parser')
          novapalavras = soup.find_all('td',{'title':'Palavra'}) 
        else:
          temp = {
          'PALAVRAANT':k.lower(),
          'PALAVRAVOP':'NAN',
          'SILABA': 'NAN',
          'CLASSE':'NAN',
          'FORTE': 'NAN',
          'MONOSSILABA':0,
          'ACENTO':1
          }
          dataNova.append(temp)
      else:
        aux=0
        for i in palavras:
          link=re.sub('<[^>]+?>', '', str(i.find('a')))
          pala = i.text.replace(" ",'').split('\n')[0]
          palavraNormalizada = normalize('NFKD', link).encode('ASCII','ignore').decode('ASCII').lower()
          if(palavraNormalizada == busca):
            if(not acento.search(str(link))):
              t=1
              temp = {
                'PALAVRAANT':k.lower(),
                'PALAVRAVOP':'NAN',
                'SILABA': 'NAN',
                'CLASSE':'NAN',
                'FORTE': 'NAN',
                'MONOSSILABA':0,
                'ACENTO':0
              }
              dataNova.append(temp)
              break
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
                'PALAVRAANT':k.lower(),
                'PALAVRAVOP':link.lower(),
                'SILABA':silaba,
                'CLASSE':classe,
                'FORTE': normalize('NFKD', str(forte)).encode('ASCII','ignore').decode('ASCII'),
                'MONOSSILABA':mono,
                'ACENTO':1
            }
            dataNova.append(temp)
            t=1
            break
          if(t==1):
            break
        if(t!=1):   
          temp = {
          'PALAVRAANT':k.lower(),
          'PALAVRAVOP':'NAN',
          'SILABA': 'NAN',
          'CLASSE':'NAN',
          'FORTE': 'NAN',
          'MONOSSILABA':0,
          'ACENTO':1
          }
          dataNova.append(temp)
    else:
      if( isdigit(busca)):
        comuns.add(busca)
      else:
        temp = {
          'PALAVRAANT':k.lower(),
          'PALAVRAVOP':'NAN',
          'SILABA': 'NAN',
          'CLASSE':'NAN',
          'FORTE': 'NAN',
          'MONOSSILABA':0,
          'ACENTO':0
        }
        
        dataNova.append(temp)
  return dataNova
@app.route('/processamento', methods=['POST'])
def processamento():
  acento = re.compile('à|[á-ú]|ê|ô|ã|õ|í') 
  texto = request.form.get('message')
  titulo = request.form['titulo']
  cleantext = re.compile('<.*?>|[!-.:-@]')
  texto = re.sub(cleantext, '', texto)
  nlp = spacy.load("pt_core_news_sm")
  conteudo = nlp(texto)
  texto = conteudo.text.split()
  stopwords = nltk.corpus.stopwords.words('portuguese')
  all_stopwords = nlp.Defaults.stop_words
  copytexto = texto.copy()
  for x in copytexto:
    if(x in stopwords or x in all_stopwords):
      texto.remove(x)
  retorno =faz_busca(texto)
  inicio = time.time()
  ex = []
  rt = retorno.copy()
  for j in range(len(retorno)):
    if(len(retorno[j]['PALAVRAANT'])<=3 and retorno[j]['PALAVRAVOP']=='NAN' ):
      retorno[j]['REGRAVERB'] = 0
      retorno[j]['REGRANaoVERB'] = 0
      retorno[j]['MONOSSILABA'] = Monossilaba(retorno[j]['PALAVRAANT'])
    else:
      retorno[j]['MONOSSILABA']=1
      if(retorno[j]['PALAVRAVOP']=='NAN'):
        retorno[j]['REGRAVERB'] =  Verbos(retorno[j]['PALAVRAANT'],retorno[j])
        retorno[j]['REGRANaoVERB'] = 0
        if(retorno[j]['REGRAVERB']==0 and retorno[j]['REGRANaoVERB']==0 and retorno[j]['ACENTO']!=0):
          retorno[j]['n']= 'palavra não classificada'
          ex.append(retorno[j]['PALAVRAANT'])
      else:
        retorno[j]['REGRAVERB'] =  Verbos(retorno[j]['PALAVRAANT'],retorno[j])
        retorno[j]['REGRANaoVERB'] = terminacao(retorno[j]['PALAVRAANT'],retorno[j]['CLASSE'])
  final=time.time()
  t = final-inicio
  return render_template('processaTexto.html',titulo = titulo,texto = retorno,t=t,ex=ex)
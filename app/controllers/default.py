import os
import nltk
import spacy
from flask_cors import CORS
from flask import render_template
from app import app
from urllib import request
from flask import request
nltk.download('stopwords')
nlp2 = spacy.load('pt_core_news_sm')
cors = CORS(app, resource={r"/*":{"origins": "*"}})

@app.route('/')
def index():
    return render_template('teste.html')
@app.route('/stop')
def stop():
    texto = 'Em 2014, durante o governo Dilma Rousseff, iniciava a operação Lava Jato Jato, que tinha o objetivo de investigar casos de corrupção envolvendo empresas estatais, como: a como a Petrobras. Em virtude disso, várias notícias relatando a participação de políticos em esquemas fraudulentos começaram a surgir e causar indignação na população. Por conseguinte, o anseio da sociedade em acompanhar os desdobramentos desses fatos ocasionaram ocasionou a notoriedade do Supremo Tribunal Federal. Mormente, ao avaliar que, o que o papel desse órgão judiciário, consiste judiciário consiste na guarda da Constituição Federal e no julgamento de ocorrências concernentes ao Congresso Nacional ou há a casos que sejam relevantes para todo o país. Nessa conjectura, é indiscutível a importância das atribuições do Supremo Tribunal Federal, visto que algumas pautas, como: a como a criminalização da homofobia, trouxeram grandes avanços para a sociedade. Entretanto, processos envolvendo ex-presidentes, ministros e ex-assessores ganharam destaque em âmbito nacional devido a à postura dos membros da corte. Ademais, convém salientar que, segundo o instituto Datafolha, 39% dos brasileiros desaprovam a conduta do Supremo Tribunal Federal, pois vereditos e decisões questionáveis questionáveis, homologadas pelo órgão, como: a como a suspensão de investigações contra políticos, absolvição e soltura de indivíduos presos em operações judiciais policiais e aprovação de habeas corpus controversos são fatores corroborantes para o resultaram no aumento da taxa de reprovação da corte.Dado o exposto, faz-se necessário necessária, mediante o Ministério de Ciência e Tecnologia em parceria com o Supremo Tribunal Federal, a ampliação de fóruns virtuais para difundir as atribuições e deveres desse órgão público público, a fim de policiar e informar a sociedade sobre as pautas discutidas pela corte. Consoante ao ex presidente africano Como disse o ex-presidente sul-africano Nelson Mandela, "Se falares uma linguagem que o homem compreenda, a tua mensagem entrará em outras mentes", diante mentes". Diante disso, é fundamental a parceria do STF com os veículos de comunicação, para propagar propagar, numa linguagem sucinta e objetiva objetiva, mensagens que visem a aproximação amigável entre a população e o Supremo Tribunal Federal.'
    conteudo = nlp2(texto)
    texto = conteudo.text.split()
    stopwords = nltk.corpus.stopwords.words('portuguese')
    all_stopwords = nlp2.Defaults.stop_words
    copytexto = texto.copy()
    for x in copytexto:
        if(x in stopwords or x in all_stopwords):
           texto.remove(x)
    return render_template('aa.html',nltk=texto)
@app.route('/teste')
def teste():
    texto = 'bla'
    titulo = 'new'
    return render_template('processaTexto.html',texto=texto,titulo=titulo)
@app.route('/escreveTexto')
def escreveTexto():
    return render_template('escreveTexto.html')
@app.route('/dicas')
def dicas():
    return render_template('dicas.html')
@app.route('/topico')
def topico():
    return render_template('topico1000.html')
@app.route('/regrasAcentuacao')
def regrasAcentuacao():
    return render_template('regrasAcentuacao.html')
@app.route('/podcast')
def podcast():
    return render_template('podcasts.html')
@app.route('/curiosidades')
def curiosidades():
    return render_template('curiosidades.html')

def main():
    port = int(os.environ.get("PORT", 5000))
if __name__ == "__main__":
    main()
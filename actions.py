
# main() será executado quando você chamar essa ação
#
# @param As ações do Cloud Functions aceitam um único parâmetro, que deve ser um objeto JSON.
#
# @return A saída dessa ação, que deve ser um objeto JSON.
#
#
import sys
import urllib.request, json 
import datetime
ALPHAVANTAGE_API_KEY = '' # inseria a key da API ALPHAVANTAGE


def main(dict):
    acao = dict['acao']
    passo = dict['passo']
    
    
###############################
 
        
    def get_busca(acao):
        global retorno
        url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={acao}&apikey={ALPHAVANTAGE_API_KEY}'
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())
        len_list_data = len(data['bestMatches'])   
        
        def get_opcao(len_list_data):
            global retorno
            text = 'Pode ocorrer de o nome usado por mim na busca ser diferente do nome oficial da ação.\n Por isto confirme o nome da ação exatamente conforme está na lista de confirmação abaixo.'
            text_blank = '-----------------'
            for i in range(len_list_data):
                symbol = data['bestMatches'][i]['1. symbol']
                nome = data['bestMatches'][i]['2. name']
                regiao = data['bestMatches'][i]['4. region']
                moeda = data['bestMatches'][i]["8. currency"]
                texti = 'Nome da ação: '+ symbol +'\n'+ 'Nome da companhia: ' + nome +'\n'+'Região: '+regiao+'\n'+'Moeda: '+moeda
                text = text + '\n'+ text_blank +'\n'+ texti
            text = text+ '\n'+ text_blank +'\n'+'Por favor confirme a ação que deseja a cotação digitando um dos nome da ação apresentados na lista de confirmação acima.'
            text_primeiro = text
            retorno = {'text_primeiro':text_primeiro}
        
        
        if len_list_data == 0:
            retorno = {'text_primeiro':f'Não foi encontrado nenhum ativo similar à {acao}. \n Por favor digite outro nome de ação.'}
        else:
            get_opcao(len_list_data)      
        
################################
 
    def get_cotacao(ativo):
        global retorno
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ativo}&apikey={ALPHAVANTAGE_API_KEY}'
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())
        len_list_data = len(data['Global Quote'])
        
        def get_cotacao_resultado(len_list_data, ativo):
            global retorno
            preco = data['Global Quote']['05. price']
            preco = str(round(float(preco),2)).replace(',',';')
            preco = preco.replace('.',',')
            preco = preco.replace(';','.')
            volume = data['Global Quote']['06. volume']
            ultima_negociacao = data['Global Quote']['07. latest trading day']
            ultima_negociacao = datetime.datetime.strptime(ultima_negociacao, '%Y-%m-%d').strftime('%d/%m/%Y')
            fechamento_anterior = data['Global Quote']['08. previous close']
            fechamento_anterior = str(round(float(fechamento_anterior),2)).replace(',',';')
            fechamento_anterior = fechamento_anterior.replace('.',',')
            fechamento_anterior = fechamento_anterior.replace(';','.')
            text_segundo = 'Ação: '+ativo+'\n'+'Preço: '+preco+'\n'+'Fechamento anterior: '+fechamento_anterior+'\n'+'Volume de ações negociados : '+volume+'\n'+'Data da última transação: '+ultima_negociacao
            
            retorno = {'text_segundo':text_segundo}
        
        if len_list_data == 0:
            retorno = {'text_segundo':f'Desculpa não foi encontrado cotação para a ação {acao}\n O nome da ação foi digitada incorretamente ou não está disponível para consulta.'}
        else:
            get_cotacao_resultado(len_list_data, acao) 
    
 ######################################   
 
    if passo == 'primeiro':
        get_busca(acao)
    elif passo =='segundo':
        get_cotacao(acao)
    
    
    return retorno
    
    
    
    

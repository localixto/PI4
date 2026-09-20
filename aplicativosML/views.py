from django.shortcuts import render
from . models import Dados_Apontamentos
from django.http import HttpResponse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# Create your views here.
def algoritmoNB(request):
    dados = Dados_Apontamentos.objects.values('cidade', 'status')
    df=pd.DataFrame.from_records(dados)

    # converte cidade para números
    unicidade_cidade=df['cidade'].unique()
    cidade_map={cid: i for i, cid in enumerate(unicidade_cidade)}
    df['cidade_numero']=df['cidade'].map(cidade_map) 

    # converte status para números
    unicidade_status=df['status'].unique()
    status_map={sta: k for k, sta in enumerate(unicidade_status)}
    df['status_numero']=df['status'].map(status_map) 

    df.drop(columns=['cidade', 'status'])
    #Início do Naive Bayes
    
    X,y=df['cidade_numero'],df['status_numero']

    X_treino,X_teste,y_treino,y_teste=train_test_split(X,y, test_size=0.2, random_state=42)
    #Converte as variáveis para matrizes, pois a função fit não aceita dados unidimensionais
    X_treino=np.array(X_treino).reshape(-1,1)
    X_teste=np.array(X_teste).reshape(-1,1)

    modeloNB=MultinomialNB()
    modeloNB.fit(X_treino, y_treino)

    y_predito=modeloNB.predict(X_teste)

    print(f"Acurácia: {accuracy_score(y_teste,y_predito):.2f}")
         
    #print(X_treino)
    #print(y_treino)

    return HttpResponse('Rodou!')
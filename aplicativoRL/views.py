from django.http import HttpResponse
from aplicativosML.models import Dados_Apontamentos 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from imblearn.over_sampling import SMOTE

def executarRegressaoLogistica(request):    

    # Buscar os dados usando o ORM do Django.
    campos_do_banco = ['cpf_cnpj', 'cidade', 'codigo_cartorio', 'valor_original', 'valor_enviado', 'status']
    dados = Dados_Apontamentos.objects.values(*campos_do_banco)
    df = pd.DataFrame.from_records(dados)   

    # Limpar espaços das colunas
    df.columns = df.columns.str.strip()

    # Tratamento e padronização das classes de Status
    df['status'] = df['status'].replace('RECEBIDO PELO CARTÓRIO', 'PROTESTADO')
    df['status'] = df['status'].replace('PAGO PELO DEVEDOR', 'REPASSADO AO CREDOR')
    df['status'] = df['status'].replace('RETIRADO', 'CANCELADO')      

    # Definimos a coluna alvo de forma fixa e limpa
    target_col = 'status'

    # Converter alvo em binário
    y = df[target_col].apply(lambda x: 1 if str(x).upper() == "PROTESTADO" else 0)

    # Converter colunas não numéricas em números de forma limpa
    for col in df.select_dtypes(include=['object', 'string']).columns:
        if col != target_col:
            try:
                df[col] = pd.to_datetime(df[col], dayfirst=True, errors='raise').map(lambda x: x.toordinal())
            except Exception:
                df[col] = LabelEncoder().fit_transform(df[col])

    # Definir as variáveis explicativas removendo a coluna alvo
    X = df.drop(target_col, axis=1)

    # Divisão treino/teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Balanceamento com SMOTE
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

    # Padronização dos dados
    scaler = StandardScaler()
    X_resampled_scaled = scaler.fit_transform(X_resampled)
    X_test_scaled = scaler.transform(X_test)

    # Treinar modelo (Regressão Logística)
    model = LogisticRegression(max_iter=1000, class_weight='balanced')
    model.fit(X_resampled_scaled, y_resampled)

    # Executa as predições nos bastidores
    y_pred = model.predict(X_test_scaled)

    # Resultados finais no terminal
    print("\n=== RESULTADOS REGRESSÃO LOGÍSTICA ===")
    print("Acurácia:", round(accuracy_score(y_test, y_pred), 4))
    print("\nMatriz de confusão:\n", confusion_matrix(y_test, y_pred))
    print("\nRelatório de classificação:\n", classification_report(y_test, y_pred, target_names=["NÃO-PROTESTADO", "PROTESTADO"], zero_division=0))


    # Capturar dados para enviar para HTTP
    acuracia_valor = round(accuracy_score(y_test, y_pred), 4)
    matriz_valores = confusion_matrix(y_test, y_pred)
    relatorio_texto = classification_report(y_test, y_pred, target_names=["NÃO-PROTESTADO", "PROTESTADO"], zero_division=0)

    # Exibir conteúdo na tela do navegador 
    conteudo_http = f"""
    <html>
    <head><title>Métricas - Regressão Logística</title></head>
    <body style="font-family: monospace; margin: 30px; background-color: #1e1e1e; color: #d4d4d4; line-height: 1.5;">
        <div style="max-width: 800px; margin: 0 auto;">
            <h2 style="color: #4fc1ff; border-bottom: 1px solid #3e3e3e; padding-bottom: 10px;">=== RESULTADOS REGRESSÃO LOGÍSTICA ===</h2>
            <p style="font-size: 16px;"><strong style="color: #9cdcfe;">Acurácia:</strong> {acuracia_valor}</p>
            
            <h3 style="color: #4fc1ff; margin-top: 30px;">Matriz de confusão:</h3>
            <pre style="background-color: #252526; padding: 15px; border-radius: 5px; border-left: 4px solid #ce9178; color: #dcdcaa; font-size: 14px;">{matriz_valores}</pre>
            
            <h3 style="color: #4fc1ff; margin-top: 30px;">Relatório de classificação:</h3>
            <pre style="background-color: #252526; padding: 15px; border-radius: 5px; border-left: 4px solid #4ec9b0; color: #d4d4d4; font-size: 14px;">{relatorio_texto}</pre>
        </div>
    </body>
    </html>
    """    
    return HttpResponse(conteudo_http)

    
    

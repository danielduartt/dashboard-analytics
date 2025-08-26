import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os 

print("Iniciando a geração dos dados para o projeto de Arrecadação...")

# --- PARÂMETROS DE CONFIGURAÇÃO ---
NUMERO_DE_PAGAMENTOS = 2500
NUMERO_DE_CLIENTES = 300
DATA_INICIAL = datetime(2023, 1, 1)
DATA_FINAL = datetime.now()

# --- 1. CRIANDO A TABELA dCanais_Pagamento ---
canais_data = {
    'ID_Canal': [1, 2, 3, 4],
    'Nome_Canal': ['Pix', 'Boleto Bancário', 'Cartão de Crédito', 'Débito Automático'],
    'Custo_Transacao_Percentual': [0.001, 0.0, 0.025, 0.015],
    'Custo_Transacao_Fixo': [0.10, 2.75, 0.50, 0.35]
}
dCanais_Pagamento = pd.DataFrame(canais_data)
print("Tabela 'dCanais_Pagamento' criada.")

# --- 2. CRIANDO A TABELA dClientes ---
clientes_ids = [f'CLI-{str(i).zfill(4)}' for i in range(1, NUMERO_DE_CLIENTES + 1)]
cidades = ['São Luís', 'Imperatriz', 'São José de Ribamar', 'Timon', 'Caxias', 'Paço do Lumiar', 'Açailândia', 'Bacabal', 'Balsas']
tipos_cliente = ['Residencial', 'Comercial']

clientes_data = {
    'ID_Cliente': clientes_ids,
    'Cidade': [random.choice(cidades) for _ in range(NUMERO_DE_CLIENTES)],
    'Estado': 'MA',
    'Tipo_Cliente': [random.choice(tipos_cliente) for _ in range(NUMERO_DE_CLIENTES)]
}
dClientes = pd.DataFrame(clientes_data)
print("Tabela 'dClientes' criada.")

# --- 3. CRIANDO A TABELA fPagamentos (COM SUJEIRA INTENCIONAL) ---
pagamentos_lista = []
total_dias = (DATA_FINAL - DATA_INICIAL).days

for i in range(1, NUMERO_DE_PAGAMENTOS + 1):
    id_fatura = 1000 + i
    data_vencimento = DATA_INICIAL + timedelta(days=random.randint(0, total_dias))
    
    pago = random.random() < 0.85 
    if pago:
        dias_diferenca_pagamento = random.randint(-5, 20)
        data_pagamento = data_vencimento + timedelta(days=dias_diferenca_pagamento)
    else:
        data_pagamento = None
        
    valor_fatura = round(random.uniform(80.50, 650.75), 2)
    id_cliente = random.choice(clientes_ids)
    id_canal = random.choice(dCanais_Pagamento['ID_Canal'])
    
    pagamentos_lista.append({
        'ID_Fatura': id_fatura,
        'Data_Vencimento': data_vencimento,
        'Data_Pagamento': data_pagamento,
        'Valor_Fatura': valor_fatura,
        'ID_Cliente': id_cliente,
        'ID_Canal': id_canal
    })

fPagamentos = pd.DataFrame(pagamentos_lista)

print("Adicionando 'sujeira' intencional nos dados...")
for index in fPagamentos.sample(frac=0.1).index:
    valor = fPagamentos.at[index, 'Valor_Fatura']
    fPagamentos.at[index, 'Valor_Fatura_Formatado'] = f'R$ {valor:.2f}'.replace('.', ',')

for index in fPagamentos.sample(frac=0.15).index:
    data = fPagamentos.at[index, 'Data_Vencimento']
    if pd.notnull(data):
        fPagamentos.at[index, 'Data_Vencimento'] = data.strftime('%d/%m/%Y')

fPagamentos['Data_Pagamento'] = pd.to_datetime(fPagamentos['Data_Pagamento'])
print("Tabela 'fPagamentos' criada.")

# Certifique-se de que a pasta 'data' existe
os.makedirs('data', exist_ok=True)

# --- 4. SALVANDO OS ARQUIVOS EXCEL ---
dCanais_Pagamento.to_excel('data/dCanais_Pagamento.xlsx', index=False, sheet_name='Canais')
dClientes.to_excel('data/dClientes.xlsx', index=False, sheet_name='Clientes')
fPagamentos.to_excel('data/fPagamentos.xlsx', index=False, sheet_name='Pagamentos')

print("\nArquivos gerados na pasta 'data'! Você está pronto para começar no Power BI.")
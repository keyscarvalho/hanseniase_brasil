#%%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# %%

df = pd.read_csv('../data/escolaridade.csv', encoding='latin1', sep=';', skiprows=3, skipfooter=18, engine='python')

df.head()

#%%

df.rename(columns={'Ano Diagnóstico' : 'ano_diagnostico', 'Analfabeto' : 'analfabeto'}, inplace=True)

df.head()
#%%

df = (df[df['ano_diagnostico'] != '<1975'].drop(columns=['Não se aplica', 'Total', 'Ign/Branco']).replace('-', 0))

#%%

colunas_escolaridade = df.columns.drop('ano_diagnostico')
df[colunas_escolaridade] = df[colunas_escolaridade].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

#%%

df['fundamental_incompleto'] = df['1ª a 4ª série incompleta do EF'] + df['5ª a 8ª série incompleta do EF']
df['fundamental_completo'] = df['4ª série completa do EF'] + df['Ensino fundamental completo']
df['medio_incompleto'] = df['Ensino médio incompleto']
df['medio_completo'] = df['Ensino médio completo']
df['superior_incompleto'] = df['Educação superior incompleta']
df['superior_completo'] = df['Educação superior completa']

#%%

# Mantém o ano e as colunas agrupadas em formato "tidy"
df_long = pd.melt(
    df,
    id_vars=['ano_diagnostico'],
    value_vars=[
        'analfabeto',
        'fundamental_incompleto',
        'fundamental_completo',
        'medio_incompleto',
        'medio_completo',
        'superior_incompleto',
        'superior_completo'
    ],
    var_name='escolaridade',
    value_name='casos'
)

# Corrigir ano "<1975" para int, se quiser incluir
df_long['ano_diagnostico'] = df_long['ano_diagnostico'].astype(int)
df_long['ano_diagnostico'] = df_long['ano_diagnostico'].astype(int)

#%%

total_escolaridade = df_long.groupby('escolaridade')['casos'].sum().reset_index()
total_escolaridade

#%%

plt.figure(figsize=(10, 6))
sns.barplot(data=total_escolaridade, x='escolaridade', y='casos', color='royalblue')
plt.title('Total de casos por escolaridade')
plt.xlabel('Escolaridade')
plt.ylabel('Total de Casos')
plt.xticks(rotation=90)

plt.tight_layout()

#%%

df_raca_escolaridade = pd.read_csv('total_por_raca.csv')

df_raca_escolaridade.head()

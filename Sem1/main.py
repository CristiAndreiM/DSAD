import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from statistica_inferentiala import testare_normalitate
from functii import nan_replace, standardizare, tabelare_salvare_matrice, calcul_corelatii_covariante

df = pd.read_csv("data_in/Teritorial_2022.csv", sep=',', index_col=0)

variabile = list(df)[3:]

x = df[variabile].values

x = nan_replace(x)#matricea completata

#2
x_std = standardizare(x, True)

#3a
V = np.cov(x, rowvar=False)
tabelare_salvare_matrice(V, variabile, variabile, "Indicatori", "V.csv")
R = np.corrcoef(x, rowvar=False)
tabelare_salvare_matrice(R, variabile, variabile, "Indicatori", "R.csv")

#3b
r, v, clase, = calcul_corelatii_covariante(x, df["Regiunea"].values)

for i in zip(clase, r, v):
    tabelare_salvare_matrice(i[1], variabile, variabile, "Indicatori", "R_" + i[0] + ".csv")
    tabelare_salvare_matrice(i[2], variabile, variabile, "Indicatori", "V_" + i[0] + ".csv")


rezultate_teste = testare_normalitate(x, variabile)

df_teste = pd.DataFrame(rezultate_teste)

df_teste.to_csv("Teste_Normalitate.csv", index=False)

print("\n--- REZULTATE TESTE DE NORMALITATE ---")
print(df_teste)

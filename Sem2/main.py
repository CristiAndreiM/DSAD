import pandas as pd

df_etnii = pd.read_csv("data_in/Ethnicity.csv", index_col=0)
#print(df_etnii)
etnii = list(df_etnii.columns.values[1:])
#print(etnii)

df_coduri_loc = pd.read_csv('data_in/Coduri_Localitati.csv', index_col=0)
df_etnii_loc = df_etnii.merge(df_coduri_loc, left_index=True, right_index=True)
#print(df_etnii_loc.head())

df_etnii_jud = df_etnii_loc[etnii +["County"]].groupby("County").sum()
#print(df_etnii_jud.head())

df_etnii_jud.to_csv('data_out/Ethnicity_Jud.csv')

df_coduri_jud = pd.read_csv('data_in/Coduri_Judete.csv', index_col=0)
#print(df_coduri_jud.head())
df_etnii_jud_reg = df_etnii_jud[etnii].merge(
    df_coduri_jud[["IndicativJudet", "Regiune"]], left_index=True, right_on="IndicativJudet"
)
#print(df_etnii_jud_reg)

df_etnii_reg = df_etnii_jud_reg.groupby(by="Regiune").sum()
df_etnii_reg.to_csv('data_out/Ethnicity_Reg.csv')

df_etnii_p = df_etnii[etnii].apply(func=lambda x: x*100/x.sum(), axis = 1)
#print(df_etnii_p.head());
df_etnii_p.insert(0, "Localitate", df_etnii["City"])
#print(df_etnii_p.head());
df_etnii_p.to_csv('data_out/Ethnicity_P.csv')

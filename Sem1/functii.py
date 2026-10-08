import numpy as np #np pentru calcule matematice
import pandas as pd


def nan_replace(x):
    nr_coloane = x.shape[1]

    for i in range(nr_coloane):
        coloana_curenta = x[:, i]
        unde_lipsesc_date = np.isnan(coloana_curenta)
        media_coloanei = np.nanmean(coloana_curenta)
        coloana_curenta[unde_lipsesc_date] = media_coloanei
    return x

def standardizare(x, scal=True):
    medii = np.mean(x, axis=0)

    x_centrat = x - medii

    if scal:
        deviatii = np.std(x, axis = 0)
        deviatii[deviatii == 0] = 1
        return x_centrat / deviatii
    else:
        return x_centrat

def tabelare_salvare_matrice(matrice, linii, coloane, titlu_index, nume_fisier=None):
    tabel = pd.DataFrame(matrice, index=linii, columns=coloane)
    tabel.index.name = titlu_index
    if nume_fisier is not None:
        tabel.to_csv("data_out/" + nume_fisier)
    else:
        print("To save that data we need to furnize name of file!")

def calcul_corelatii_covariante(x, regiuni):
    regiuni_unice = np.unique(regiuni)
    liste_corelatii = []
    liste_covariante = []

    for regiune_curenta in regiuni_unice:
        pozitii = (regiuni == regiune_curenta)

        date_regiune = x[pozitii]

        r_regiune = np.corrcoef(date_regiune, rowvar=False)
        v_regiune = np.cov(date_regiune, rowvar=False)

        liste_corelatii.append(r_regiune)
        liste_covariante.append(v_regiune)

    return liste_corelatii, liste_covariante, regiuni_unice
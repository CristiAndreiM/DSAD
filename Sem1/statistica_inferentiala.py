import numpy as np
import scipy.stats as stats

def testare_normalitate(x, variabile):
    rezultate = []

    for i, var_nume in enumerate(variabile):
        date_col = x[:, i]
        n = len(date_col)

        # --- 1. TESTUL SHAPIRO-WILK ---
        shapiro_stat, shapiro_p = stats.shapiro(date_col)

        # --- 2. TESTUL KOLMOGOROV-SMIRNOV (KS) ---
        col_std = (date_col - np.mean(date_col)) / (np.std(date_col) if np.std(date_col) != 0 else 1)
        ks_stat, ks_p = stats.kstest(col_std, 'norm')

        # --- 3. TESTUL ANDERSON-DARLING ---
        anderson_res = stats.anderson(date_col, dist='norm')
        anderson_stat = anderson_res.statistic
        valoare_critica_5pct = anderson_res.critical_values[2]
        anderson_trecut = "Da" if anderson_stat < valoare_critica_5pct else "Nu"

        # --- 4. IMPLEMENTARE MANUALĂ TEST CHI2 (Chi-pătrat) ---

        frecvente_observate, margini_intervale = np.histogram(date_col, bins=5)

        media = np.mean(date_col)
        std_dev = np.std(date_col) if np.std(date_col) != 0 else 1

        cdf_valori = stats.norm.cdf(margini_intervale, loc=media, scale=std_dev)
        probabilitati_intervale = np.diff(cdf_valori)

        probabilitati_intervale /= np.sum(probabilitati_intervale)
        frecvente_teoretice = probabilitati_intervale * n

        chi2_stat = np.sum(((frecvente_observate - frecvente_teoretice) ** 2) / (frecvente_teoretice + 1e-5))

        grade_libertate = 2
        chi2_p = stats.chi2.sf(chi2_stat, df=grade_libertate)

        rezultate.append({
            "Variabila": var_nume,
            "Shapiro_p": round(shapiro_p, 4),
            "KS_p": round(ks_p, 4),
            "Anderson_Stat": round(anderson_stat, 4),
            "Anderson_Critic_5%": valoare_critica_5pct,
            "Anderson_Normal": anderson_trecut,
            "Chi2_p": round(chi2_p, 4)
        })

    return rezultate
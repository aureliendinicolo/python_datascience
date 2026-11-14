# Les 3 académies d'Île-de-France, qui forment un seul secteur Parcoursup depuis 2019
ACADEMIES_IDF = ["Paris", "Créteil", "Versailles"]


def taux_poursuite(poursuite, par):
    """Taux de poursuite dans le supérieur (en %) par groupe, par exemple par=["annee", "voie"].

    Comme le recommande la documentation du jeu de données, on somme d'abord les
    poursuivants et les bacheliers du groupe, puis on divise (et non une moyenne de taux).
    """
    sommes = poursuite.groupby(par)[["poursuivants", "bacheliers"]].sum()
    return (sommes["poursuivants"] / sommes["bacheliers"] * 100).round(1)


def part_poursuite_autre_academie_idf(poursuite):
    """Part (en %) des bacheliers franciliens poursuivant dans une autre académie d'Île-de-France.

    Calculée parmi les bacheliers franciliens qui poursuivent dans le supérieur, chaque année.
    Paris, Créteil et Versailles forment une seule région académique : une poursuite dans
    une autre académie francilienne est donc comptée dans poursuivants_autre_academie_meme_region.
    """
    idf = poursuite[poursuite["academie"].isin(ACADEMIES_IDF)]
    sommes = idf.groupby("annee")[["poursuivants_autre_academie_meme_region", "poursuivants"]].sum()
    return (sommes["poursuivants_autre_academie_meme_region"] / sommes["poursuivants"] * 100).round(1)


def part_admis_meme_academie(base, academie):
    """Part (en %) des admis venant de la même académie, dans les formations d'une académie.

    acc_aca_orig : nombre d'admis issus de la même académie que la formation.
    """
    formations = base[base["academie"] == academie]
    sommes = formations.groupby("session")[["acc_aca_orig", "acc_tot"]].sum()
    return (sommes["acc_aca_orig"] / sommes["acc_tot"] * 100).round(1)

def tableau_comp_1(base, selection, total, debut, fin, col_annee = "session", col_etab = "code_UAI"):
    """Tableau (établissement x année) du ratio selection/total,
    avec l'évolution entre la première et la dernière année (qu'on peut choisir).

    selection  : nom de la colonne du numérateur (ex. nb de formations sélectives)
    total      : nom de la colonne du dénominateur (ex. nb total de formations)
    """
    df = base[base[col_annee].between(debut, fin)]

    # Somme par établissement et par année (gère les plusieurs lignes par établissement)
    agg = (df.groupby([col_etab, col_annee])[[selection, total]]
             .sum()
             .reset_index())

    # Ratio, en évitant la division par zéro
    agg["ratio"] = agg[selection] / agg[total].where(agg[total] != 0)

    # Une ligne par établissement, une colonne par année
    tableau = agg.pivot(index=col_etab, columns=col_annee, values="ratio")

    # Évolution entre la première et la dernière année (en points de ratio)
    if debut in tableau.columns and fin in tableau.columns:
        tableau["evolution"] = tableau[fin] - tableau[debut]

    return tableau.round(3)
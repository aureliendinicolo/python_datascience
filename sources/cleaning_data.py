import pandas as pd


# Les 4 façons d'écrire select_form selon les années (sans accent et tronqué en 2020)
CORRESPONDANCE_SELECTIVITE = {
    "formation selective": 1,
    "formation non selec": 0,
    "formation sélective": 1,
    "formation non sélective": 0,
}

# Nomenclature commune des filières : les modalités de fili changent selon les années
# (DUT devient BUT en 2021, PACES devient PASS et LAS en 2020, écoles isolées en 2020)
NOMENCLATURE_FILIERES = {
    "CPGE": "CPGE",
    "BTS": "BTS",
    "DUT": "IUT",
    "BUT": "IUT",
    "Licence": "Licence",
    "Licence_Las": "LAS",
    "PACES": "Santé",
    "PASS": "Santé",
    "Ecole d'Ingénieur": "Ecole d'ingénieur",
    "Ecole de Commerce": "Ecole de commerce",
    "EFTS": "Sanitaire et social",
    "IFSI": "Sanitaire et social",
    "Autre formation": "Autre",
}

# Statut des filières où toutes les formations ont le même entre 2020 et 2025
# (voir le tableau croisé filière x sélectivité dans notebooks/exploration.ipynb).
# Les licences et les LAS sont mixtes : on ne peut pas deviner leur statut.
STATUT_FILIERE = {
    "BTS": 1,
    "CPGE": 1,
    "IUT": 1,
    "Ecole d'ingénieur": 1,
    "Ecole de commerce": 1,
    "Sanitaire et social": 1,
    "Autre": 1,
    "Santé": 0,
}


# Noms d'académie de Parcoursup à corriger pour être identiques toutes les années et
# identiques au fichier du taux de poursuite (Caen et Rouen fusionnent en Normandie en 2020)
CORRECTIONS_ACADEMIES = {
    "Besancon": "Besançon",
    "Caen": "Normandie",
    "Rouen": "Normandie",
    "Réunion": "La Réunion",
}


def ajouter_code(df):
    """Ajoute la colonne code : l'identifiant de la formation, suivi d'une année à l'autre.

    À partir de 2020, il est dans la colonne cod_aff_form.
    En 2018 et 2019, cette colonne n'existe pas : on extrait le code du lien vers la
    fiche Parcoursup (lien_form_psup), qui contient "g_ta_cod=<code>".
    Le code est en float, car il peut manquer (lien vide) et un entier ne peut pas
    contenir de valeur manquante (NaN).
    """
    df = df.copy()
    if "cod_aff_form" in df.columns:
        df["code"] = df["cod_aff_form"].astype(float)
    else:
        df["code"] = df["lien_form_psup"].str.extract(r"g_ta_cod=(\d+)")[0].astype(float)
    return df


def harmoniser_selectivite(df):
    """Ajoute la colonne selective (1 = sélective, 0 = non sélective).

    select_form n'existe qu'à partir de 2020 : pour 2018 et 2019, le tableau est
    renvoyé tel quel, et la sélectivité est ajoutée par completer_2018_2019.
    """
    df = df.copy()
    if "select_form" in df.columns:
        df["selective"] = df["select_form"].map(CORRESPONDANCE_SELECTIVITE)
    return df


def harmoniser_filiere(df):
    """Ajoute la colonne filiere, avec la même nomenclature toutes les années."""
    df = df.copy()
    df["filiere"] = df["fili"].map(NOMENCLATURE_FILIERES)
    return df


def completer_2018_2019(bases):
    """Complète la filière et la sélectivité de 2018 et 2019 à partir de 2020.

    bases : dictionnaire {année: tableau}, où chaque tableau a déjà les colonnes
    code, filiere et selective (pour 2020 et après).
    1. Filière : les écoles d'ingénieurs et de commerce n'apparaissent qu'en 2020 ;
       en 2018-2019 elles sont dans "Autre formation". On reprend leur filière de 2020
       grâce au code.
    2. Sélectivité : on reprend le statut de 2020 grâce au code (il change pour moins
       de 0,1 % des formations par an entre 2020 et 2025). Quand il reste inconnu,
       on utilise la règle par filière (STATUT_FILIERE).
    """
    bases = dict(bases)  # nouveau dictionnaire : celui passé en argument n'est pas modifié
    reference = bases[2020].set_index("code")  # une ligne par code de formation en 2020

    for annee in [2018, 2019]:
        b = bases[annee].copy()

        autre = b["fili"] == "Autre formation"
        b.loc[autre, "filiere"] = b.loc[autre, "code"].map(reference["filiere"]).fillna("Autre")

        b["selective"] = b["code"].map(reference["selective"])
        inconnu = b["selective"].isna()
        b.loc[inconnu, "selective"] = b.loc[inconnu, "filiere"].map(STATUT_FILIERE)

        bases[annee] = b
    return bases


def empiler(bases):
    """Empile les sessions en une seule base : une ligne par formation et par session.

    Ajoute toutes_annees (True si la formation est présente toutes les sessions) et
    remplace la mention "identifiant obsolète" (189 lignes de 2018) par une valeur
    manquante dans cod_uai.
    """
    # ignore_index=True : on renumérote les lignes, sinon l'index aurait des doublons
    base = pd.concat(bases.values(), ignore_index=True)

    nb_sessions = base.dropna(subset=["code"]).groupby("code")["session"].nunique()
    base["toutes_annees"] = base["code"].map(nb_sessions).eq(len(bases))

    base.loc[base["cod_uai"] == "identifiant obsolète", "cod_uai"] = pd.NA
    return base


def harmoniser_academie(base):
    """Ajoute la colonne academie : acad_mies avec les noms corrigés (CORRECTIONS_ACADEMIES)."""
    base = base.copy()
    base["academie"] = base["acad_mies"].replace(CORRECTIONS_ACADEMIES)
    return base


def preparer_base(bases):
    """Enchaîne toutes les étapes et renvoie la base empilée.

    bases : dictionnaire {année: tableau brut}, par exemple le résultat de
    charger_parcoursup pour chaque année.
    """
    bases = {
        annee: harmoniser_filiere(harmoniser_selectivite(ajouter_code(df)))
        for annee, df in bases.items()
    }
    bases = completer_2018_2019(bases)
    return harmoniser_academie(empiler(bases))


def harmoniser_ips(tables):
    """Réunit les 3 fichiers IPS des lycées en un seul tableau aux colonnes identiques.

    Différences entre les fichiers : l'IPS de l'ensemble du lycée s'appelle
    ips_ensemble_gt_pro jusqu'en 2022 et ips_etab à partir de 2023, et les IPS sont
    du texte (lus en str) qu'il faut convertir en nombres.
    Renvoie une ligne par lycée (uai) et par rentrée (2016 pour 2016-2017, etc.).
    """
    colonnes = ["rentree_scolaire", "uai", "secteur", "type_de_lycee",
                "ips_ensemble_gt_pro", "ips_voie_gt", "ips_voie_pro"]
    morceaux = [t.rename(columns={"ips_etab": "ips_ensemble_gt_pro"})[colonnes] for t in tables]
    ips = pd.concat(morceaux, ignore_index=True)

    ips["rentree"] = ips["rentree_scolaire"].str[:4].astype(int)  # "2016-2017" -> 2016
    for colonne in ["ips_ensemble_gt_pro", "ips_voie_gt", "ips_voie_pro"]:
        # errors="coerce" : une valeur qui n'est pas un nombre devient NaN au lieu d'une erreur
        ips[colonne] = pd.to_numeric(ips[colonne], errors="coerce")

    ips = ips.rename(columns={"ips_ensemble_gt_pro": "ips_lycee"})
    return ips.drop(columns="rentree_scolaire")


def preparer_poursuite(poursuite):
    """Calcule, pour chaque ligne du fichier de poursuite d'études, le nombre de poursuivants.

    Une ligne = une session du bac, une académie du bac, une voie et un genre.
    Les colonnes *_stable, *_flux_a et *_flux_ar comptent les néo-bacheliers qui
    poursuivent dans chaque type de formation : dans la même académie (stable), dans
    une autre académie de la même région académique (flux_a), ou dans une autre région
    académique (flux_ar). On fait les trois sommes, puis leur total.
    """
    df = poursuite.copy()
    stable = [c for c in df.columns if c.endswith("_stable")]
    flux_a = [c for c in df.columns if c.endswith("_flux_a")]
    flux_ar = [c for c in df.columns if c.endswith("_flux_ar")]

    # sum(axis=1) : somme sur les colonnes de la liste, ligne par ligne
    df["poursuivants_meme_academie"] = df[stable].sum(axis=1)
    df["poursuivants_autre_academie_meme_region"] = df[flux_a].sum(axis=1)
    df["poursuivants_autre_region"] = df[flux_ar].sum(axis=1)
    df["poursuivants"] = (df["poursuivants_meme_academie"]
                          + df["poursuivants_autre_academie_meme_region"]
                          + df["poursuivants_autre_region"])

    df = df.rename(columns={"rentree_session": "annee", "aca_lib": "academie",
                            "voie_du_baccalaureat": "voie"})
    return df[["annee", "academie", "voie", "genre", "bacheliers", "poursuivants",
               "poursuivants_meme_academie", "poursuivants_autre_academie_meme_region",
               "poursuivants_autre_region"]]


def base_selective(base):
    """ créer une nouvelle base ou on ne garde que les formations sélectives
    base : mettre le nom de la base créée et sauvegarder dans data"""
    return base[base["selective"]==1.0]
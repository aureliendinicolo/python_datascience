import pandas as pd
import os


# Identifiant de chaque session sur le portail open data du ministère
IDENTIFIANTS = {
    2018: "fr-esr-parcoursup-2018",
    2019: "fr-esr-parcoursup-2019",
    2020: "fr-esr-parcoursup_2020",
    2021: "fr-esr-parcoursup_2021",
    2022: "fr-esr-parcoursup_2022",
    2023: "fr-esr-parcoursup_2023",
    2024: "fr-esr-parcoursup_2024",
    2025: "fr-esr-parcoursup",
}

# Sans use_labels=true, l'export garde les noms courts des colonnes (cod_uai, acc_tot...),
# qui sont les identifiants stables décrits dans la documentation du jeu de données.
URL = "https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/{}/exports/csv?delimiter=%3B"
DATASETS = {annee: URL.format(identifiant) for annee, identifiant in IDENTIFIANTS.items()}

# Dossier du cache : data/raw/ à la racine du dépôt. On part de l'emplacement de ce fichier
# (sources/), pour que le chemin soit le bon quel que soit le dossier d'où on lance le code.
DOSSIER_RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

# dep (codes 2A/2B de la Corse, zéro initial de "01") et cod_uai (lettre finale) sont lus
# en texte, pour garder les zéros et avoir le même type toutes les années.
TYPES = {"dep": str, "cod_uai": str}


def charger_parcoursup(annee, force=False):
    """Charge le jeu de données Parcoursup d'une année.

    Le fichier est téléchargé une seule fois, puis gardé en cache dans data/raw/.
    Avec force=True, on le retélécharge même s'il est déjà enregistré
    (mise à jour des données, ou ancien fichier à remplacer).
    L'année est déjà dans la colonne session.
    """
    chemin = os.path.join(DOSSIER_RAW, f"parcoursup_{annee}.csv")

    if force or not os.path.exists(chemin):
        df = pd.read_csv(DATASETS[annee], sep=";", low_memory=False, dtype=TYPES)
        os.makedirs(DOSSIER_RAW, exist_ok=True)
        df.to_csv(chemin, index=False, sep=";")
    else:
        df = pd.read_csv(chemin, sep=";", low_memory=False, dtype=TYPES)

    return df

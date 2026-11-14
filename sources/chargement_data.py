import pandas as pd
import os


# Identifiant de chaque session Parcoursup sur le portail open data du ministère
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

# Taux de poursuite des néo-bacheliers dans le supérieur, par académie du bac (2010-2025)
URL_POURSUITE = URL.format("fr-esr-taux-poursuite-enseignement-superieur-par-academie")

# Indice de position sociale (IPS) des lycées, publié en 3 fichiers par l'Éducation nationale
URL_EDUCATION = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/{}/exports/csv?delimiter=%3B"
URL_IPS = {
    "2016-2021": URL_EDUCATION.format("fr-en-ips_lycees"),
    "2022": URL_EDUCATION.format("fr-en-ips-lycees-ap2022"),
    "2023-2025": URL_EDUCATION.format("fr-en-ips-lycees-ap2023"),
}

# Dossier du cache : data/raw/ à la racine du dépôt. On part de l'emplacement de ce fichier
# (sources/), pour que le chemin soit le bon quel que soit le dossier d'où on lance le code.
DOSSIER_RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

# dep (codes 2A/2B de la Corse, zéro initial de "01") et cod_uai (lettre finale) sont lus
# en texte, pour garder les zéros et avoir le même type toutes les années.
TYPES = {"dep": str, "cod_uai": str}


def telecharger(url, nom_fichier, force=False, types=None):
    """Télécharge un fichier CSV une seule fois, puis le relit depuis data/raw/.

    Avec force=True, on le retélécharge même s'il est déjà enregistré
    (mise à jour des données, ou ancien fichier à remplacer).
    types : dictionnaire {colonne: type} passé à read_csv (dtype).
    """
    chemin = os.path.join(DOSSIER_RAW, nom_fichier)

    if force or not os.path.exists(chemin):
        df = pd.read_csv(url, sep=";", low_memory=False, dtype=types)
        os.makedirs(DOSSIER_RAW, exist_ok=True)
        df.to_csv(chemin, index=False, sep=";")
    else:
        df = pd.read_csv(chemin, sep=";", low_memory=False, dtype=types)

    return df


def charger_parcoursup(annee, force=False):
    """Charge le jeu de données Parcoursup d'une année (l'année est dans la colonne session)."""
    return telecharger(DATASETS[annee], f"parcoursup_{annee}.csv", force, TYPES)


def charger_poursuite(force=False):
    """Charge le taux de poursuite des néo-bacheliers par académie, voie du bac et genre."""
    return telecharger(URL_POURSUITE, "poursuite_etudes.csv", force)


def charger_ips(force=False):
    """Charge les 3 fichiers IPS des lycées, sous forme de liste de tableaux bruts.

    Tout est lu en texte : les 3 fichiers n'ont pas les mêmes formats, ils sont
    harmonisés ensuite par harmoniser_ips (sources/cleaning_data.py).
    """
    return [
        telecharger(url, f"ips_lycees_{periode}.csv", force, str)
        for periode, url in URL_IPS.items()
    ]

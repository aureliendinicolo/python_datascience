import pandas as pd
import os


DATASETS = {
    2018: "https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-parcoursup-2018/exports/csv/?delimiter=%3B&lang=fr&timezone=Europe%2FParis&use_labels=true",
    2019: "https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-parcoursup-2019/exports/csv/?delimiter=%3B&lang=fr&timezone=Europe%2FParis&use_labels=true",
    2020: "https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-parcoursup_2020/exports/csv/?delimiter=%3B&lang=fr&timezone=Europe%2FParis&use_labels=true",
    2021: "https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-parcoursup_2021/exports/csv/?delimiter=%3B&lang=fr&timezone=Europe%2FParis&use_labels=true",
    2022: "https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-parcoursup_2022/exports/csv/?delimiter=%3B&lang=fr&timezone=Europe%2FParis&use_labels=true",
    2023: "https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-parcoursup_2023/exports/csv/?delimiter=%3B&lang=fr&timezone=Europe%2FParis&use_labels=true",
    2024: "https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-parcoursup_2024/exports/csv/?delimiter=%3B&lang=fr&timezone=Europe%2FParis&use_labels=true",
    2025: "https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-parcoursup_2025/exports/csv/?delimiter=%3B&lang=fr&timezone=Europe%2FParis&use_labels=true",

}

def charger_parcoursup(annee, force=False):
    """Charge le jeu de données Parcoursup d'une année.

    Le fichier est téléchargé une seule fois puis gardé en cache
    dans data/raw/. Utiliser force=False : pour ne pas retélécharger le fichier à chaque fois.
    """

    df = pd.read_csv(DATASETS[annee], sep=";")
    os.makedirs("../data/raw", exist_ok=True)
    df.to_csv(f"../data/raw/parcoursup_{annee}.csv", index=False, sep=";")
    df["annee"] = annee
    return df
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
    2025: "https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-parcoursup/exports/csv/?delimiter=%3B&lang=fr&timezone=Europe%2FParis&use_labels=true",

}
# code plus élaboré qui permet de faire deux cas : soit les données ne sont pas chargées, on les charge dans data/raw, soit elles existes et on les lit juste. Il suffit de commander avec force=true pour forcer le retéléchargement (mise à jour ou autre)

def charger_parcoursup(annee, force=False):
    """Charge le jeu de données Parcoursup d'une année
    Le fichier est téléchargé une seule fois puis gardé en cache
    dans data/raw/. force = False par défaut, utiliser force=True pour retélécharger les données au cas où elles soient déjà enregistrées (mise à jour des données ou autre).
    """
    chemin = f"../data/raw/parcoursup_{annee}.csv"

    if force or not os.path.exists(chemin):
        df = pd.read_csv(DATASETS[annee], sep=";", low_memory=False)
        os.makedirs("../data/raw", exist_ok=True)
        df.to_csv(chemin, index=False, sep=";")
    else:
        df = pd.read_csv(chemin, sep=";", low_memory=False)

    df["annee"] = annee
    return df
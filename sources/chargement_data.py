import pandas as pd



def charger_parcoursup(annee, force=False):
    """Charge le jeu de données Parcoursup d'une année.

    Le fichier est téléchargé une seule fois puis gardé en cache
    dans data/raw/. Utiliser force=False : pour ne pas retélécharger le fichier à chaque fois.
    """
    df_{annee} = pd.read_csv("https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-parcoursup-{année}/exports/csv/?delimiter=%3B&lang=fr&timezone=Europe%2FParis&use_labels=true", sep=";")
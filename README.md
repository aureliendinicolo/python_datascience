# Etude de la démocratisation de l’enseignement supérieur depuis l’ouverture de Parcoursup en 2018

Projet Python pour la data science, ENSAE (2A), 2026-2027.

## Question

**Observe-t-on une démocratisation de l'enseignement supérieur depuis l'ouverture de la plateforme Parcoursup ?**

On ne cherche pas à établir un effet causal de la plateforme. On décrit comment le profil des candidats et des admis a évolué entre 2018 et 2025 (boursiers, type de bac, mention, origine géographique, sexe), selon la filière et la sélectivité des formations, en signalant les limites des données.

## Données

- Parcoursup, vœux de poursuite d'études et de réorientation, sessions 2018 à 2025 : open data du ministère de l'Enseignement supérieur ([data.enseignementsup-recherche.gouv.fr](https://data.enseignementsup-recherche.gouv.fr/explore/?q=parcoursup)). Une ligne correspond à une formation pour une session.
- Indice de position sociale (IPS) des lycées, rentrées 2016 à 2025 : open data de l'Éducation nationale ([data.education.gouv.fr](https://data.education.gouv.fr/explore/?q=indice+de+position+sociale)), en trois fichiers. Joint aux formations par le code UAI et l'année (CPGE et BTS principalement).
- Taux de poursuite des néo-bacheliers dans l'enseignement supérieur par académie, 2010 à 2025 : open data du ministère de l'Enseignement supérieur ([fiche du jeu de données](https://data.enseignementsup-recherche.gouv.fr/explore/dataset/fr-esr-taux-poursuite-enseignement-superieur-par-academie/information/)). Joint aux admis de Parcoursup par académie et par année.

Les données sont téléchargées directement depuis les URL publiques. Elles ne sont pas stockées dans le dépôt.

## Installation

```
git clone https://github.com/aureliendinicolo/python_datascience.git
cd python_datascience
pip install -r requirements.txt
```

Ce projet est testé sur le SSP Cloud (Onyxia, Genes et Insee).

## Lancement

Ouvrir `notebooks/rapport.ipynb` et exécuter toutes les cellules. Les données sont téléchargées automatiquement dans `data/`.

## Organisation du dépôt

- `notebooks/rapport.ipynb` : notebook final, qui importe les fonctions de `sources/`.
- `notebooks/exploration.ipynb` : notebook d'exploration. Il garde la trace des vérifications qui justifient nos choix (identifiant, sélectivité, filières) et enregistre la base empilée dans `data/`.
- `sources/` : fonctions Python importées par les notebooks (`chargement_data.py` pour télécharger les données ; `cleaning_data.py`, `indicateurs.py` et `graphiques.py` à remplir).
- `data/` : données téléchargées ou générées, non versionnées (voir `.gitignore`).

## Avancement

Fait :

- chargement des 8 sessions avec mise en cache dans `data/raw/` (`sources/chargement_data.py`) ;
- identifiant de formation suivi d'une année à l'autre (`code`), validé en 2019-2020 et en 2025 ;
- sélectivité harmonisée (`selective`, 0/1), reportée de 2020 sur 2018-2019 puis complétée grâce à la filière (seules 634 licences de 2018-2019 restent sans statut) ;
- nomenclature commune des filières (`filiere`) ;
- base empilée : une ligne par formation et par session, environ 104 000 lignes.

- préparation de la base en fonctions (`sources/cleaning_data.py`), appelées par `notebooks/rapport.ipynb` ;
- enrichissements : IPS des lycées (`joindre_ips`), taux de poursuite par académie (`panel_academies`), indicateurs pour le zoom Île-de-France (`sources/indicateurs.py`).

À faire, dans cet ordre :

1. Analyse descriptive avec graphiques (`sources/graphiques.py`) : boursiers (rapport admis/candidats chaque année), type de bac, IPS des lycées pour les CPGE et les BTS, zoom Île-de-France.
2. Rédiger les limites : formations sans code en 2018-2019, sélectivité imputée, sauts de la part de boursiers en 2020 et 2025 (aussi chez les candidats, donc liés au comptage), académie de la formation et académie du bac différentes.

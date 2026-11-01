# python_datascience

Projet Python pour la data science, ENSAE (2A), 2026-2027.

## Question

**Huit ans après sa création, Parcoursup a-t-il permis une démocratisation de l'accès à l'enseignement supérieur ?**

On ne cherche pas à établir un effet causal de la plateforme. On décrit comment le profil des candidats et des admis a évolué entre 2018 et 2025 (boursiers, type de bac, mention, origine géographique, sexe), selon la filière et la sélectivité des formations, en signalant les limites des données.

## Données

- Parcoursup, vœux de poursuite d'études et de réorientation, sessions 2018 à 2025 : open data du ministère de l'Enseignement supérieur ([data.enseignementsup-recherche.gouv.fr](https://data.enseignementsup-recherche.gouv.fr/explore/?q=parcoursup)). Une ligne correspond à une formation pour une session.

Les données sont téléchargées directement depuis les URL publiques. Elles ne sont pas stockées dans le dépôt.

## Organisation du dépôt

- `exploration.ipynb` : notebook d'exploration. Il télécharge les 8 sessions, construit la base empilée et l'enregistre dans `data/`.
- `data/` : données générées par le notebook, non versionnées (voir `.gitignore`).

## Avancement

Fait :

- import des 8 sessions depuis l'API du ministère ;
- identifiant de formation suivi d'une année à l'autre (`code`), validé en 2019-2020 et en 2025 ;
- sélectivité harmonisée (`selective`, 0/1), reportée de 2020 sur 2018-2019 puis complétée grâce à la filière (seules 634 licences de 2018-2019 restent sans statut) ;
- nomenclature commune des filières (`filiere`) ;
- base empilée : une ligne par formation et par session, environ 104 000 lignes.

À faire, dans cet ordre :

1. Passer le code du notebook dans des fonctions (fichiers `.py`) importées par un notebook final.
2. Enrichir la base par des jointures avec d'autres sources (par exemple : bacheliers par académie, IPS des lycées, données INSEE), en commençant par l'Île-de-France.
3. Analyse descriptive avec graphiques : boursiers, type de bac, mobilité géographique, par filière et selon la sélectivité.
4. Rédiger les limites (formations sans code en 2018-2019, sélectivité imputée).

## Reproduire

À compléter : dépendances (`requirements.txt`) et ordre d'exécution.

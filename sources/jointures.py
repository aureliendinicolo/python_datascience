def joindre_ips(base, ips):
    """Ajoute à chaque formation l'IPS du lycée qui l'accueille (colonnes ips_*).

    Clé de jointure : le code UAI de l'établissement (cod_uai <-> uai) et l'année.
    La session Parcoursup N concerne les élèves de terminale de l'année scolaire
    (N-1)-N : on prend donc l'IPS de la rentrée N-1 (rentrée 2017 pour la session 2018).
    Seules les formations installées dans un lycée (surtout les CPGE et les BTS) trouvent
    un IPS ; pour les autres (universités, écoles), les colonnes ips_* restent vides.
    """
    base = base.copy()
    base["rentree_ips"] = base["session"] - 1

    colonnes_ips = ips[["uai", "rentree", "ips_lycee", "ips_voie_gt", "ips_voie_pro"]]
    base = base.merge(
        colonnes_ips,
        left_on=["cod_uai", "rentree_ips"],
        right_on=["uai", "rentree"],
        how="left",        # on garde toutes les formations, même sans IPS
        validate="m:1",    # vérifie qu'il y a au plus un IPS par lycée et par rentrée
    )
    return base.drop(columns=["uai", "rentree", "rentree_ips"])


def panel_academies(base, poursuite):
    """Construit un tableau avec une ligne par académie et par année (2018-2025).

    Côté Parcoursup : les admis des formations de l'académie (total, bacs pro et techno,
    boursiers néo-bacheliers), en sommant les formations.
    Côté poursuite d'études : les bacheliers de l'académie et ceux qui poursuivent dans le
    supérieur, par voie du bac (sommés sur les deux genres).
    Attention : Parcoursup donne l'académie de la formation, alors que le fichier de
    poursuite donne l'académie où le bac a été obtenu.
    """
    admis = (
        base.groupby(["academie", "session"])[["acc_tot", "acc_neobac", "acc_bp", "acc_bt", "acc_brs"]]
        .sum()
        .reset_index()
        .rename(columns={"session": "annee"})
    )

    # pivot_table : une colonne par voie du bac, au lieu d'une ligne par voie
    bacheliers = poursuite.pivot_table(index=["academie", "annee"], columns="voie",
                                       values=["bacheliers", "poursuivants"], aggfunc="sum")
    bacheliers.columns = [f"{mesure}_{voie}" for mesure, voie in bacheliers.columns]
    bacheliers = bacheliers.reset_index()

    # how="inner" : on garde les académies et années présentes des deux côtés
    # (ce qui exclut "Etranger" et les collectivités d'outre-mer, absentes du fichier de poursuite)
    return admis.merge(bacheliers, on=["academie", "annee"], how="inner", validate="1:1")

import os

import pandas as pd
import geopandas as gpd


BASE_PATH = os.path.dirname(os.path.realpath(__file__))


CENSUS_INCOME_FILES = {
    "rj": f"{BASE_PATH}/../../../data_raw/RJ/Base informaçoes setores2010 universo RJ/CSV/DomicilioRenda_RJ.csv",
    "df": f"{BASE_PATH}/../../../data_raw/DF/Base informaçoes setores2010 universo DF/CSV/DomicilioRenda_DF.csv",
    "pa": f"{BASE_PATH}/../../../data_raw/PA/Base informaçoes setores2010 universo PA/CSV/DomicilioRenda_PA.csv",
}

CENSUS_POLYGON_FILES = {
    "rj": f"{BASE_PATH}/../../../data_raw/33.gpkg",
    "df": f"{BASE_PATH}/../../../data_raw/53.gpkg",
    "pa": f"{BASE_PATH}/../../../data_raw/15.gpkg",
}

MUNICIPALITIES = {
    "rj": {
        "rio de janeiro",
        "niterói",
        "duque de caxias",
        "nova iguaçu",
        "itaboraí",
        "queimados",
        "são gonçalo",
        "belford roxo",
        "nilópolis",
        "são joão de meriti",
        "mesquita",
    },
    "df": {
        "brasília",
    },
    "pa": {
        "belém",
        "ananindeua",
        "benevides",
        "castanhal",
        "marituba",
        "santa bárbara do pará",
        "santa isabel do pará",
    },
}

INSTANCE_UF = {
    "rj": "rj",
    "df": "df",
    "pa": "pa",
}


def load_income_per_sector(uf):
    def int_or_zero(s):
        # There are a few occurrences of "X" in some numerical columns.
        try:
            return int(s)
        except ValueError:
            return 0

    census_income_df = pd.read_csv(
        CENSUS_INCOME_FILES[uf],
        sep=";",
        encoding="iso-8859-1",
        decimal=",",
    )

    # Sector code to string.
    census_income_df["code_tract"] = census_income_df.Cod_setor.apply(
        lambda s: str(s)
    )

    # Total income (V002) to int removing empty fields.
    census_income_df["total_income"] = census_income_df.V002.apply(int_or_zero)

    # Drop all other fields.
    return census_income_df[["code_tract", "total_income"]]


def load_geodata_per_sector(uf):

    # Read gpkg file using GeoPandas.
    census_geo_df = gpd.read_file(CENSUS_POLYGON_FILES[uf])

    return census_geo_df


def prepare_census_data(instance_name):
    if instance_name not in INSTANCE_UF:
        raise ValueError("Invalid instance identifier. Is it configured?")

    census_geo_df = load_geodata_per_sector(INSTANCE_UF[instance_name])
    census_income_df = load_income_per_sector(INSTANCE_UF[instance_name])

    tract_df = pd.merge(
        left=census_geo_df, right=census_income_df, on="code_tract"
    )

    municipalities = MUNICIPALITIES[instance_name]
    tract_df = tract_df[tract_df.name_muni.str.lower().isin(municipalities)]

    return tract_df

# coding: utf-8

import random
from io import BytesIO

import requests
import pandas as pd
import geopandas as gpd
from tqdm import tqdm
from shapely.geometry import Point


CENSUS_INCOME_FILES = {
    "RJ": "./data_raw/RJ/Base informaçoes setores2010 universo RJ/CSV/DomicilioRenda_RJ.csv",
}

CENSUS_POLYGON_FILES = {
    "RJ": "https://www.ipea.gov.br/geobr/data_gpkg/census_tract/2010/33.gpkg",
}

MUNICIPALITIES = {
    "RJ": {
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
    },
}

scaling_factor = 5e4


def load_income_per_sector():
    def int_or_zero(s):
        try:
            return int(s)
        except ValueError:
            return 0

    census_income_df = pd.read_csv(
        CENSUS_INCOME_FILES["RJ"],
        sep=";",
        encoding="iso-8859-1",
        decimal=",",
    )

    # Sector code to string.
    census_income_df["code_tract"] = census_income_df.Cod_setor.apply(lambda s: str(s))

    # Total income (V002) to int removing empty fields.
    census_income_df["total_income"] = census_income_df.V002.apply(int_or_zero)

    # Drop all other fields.
    return census_income_df[["code_tract", "total_income"]]


def load_geodata_per_sector():
    req = requests.get(CENSUS_POLYGON_FILES["RJ"])
    gpkg_content = req.content

    # Read gpkg file using GeoPandas.
    census_geo_df = gpd.read_file(BytesIO(gpkg_content))

    return census_geo_df


def prepare_data():
    census_geo_df = load_geodata_per_sector()
    census_income_df = load_income_per_sector()

    tract_df = pd.merge(left=census_geo_df, right=census_income_df, on="code_tract")

    municipalities = MUNICIPALITIES["RJ"]
    tract_df = tract_df[tract_df.name_muni.str.lower().isin(municipalities)]

    return tract_df


def generate_points(tract_df):
    def generate_random(number, polygon):
        points = []
        minx, miny, maxx, maxy = polygon.bounds
        while len(points) < number:
            pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
            if polygon.contains(pnt):
                points.append(pnt)
        return points

    region_samples = tract_df.progress_apply(
        lambda r: generate_random(r.total_income / scaling_factor, r.geometry), axis=1
    )
    points = pd.Series([p for r in region_samples for p in r])
    return points


def generate_cvrp():
    pass


def generate_cvrpsc():
    pass


def generate_lap():
    pass


if __name__ == "__main__":
    random.seed(42)
    # Create and register a new `tqdm` instance with `pandas`
    # (can use tqdm_gui, optional kwargs, etc.)
    tqdm.pandas()
    print(generate_points(prepare_data()))

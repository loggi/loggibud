# coding: utf-8

import random
import itertools
from io import BytesIO
from collections import Counter

import folium
import requests
import numpy as np
import pandas as pd
import geopandas as gpd
from tqdm import tqdm
from shapely.geometry import Point
from sklearn.cluster import KMeans

from p_hub import PHubProblem, solve_p_hub
from distances import calculate_distance_matrix_m


CENSUS_INCOME_FILES = {
    "RJ": "./data_raw/RJ/Base informaçoes setores2010 universo RJ/CSV/DomicilioRenda_RJ.csv",
}

CENSUS_POLYGON_FILES = {
    "RJ": "./data_raw/33.gpkg",
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

scaling_factor = 1e5


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

    # Read gpkg file using GeoPandas.
    census_geo_df = gpd.read_file(CENSUS_POLYGON_FILES["RJ"])

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


def generate_subinstances():
    pass


def generate_cvrpsc():
    pass


if __name__ == "__main__":
    seed = 42
    random.seed(seed)

    # Create and register a new `tqdm` instance with `pandas`
    # (can use tqdm_gui, optional kwargs, etc.)
    tqdm.pandas()

    # Generate instances.
    input_data = prepare_data()
    points = generate_points(input_data)
    sizes = np.random.randint(-5_301, 5_301, size=90) + 27_541

    lap_instances = [np.random.choice(points, size=size) for size in sizes]

    train_instances, test_instances = lap_instances[:60], lap_instances[60:]

    # Generate subinstances.
    clustering_points = [p for p in train_instances]
    n_clusters = 200
    num_hubs = 9

    clustering = KMeans(n_clusters, random_state=seed)
    clusters = clustering.fit_predict([[p.x, p.y] for p in points])
    cluster_weights = Counter(clusters)
    demands = np.array([cluster_weights[i] for i in range(n_clusters)])

    distances_matrix = calculate_distance_matrix_m(
        [Point(x, y) for x, y in clustering.cluster_centers_]
    )

    locations, allocations = solve_p_hub(
        PHubProblem(
            p=num_hubs,
            demands=demands,
            transport_costs=distances_matrix,
        )
    )

    remappings = {
        j: i for i, row in enumerate(allocations) for j, a in enumerate(row) if a
    }

    print(remappings)

    def subinstance_allocation(instance):
        return np.array(
            [remappings[i] for i in clustering.predict([[p.x, p.y] for p in instance])]
        )

    instance = train_instances[0]

    # Deterministic hub assignment.
    subinstance_index = subinstance_allocation(instance)

    print(Counter(subinstance_index))

    # Random hub assignment.
    num_random_points = int(len(instance) * 0.1)
    subinstance_index[:num_random_points] = np.random.choice(
        subinstance_index, size=num_random_points
    )

    subinstances = [
        [p for _, p in group]
        for key, group in itertools.groupby(
            sorted(zip(subinstance_index, instance), key=lambda v: v[0]),
            key=lambda v: v[0],
        )
    ]

    # Plot instance.

    for idx, subinstance in enumerate(subinstances):
        print(len(subinstance))
        latlng = np.array([[p.y, p.x] for p in subinstance])

        center = np.average(latlng, axis=0)

        m = folium.Map(
            location=center,
            zoom_start=11,
            tiles="cartodbpositron",
        )

        for (lat, lng) in latlng:
            folium.CircleMarker([lat, lng], color="blue", radius=1, weight=1).add_to(m)

        m.save(f"instance-{0}-{idx}.html")

    latlng = np.array([[p.y, p.x] for p in instance])
    center = np.average(latlng, axis=0)

    m = folium.Map(
        location=center,
        zoom_start=11,
        tiles="cartodbpositron",
    )

    for (lat, lng) in latlng:
        folium.CircleMarker([lat, lng], color="blue", radius=1, weight=1).add_to(m)

    m.save(f"instance-{0}.html")

    # Plot hub assignment.

    center = np.average(clustering.cluster_centers_, axis=0)

    m = folium.Map(
        location=center[::-1],
        zoom_start=11,
        tiles="cartodbpositron",
    )

    demand_average = np.average(demands)

    for (lng, lat), demand, assign in zip(
        clustering.cluster_centers_, demands, locations
    ):
        color = "red" if assign else "blue"

        folium.CircleMarker(
            [lat, lng], color=color, radius=demand / demand_average, weight=1
        ).add_to(m)

    for i, (x_lng, x_lat) in enumerate(clustering.cluster_centers_):
        for j, (y_lng, y_lat) in enumerate(clustering.cluster_centers_):
            if allocations[i, j]:
                folium.PolyLine([[x_lat, x_lng], [y_lat, y_lng]], weight=1).add_to(m)

    m.save("demo.html")

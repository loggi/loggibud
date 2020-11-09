# coding: utf-8

import os
import random
import itertools
import json
from pathlib import Path
from io import BytesIO
from collections import Counter
from dataclasses import dataclass, asdict
from typing import List, Optional

import folium
import numpy as np
import pandas as pd

from tqdm import tqdm
from shapely.geometry import Point as ShapelyPoint
from sklearn.cluster import KMeans

from ..cvrp.types import CVRPInstance
from ..shared.distances import calculate_distance_matrix_m
from ..shared.types import Point, Delivery, DeliveryProblemInstance
from ..shared.p_hub import PHubProblem, solve_p_hub
from .preprocessing import prepare_census_data


# Create and register a new `tqdm` instance with `pandas`
# (can use tqdm_gui, optional kwargs, etc.)
tqdm.pandas()


@dataclass
class DeliveryGenerationConfig:
    name: str
    num_train_instances: int
    num_dev_instances: int
    revenue_income_ratio: float
    size_average: int
    size_range: int
    seed: int = 0
    save_to: Optional[str] = None

    def get_default(cls):
        return cls(
            name="rj",
            num_train_instances=90,
            num_dev_instances=30,
            revenue_income_ratio=1e-5,
            size_average=27_541,
            size_range=5_301,
        )


@dataclass
class CVRPGenerationConfig:
    name: str
    num_hubs: int
    num_clusters: int
    random_demand_ratio: float
    vehicle_capacity: int
    seed: int = 0
    save_to: Optional[str] = None

    def get_default(cls):
        return cls(
            name="rj",
            num_hubs=9,
            random_demand_ratio=0.01,
            vehicle_capacity=120,
        )


@dataclass
class CensusGenerationResult:
    name: str
    deliveries: List[Delivery]
    train_instances: List[DeliveryProblemInstance]
    dev_instances: List[DeliveryProblemInstance]


@dataclass
class CVRPGenerationResult:
    name: str
    train_instances: List[CVRPInstance]
    dev_instances: List[CVRPInstance]


def generate_deliveries(
    tract_df: pd.DataFrame, revenue_income_ratio: float
) -> List[Delivery]:
    def new_point(polygon):
        # Loop until the point matches the poligon.
        while True:
            # Generate using a uniform distribution inside the bounding box.
            minx, miny, maxx, maxy = polygon.bounds
            p = ShapelyPoint(random.uniform(minx, maxx), random.uniform(miny, maxy))

            # If is contained, return.
            if polygon.contains(p):
                return Delivery(
                    point=Point.from_shapely(p),
                    size=random.randint(1, 10),
                )

    region_samples = tract_df.progress_apply(
        lambda r: [
            new_point(r.geometry)
            for i in range(int(r.total_income * revenue_income_ratio))
        ],
        axis=1,
    )
    return [p for r in region_samples for p in r]


def generate_census_instances(
    config: DeliveryGenerationConfig,
) -> CensusGenerationResult:
    np.random.seed(config.seed)

    num_instances = config.num_train_instances + config.num_dev_instances

    sizes = (
        np.random.randint(-config.size_range, config.size_range, size=num_instances)
        + config.size_average
    )

    # Compute deliveries from demand distribution.
    tract_df = prepare_census_data(config.name)
    deliveries = generate_deliveries(tract_df, config.revenue_income_ratio)

    # Sample deliveries into instances.
    instances = [
        DeliveryProblemInstance(
            name=f"{config.name}-{i}",
            deliveries=np.random.choice(deliveries, size=size).tolist(),
        )
        for i, size in enumerate(sizes)
    ]

    # Split train and dev instances.
    train_instances = instances[: config.num_train_instances]
    dev_instances = instances[config.num_train_instances :]

    if config.save_to is not None:
        for prefix, instances_subset in (
            ("train", train_instances),
            ("dev", dev_instances),
        ):
            path = Path(f"{config.save_to}/{prefix}/").mkdir(
                parents=True, exist_ok=True
            )

            for instance in instances_subset:
                path = Path(f"{config.save_to}/{prefix}/{instance.name}.json")
                with path.open("w") as file:
                    json.dump(asdict(instance), file)

    return CensusGenerationResult(
        name=config.name,
        deliveries=deliveries,
        train_instances=train_instances,
        dev_instances=dev_instances,
    )


def generate_cvrp_subinstances(
    config: CVRPGenerationConfig, generation: CensusGenerationResult
):
    np.random.seed(config.seed)

    # Merge all train instance deliveries.
    clustering_points = np.array(
        [
            [d.point.lng, d.point.lat]
            for instance in generation.train_instances
            for d in instance.deliveries
        ]
    )

    # Run k means clustering over the points.
    clustering = KMeans(config.num_clusters, random_state=config.seed)
    clusters = clustering.fit_predict(clustering_points)

    # Compute the number of deliveries in every cluster.
    cluster_weights = Counter(clusters)
    demands = np.array([cluster_weights[i] for i in range(config.num_clusters)])

    # Compute the street distance between points.
    distances_matrix = calculate_distance_matrix_m(
        [Point(x, y) for x, y in clustering.cluster_centers_]
    )

    # Solve the p-hub location problems between hubs.
    locations, allocations = solve_p_hub(
        PHubProblem(
            p=config.num_hubs,
            demands=demands,
            transport_costs=distances_matrix,
        )
    )

    # Map every cluster into a hub.
    hub_allocations = {
        i: [j for j, a in enumerate(row) if a] for i, row in enumerate(allocations)
    }

    print(hub_allocations)

    def aggregate_subinstances(instance):

        # Deterministic hub assignment.
        cluster_index = clustering.predict(
            [[d.point.lng, d.point.lat] for d in instance.deliveries]
        )

        # Random hub assignment.
        num_random_points = int(len(instance.deliveries) * config.random_demand_ratio)
        cluster_index[:num_random_points] = np.random.choice(
            cluster_index, size=num_random_points
        )

        # Group deliveries per cluster.
        cluster_deliveries = {
            key: [d for _, d in group]
            for key, group in itertools.groupby(
                sorted(zip(cluster_index, instance.deliveries), key=lambda v: v[0]),
                key=lambda v: v[0],
            )
        }

        # Aggregate clusters into subinstances according to the hub assignment.
        subinstance_deliveries = [
            [d for cluster in clusters for d in cluster_deliveries.get(cluster, [])]
            for hub_cluster, clusters in hub_allocations.items()
            if clusters
        ]

        # Select the hub as one demand from the selected cluster.
        subinstance_hubs = [
            Point(*clustering.cluster_centers_[hub_cluster])
            for hub_cluster, clusters in hub_allocations.items()
            if clusters
        ]

        return [
            CVRPInstance(
                name=f"{instance.name}-cvrp-{idx}",
                origin=hub,
                deliveries=deliveries,
                vehicle_capacity=config.vehicle_capacity,
            )
            for idx, (deliveries, hub) in enumerate(
                zip(subinstance_deliveries, subinstance_hubs)
            )
        ]

    train_subinstances = [
        subinstance
        for instance in generation.train_instances
        for subinstance in aggregate_subinstances(instance)
    ]
    dev_subinstances = [
        subinstance
        for instance in generation.dev_instances
        for subinstance in aggregate_subinstances(instance)
    ]

    if config.save_to is not None:
        for prefix, instances_subset in (
            ("train", train_subinstances),
            ("dev", dev_subinstances),
        ):
            path = Path(f"{config.save_to}/{prefix}/").mkdir(
                parents=True, exist_ok=True
            )

            for instance in instances_subset:
                path = Path(f"{config.save_to}/{prefix}/{instance.name}.json")
                with path.open("w") as file:
                    json.dump(asdict(instance), file)

    return CVRPGenerationResult(
        name=config.name,
        train_instances=train_subinstances,
        dev_instances=dev_subinstances,
    )

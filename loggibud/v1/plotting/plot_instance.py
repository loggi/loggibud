import logging
from argparse import ArgumentParser

import numpy as np
import folium

from ..types import CVRPInstance, DeliveryProblemInstance


logger = logging.getLogger(__name__)


def plot_cvrp_instance(instance: CVRPInstance):

    origin = instance.origin
    points = [delivery.point for delivery in instance.deliveries]

    # create a map
    m = folium.Map(
        location=(origin.lat, origin.lng),
        zoom_start=12,
        tiles="cartodbpositron",
    )

    for point in points:
        folium.CircleMarker(
            [point.lat, point.lng], color="blue", radius=1, weight=1
        ).add_to(m)

    folium.CircleMarker(
        [origin.lat, origin.lng], color="red", radius=3, weight=5
    ).add_to(m)

    return m


def plot_delivery_instance(instance: DeliveryProblemInstance):

    points = [delivery.point for delivery in instance.deliveries]
    center_lat = np.mean([p.lat for p in points])
    center_lng = np.mean([p.lng for p in points])

    # create a map
    m = folium.Map(
        location=(center_lat, center_lng),
        zoom_start=12,
        tiles="cartodbpositron",
    )

    for point in points:
        folium.CircleMarker(
            [point.lat, point.lng], color="blue", radius=1, weight=1
        ).add_to(m)

    return m


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("--cvrp", type=str)
    parser.add_argument("--delivery", type=str)

    args = parser.parse_args()

    # Load instance and heuristic params.

    if args.cvrp:
        instance = CVRPInstance.from_file(args.cvrp)
        m = plot_cvrp_instance(instance)

    elif args.delivery:
        instance = DeliveryProblemInstance.from_file(args.delivery)
        m = plot_delivery_instance(instance)

    m.save("map.html")

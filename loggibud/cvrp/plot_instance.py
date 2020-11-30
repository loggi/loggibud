import logging
from argparse import ArgumentParser

import folium

from .types import CVRPInstance, CVRPSolution


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

    m.save("map.html")


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("--instance", type=str, required=True)

    args = parser.parse_args()

    # Load instance and heuristic params.
    instance = CVRPInstance.from_file(args.instance)

    plot_cvrp_instance(instance)

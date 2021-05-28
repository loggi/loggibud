"""Plots solution routes"""
from typing import List, Optional

import folium
import numpy as np

from loggibud.v1.types import CVRPSolution


# All available map colors
MAP_COLORS = (
    "black",
    "blue",
    "darkred",
    "purple",
    "red",
    "orange",
    "green",
    "pink",
    "darkblue",
    "beige",
    "gray",
    "lightgreen",
    "lightblue",
    "lightgray",
    "cadetblue"
)


def plot_solution(
    solution: CVRPSolution, route_indices_to_plot: Optional[List[int]] = None
) -> None:
    """Plot solutions routes in a map

    Parameters
    ----------
    solution
        A solution to any solver with the vehicles routes to plot

    route_indices_to_plot
        If specified, selects a smaller subset of routes to plot by their
        indices. This can be useful to reduce the clutter in case of a
        solution with too many vehicles
    """
    # Initialize map centered at the mean of the origins
    origins_mean = np.mean(
        [
            (vehicle.origin.lat, vehicle.origin.lng)
            for vehicle in solution.vehicles
        ],
        axis=0
    )
    m = folium.Map(
        location=origins_mean, zoom_start=12, tiles="cartodbpositron",
    )

    num_vehicles = len(solution.vehicles)
    route_indices_to_plot = route_indices_to_plot or range(num_vehicles)
    vehicles_subset = [solution.vehicles[i] for i in route_indices_to_plot]

    for i, vehicle in enumerate(vehicles_subset):
        origin = (vehicle.origin.lat, vehicle.origin.lng)
        folium.CircleMarker(origin, color="red", radius=3, weight=5).add_to(m)

        vehicle_color = MAP_COLORS[i % len(MAP_COLORS)]
        vehicle_coords = [(point.lat, point.lng) for point in vehicle.circuit]
        folium.Polygon(
            vehicle_coords,
            popup=f"Vehicle {i + 1}",
            color=vehicle_color,
            weight=1,
        ).add_to(m)

    return m

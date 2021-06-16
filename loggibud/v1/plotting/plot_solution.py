"""Plots solution routes"""
from typing import List, Iterable, Optional

import folium
import numpy as np
import polyline
import requests

from loggibud.v1.types import CVRPSolution, Point
from loggibud.v1.distances import OSRMConfig


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
    "cadetblue",
)


def plot_cvrp_solution_routes(
    solution: CVRPSolution,
    route_indices_to_plot: Optional[List[int]] = None,
    config: Optional[OSRMConfig] = None,
) -> None:
    """Plot solution routes in a map along the streets

    Parameters
    ----------
    solution
        A solution to any solver with the vehicles routes to plot

    route_indices_to_plot
        If specified, selects a smaller subset of routes to plot by their
        indices. This can be useful to reduce the clutter in case of a
        solution with too many vehicles

    config
        OSRM configuration
    """
    config = config or OSRMConfig()

    # Initialize map centered at the mean of the origins
    origins_mean = np.mean(
        [
            (vehicle.origin.lat, vehicle.origin.lng)
            for vehicle in solution.vehicles
        ],
        axis=0,
    )
    m = folium.Map(
        location=origins_mean,
        zoom_start=12,
        tiles="cartodbpositron",
    )

    num_vehicles = len(solution.vehicles)
    route_indices_to_plot = route_indices_to_plot or range(num_vehicles)
    vehicles_subset = [solution.vehicles[i] for i in route_indices_to_plot]

    for i, vehicle in enumerate(vehicles_subset):
        vehicle_color = MAP_COLORS[i % len(MAP_COLORS)]

        # Plot origin
        origin = (vehicle.origin.lat, vehicle.origin.lng)
        folium.CircleMarker(origin, color="red", radius=3, weight=5).add_to(m)

        # Plot street outlines
        wiring = _route_wiring(vehicle.circuit, config)
        folium.PolyLine(
            wiring, color=vehicle_color, weight=1.0, popup=f"Vehicle {i}"
        ).add_to(m)

        # Plot the deliveries as regular points
        for delivery in vehicle.deliveries:
            folium.Circle(
                location=(delivery.point.lat, delivery.point.lng),
                radius=10,
                fill=True,
                color=vehicle_color,
                popup=(
                    f"Vehicle {i} ({delivery.point.lat}, {delivery.point.lng})"
                ),
            ).add_to(m)

    return m


def _route_wiring(points: Iterable[Point], config):
    coords_uri = ";".join(f"{point.lng},{point.lat}" for point in points)

    response = requests.get(
        f"{config.host}/route/v1/driving/{coords_uri}?overview=simplified",
        timeout=config.timeout_s,
    )

    data = response.json()
    line = data["routes"][0]["geometry"]

    return [(lat, lng) for lat, lng in polyline.decode(line)]


def plot_cvrp_solution(
    solution: CVRPSolution, route_indices_to_plot: Optional[List[int]] = None
) -> None:
    """Plot solution deliveries in a map
    This is a simplified version showing only the edges between each delivery.
    It does not require an OSRM server configuration.

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
        axis=0,
    )
    m = folium.Map(
        location=origins_mean,
        zoom_start=12,
        tiles="cartodbpositron",
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
            popup=f"Vehicle {i}",
            color=vehicle_color,
            weight=1,
        ).add_to(m)

    return m

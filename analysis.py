import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

HEIGHT = 2.7  # Height of each cargo unit
LENGTH = 13.625  # Length of the trailer
WIDTH = 2.48   # Width of the trailer

def visualize_cargo_load(load_grid):
    """
    Visualizes the cargo load in a 3x2 grid inside a trailer using a 3D bar plot.

    Args:
        load_grid (np.ndarray): 3x2 array with cargo heights.
    """
    assert load_grid.shape == (3, 2), "Input grid must be 3x2 (WIDTH x LENGTH)"

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    width_zones = 2
    length_zones = 3
    zone_width = WIDTH / width_zones
    zone_length = LENGTH / length_zones

    # x = Länge (3 Zonen), y = Breite (2 Zonen)
    x = np.repeat(np.arange(length_zones) * zone_length, width_zones)
    y = np.tile(np.arange(width_zones) * zone_width, length_zones)
    z = np.zeros_like(x)
    dx = np.full_like(x, zone_length * 0.98)
    dy = np.full_like(y, zone_width * 0.95)
    dz = load_grid.flatten()

    # Add color mapping based on height
    colors = plt.cm.RdYlGn((dz) / (HEIGHT))
    ax.bar3d(x, y, z, dx, dy, dz, color=colors)

    # Draw cargo hold (trailer) as a wireframe box
    corners = np.array([
        [0, 0, 0], [LENGTH, 0, 0], [LENGTH, WIDTH, 0], [0, WIDTH, 0],
        [0, 0, HEIGHT], [LENGTH, 0, HEIGHT], [LENGTH, WIDTH, HEIGHT], [0, WIDTH, HEIGHT]
    ])
    edges = [
        (0,1), (1,2), (2,3), (3,0), # bottom
        (4,5), (5,6), (6,7), (7,4), # top
        (0,4), (1,5), (2,6), (3,7)  # sides
    ]
    for edge in edges:
        ax.plot(*zip(*corners[list(edge)]), color='black', linewidth=1.2)

    ax.text(0, WIDTH/2, HEIGHT*1.05, "FRONT", color="blue", fontsize=12, ha="center", va="bottom", weight="bold")
    ax.text(LENGTH, WIDTH/2, HEIGHT*1.05, "REAR", color="blue", fontsize=12, ha="center", va="bottom", weight="bold")

    ax.set_box_aspect([LENGTH, WIDTH, HEIGHT])
    ax.set_axis_off()
    ax.set_title('Trailer Cargo Load Visualization')
    plt.show()

def calculate_cargo_load(load_grid):
    """
    Calculates the total cargo load from the grid.

    Args:
        load_grid (np.ndarray): 3x2 array with cargo heights.

    Returns:
        float: Total cargo load.
    """

    assert load_grid.shape == (3, 2), "Input grid must be 3x2 (WIDTH x LENGTH)"

    load_grid = load_grid / HEIGHT

    total_load = (np.sum(load_grid) / 6) * 100
    print(f"Total cargo load: {total_load:.2f} %")

    # Check number of non-empty zones
    print(f"Loaded zones: {np.count_nonzero(load_grid)}/6")


    return total_load


if __name__ == "__main__":
    cargo_grid = np.array([[0.5, 1],
                           [1.5, 2],
                           [0, 0]])
    
    # visualize_cargo_load(cargo_grid)
    calculate_cargo_load(cargo_grid)
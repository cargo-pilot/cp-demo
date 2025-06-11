import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import messagebox

# Constants for trailer dimensions
# UPDATE TO FIT 1/8 MODEL!
HEIGHT = 2.7
LENGTH = 13.625
WIDTH = 2.48

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
    dx = np.full_like(x, zone_length)
    dy = np.full_like(y, zone_width)
    dz = load_grid.flatten()

    # Add color mapping based on height
    colors = plt.cm.RdYlGn((dz) / (HEIGHT))
    ax.bar3d(x, y, z, dx, dy, dz, color=colors,linewidth=0.5, edgecolor='black', alpha=0.8)
    
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

    # Set default subplot parameters
    plt.subplots_adjust(left=0, right=1, top=0.9, bottom=0)


    plt.show()

def calculate_cargo_load(load_grid):
    """
    Calculates the total cargo load from the grid.

    Args:
        load_grid (np.ndarray): 3x2 array with cargo heights.

    Returns:
        total_load (float): Total cargo load in percent.
    """

    assert load_grid.shape == (3, 2), "Input grid must be 3x2 (WIDTH x LENGTH)"

    load_grid = load_grid / HEIGHT

    total_load = (np.sum(load_grid) / 6) * 100
    print(f"Total cargo load: {total_load:.2f} %")

    # Check number of non-empty zones
    print(f"Loaded zones: {np.count_nonzero(load_grid)}/6")


    return total_load

def launch_gui():
    root = tk.Tk()
    root.title("Cargo Load Input")

    entries = []
    # Add 'FRONT' label above first row
    front_label = tk.Label(root, text="FRONT", fg="blue", font=("Arial", 10, "bold"))
    front_label.grid(row=0, column=0, columnspan=2, pady=(5,0))

    # Entry fields (start at row=1)
    for i in range(3):
        row_entries = []
        for j in range(2):
            e = tk.Entry(root, width=5, justify='center')
            e.grid(row=i+1, column=j, padx=5, pady=5)
            e.insert(0, "0")
            row_entries.append(e)
        entries.append(row_entries)

    # Add 'REAR' label below last row
    rear_label = tk.Label(root, text="REAR", fg="blue", font=("Arial", 10, "bold"))
    rear_label.grid(row=4, column=0, columnspan=2, pady=(0,5))

    # Output fields for calculated values
    result_var = tk.StringVar()
    zones_var = tk.StringVar()
    result_label = tk.Label(root, textvariable=result_var, font=("Arial", 10))
    result_label.grid(row=6, column=0, columnspan=2, pady=(5,0))
    result_var.set(f"Total cargo load: 0.00 %")
    zones_label = tk.Label(root, textvariable=zones_var, font=("Arial", 10))
    zones_label.grid(row=7, column=0, columnspan=2, pady=(0,5))
    zones_var.set(f"Loaded zones: 0/6")

    def get_grid():
        grid = np.zeros((3,2))
        for i in range(3):
            for j in range(2):
                val = float(entries[i][j].get())
                if val < 0 or val > HEIGHT:
                    raise ValueError(f"Value at ({i+1},{j+1}) must be between 0 and {HEIGHT}")
                grid[i, j] = val
        return grid

    def on_calculate():
        try:
            grid = get_grid()
            # Calculate and update output fields
            grid_norm = grid / HEIGHT
            total_load = (np.sum(grid_norm) / 6) * 100
            loaded_zones = np.count_nonzero(grid_norm)
            result_var.set(f"Total cargo load: {total_load:.2f} %")
            zones_var.set(f"Loaded zones: {loaded_zones}/6")
        except Exception as ex:
            messagebox.showerror("Input Error", str(ex))

    def on_visualize():
        try:
            grid = get_grid()
            visualize_cargo_load(grid)
        except Exception as ex:
            messagebox.showerror("Input Error", str(ex))

    btn_calc = tk.Button(root, text="Calculate", command=on_calculate)
    btn_calc.grid(row=5, column=0, pady=10)
    btn_vis = tk.Button(root, text="Visualize", command=on_visualize)
    btn_vis.grid(row=5, column=1, pady=10)

    root.mainloop()

if __name__ == "__main__":
    launch_gui()
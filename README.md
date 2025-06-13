# Analysis Tool for 3x2 Sensor Grid in Cargo Hold

This tool provides a graphical interface and visualization for analyzing cargo load distribution in a trailer using a 3x2 sensor grid. It calculates the total cargo load and visualizes the load distribution in 3D.

## Setup

1. **Install Python**  
   Ensure you have Python 3.x installed. Download it from [python.org](https://www.python.org/downloads/).

2. **(Optional) Create a virtual environment**  
   It is recommended to use a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```

3. **Install required packages**  
   Run the following command in your terminal:
   ```powershell
   pip install numpy matplotlib
   ```
   > Note: `tkinter` is included with most standard Python installations. If you encounter an error about `tkinter`, you may need to install it separately or ensure you are using a standard Python distribution (not minimal/embedded).

4. **Run the script**  
   ```powershell
   python analysis.py
   ```

## Configuration

By default, the script uses the standard dimensions of a trailer for calculations and visualizations.

If you are using a trailer with different dimensions (e.g., a 1:8 model), update the constants at the top of `analysis.py`:

```python
HEIGHT = 2.7
LENGTH = 13.625
WIDTH = 2.48
```

## Usage

1. Input the measured data into the 3x2 grid.
2. Press the **Calculate** button to display the cargo load in percent.
3. Press the **Visualize** button to display the 3D load graphic.


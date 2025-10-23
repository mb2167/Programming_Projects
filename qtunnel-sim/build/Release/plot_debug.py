import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # registers 3D projection

def plot_field_3d_surface(filename, title, extent=(-20, 20, -20, 20), cmap='inferno'):
    data = np.loadtxt(filename, delimiter=",")
    ny, nx = data.shape
    x_min, x_max, y_min, y_max = extent
    x = np.linspace(x_min, x_max, nx)
    y = np.linspace(y_min, y_max, ny)
    X, Y = np.meshgrid(x, y)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, data,
                           cmap=cmap,
                           linewidth=0,
                           antialiased=True,
                           rcount=200,
                           ccount=200)
    fig.colorbar(surf, ax=ax, shrink=0.6, label='Amplitude')
    ax.set_title(title)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('Value')
    plt.tight_layout()
    plt.show()

# Examples
plot_field_3d_surface('potential.csv', 'Potential V(x,y)')
plot_field_3d_surface('wave_init.csv', 'Initial |ψ(x,y)|²')
plot_field_3d_surface('wave_final.csv', 'Final |ψ(x,y)|²')

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import os

# Parameters
Nx, Ny = 128, 128
extent = (-20, 20, -20, 20)
folder = '.'  # folder with wave CSVs and potential.csv
cmap_wave = 'inferno'
cmap_pot = 'coolwarm'

# Load potential once (fixed)
potential_data = np.loadtxt(os.path.join(folder, 'potential.csv'), delimiter=",")

# Automatically find all wave CSV files
wave_files = sorted([f for f in os.listdir(folder) if f.startswith("wave_") and f.endswith(".csv")],
                    key=lambda x: int(x.split('_')[1].split('.')[0]))
num_frames = len(wave_files)

# Create grid
x = np.linspace(extent[0], extent[1], Nx)
y = np.linspace(extent[2], extent[3], Ny)
X, Y = np.meshgrid(x, y)

# Prepare figure
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot potential as semi-transparent surface (fixed)
ax.plot_surface(X, Y, potential_data, cmap=cmap_pot, alpha=0.6, linewidth=0, antialiased=True)

# Initial wave surface (first timestep)
wave_data = np.loadtxt(os.path.join(folder, wave_files[0]), delimiter=",")
surf_wave = ax.plot_surface(X, Y, wave_data, cmap=cmap_wave, linewidth=0, antialiased=True)

# Set labels and limits
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('Value')
ax.set_zlim(0, max(np.max(wave_data), np.max(potential_data))*1.2)

# Colorbars
mappable_wave = plt.cm.ScalarMappable(cmap=cmap_wave)
mappable_wave.set_array(wave_data)
fig.colorbar(mappable_wave, ax=ax, shrink=0.5, label='|ψ(x,y)|²')

mappable_pot = plt.cm.ScalarMappable(cmap=cmap_pot)
mappable_pot.set_array(potential_data)
fig.colorbar(mappable_pot, ax=ax, shrink=0.5, label='Potential V(x,y)')

# Update function for animation
def update(frame):
    global surf_wave
    ax.collections.remove(surf_wave)  # remove old wave surface
    wave_data = np.loadtxt(os.path.join(folder, wave_files[frame]), delimiter=",")
    surf_wave = ax.plot_surface(X, Y, wave_data, cmap=cmap_wave, linewidth=0, antialiased=True)
    ax.set_title(f'Wavefunction and Potential: timestep {frame}')
    return surf_wave,

# Create animation
ani = FuncAnimation(fig, update, frames=num_frames, interval=100, blit=False)

# Show animation
plt.show()

# Optional: save as mp4
# ani.save('wave_evolution.mp4', writer='ffmpeg', fps=10)

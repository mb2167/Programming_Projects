#pragma once
#include <vector>

class MACGrid {
public:
    // Grid cell size (uniform spacing)
    static constexpr double cellSize = 0.01;

    // Number of cells in each direction
    int Nx, Ny;

    // -------------------------------
    // Data storage
    // -------------------------------
    // Pressure at cell centers (Nx * Ny)
    std::vector<double> pressure;

    // Velocity components stored on staggered faces:
    // u = x-velocity, stored on vertical faces (Nx+1 by Ny)
    // v = y-velocity, stored on horizontal faces (Nx by Ny+1)
    std::vector<double> u;
    std::vector<double> v;

    // -------------------------------
    // Constructor
    // -------------------------------
    MACGrid(int Nx_, int Ny_);

    // -------------------------------
    // Indexing helpers (flatten 2D → 1D)
    // -------------------------------
    inline int idxP(int i, int j) const { return i + Nx * j; }         // pressure
    inline int idxU(int i, int j) const { return i + (Nx + 1) * j; }   // u-velocity
    inline int idxV(int i, int j) const { return i + Nx * j; }         // v-velocity

    // -------------------------------
    // Accessors
    // -------------------------------
    double getPressure(int i, int j) const;
    void setPressure(int i, int j, double val);

    double getU(int i, int j) const;
    void setU(int i, int j, double val);

    double getV(int i, int j) const;
    void setV(int i, int j, double val);

    // -------------------------------
    // Core fluid operations
    // -------------------------------
    double divergence(int i, int j) const;           // ∇·u in cell (i,j)
    void applyPressureGradient();                    // project to make velocity divergence-free
};

#include "MACGrid.h"

// -------------------------------
// Constructor
// -------------------------------
MACGrid::MACGrid(int Nx_, int Ny_)
    : Nx(Nx_), Ny(Ny_),
      pressure(Nx * Ny, 0.0),
      u((Nx + 1) * Ny, 0.0),
      v(Nx * (Ny + 1), 0.0) {}

// -------------------------------
// Accessors
// -------------------------------
double MACGrid::getPressure(int i, int j) const {
    return pressure[idxP(i,j)];
}
void MACGrid::setPressure(int i, int j, double val) {
    pressure[idxP(i,j)] = val;
}

double MACGrid::getU(int i, int j) const {
    return u[idxU(i,j)];
}
void MACGrid::setU(int i, int j, double val) {
    u[idxU(i,j)] = val;
}

double MACGrid::getV(int i, int j) const {
    return v[idxV(i,j)];
}
void MACGrid::setV(int i, int j, double val) {
    v[idxV(i,j)] = val;
}

// -------------------------------
// Compute divergence at cell center (i,j)
// -------------------------------
double MACGrid::divergence(int i, int j) const {
    // valid for 0 <= i < Nx, 0 <= j < Ny
    double dudx = (u[idxU(i+1, j)] - u[idxU(i, j)]) / cellSize;
    double dvdy = (v[idxV(i, j+1)] - v[idxV(i, j)]) / cellSize;
    return dudx + dvdy;
}

// -------------------------------
// Subtract pressure gradient from velocities
// -------------------------------
void MACGrid::applyPressureGradient() {
    // Adjust u velocities (skip boundaries)
    for (int j = 0; j < Ny; j++) {
        for (int i = 1; i < Nx; i++) { // skip i=0 and i=Nx faces
            double gradP = (pressure[idxP(i,j)] - pressure[idxP(i-1,j)]) / cellSize;
            u[idxU(i,j)] -= gradP;
        }
    }

    // Adjust v velocities (skip boundaries)
    for (int j = 1; j < Ny; j++) { // skip j=0 and j=Ny faces
        for (int i = 0; i < Nx; i++) {
            double gradP = (pressure[idxP(i,j)] - pressure[idxP(i,j-1)]) / cellSize;
            v[idxV(i,j)] -= gradP;
        }
    }
}

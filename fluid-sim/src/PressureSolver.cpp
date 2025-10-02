#include "PressureSolver.h"

void PressureSolver::solve(MACGrid& grid, float dt, float rho) {
    int Nx = grid.Nx;
    int Ny = grid.Ny;
    int maxIters = 100; // number of Jacobi iterations
    double alpha = -(MACGrid::cellSize * MACGrid::cellSize) / (rho * dt);
    double beta = 4.0;

    std::vector<double> b(Nx * Ny, 0.0); // right-hand side (divergence)
    std::vector<double> pNew(Nx * Ny, 0.0); // new pressure values

    // Build right-hand side
    for (int j = 0; j < Ny; j++) {
        for (int i = 0; i < Nx; i++) {
            b[grid.idxP(i,j)] = -grid.divergence(i,j);
        }
    }

    // Jacobi iterations
    for (int iter = 0; iter < maxIters; iter++) {
        for (int j = 0; j < Ny; j++) {
            for (int i = 0; i < Nx; i++) {
                double pL = (i > 0) ? grid.getPressure(i-1,j) : 0.0;
                double pR = (i < Nx-1) ? grid.getPressure(i+1,j) : 0.0;
                double pB = (j > 0) ? grid.getPressure(i,j-1) : 0.0;
                double pT = (j < Ny-1) ? grid.getPressure(i,j+1) : 0.0;

                pNew[grid.idxP(i,j)] = (pL + pR + pB + pT + alpha * b[grid.idxP(i,j)]) / beta;
            }
        }
        // Swap pressure arrays
        std::swap(grid.pressure, pNew);
    }

    // Apply pressure gradient to velocities
    grid.applyPressureGradient();
}
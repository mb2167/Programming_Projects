#include <iostream>
#include "Grid.hpp"
#include "Wavefunction.hpp"
#include "Solver.hpp"
#include "PotentialBarrier.hpp"
#include "Utils.hpp"

int main() {
    // Create grid
    Grid grid(128, 128, 40.0, 40.0);

    // Choose potential
    GaussianBarrier barrier(8.0, 0.0, 0.0, 2.0, 2.0);
    auto Vmap = barrier.compute(grid);

    // Initialize wavefunction
    Wavefunction psi(grid.Nx, grid.Ny);
    psi.initializeGaussian(grid, -10.0, 0.0, 2.0, 2.5, 0.0);

    save2DRealArray("potential.csv", Vmap, grid.Nx, grid.Ny);
    saveWavefunctionMagnitude("wave_init.csv", psi.psi, grid.Nx, grid.Ny);

    // Time evolution
    Solver solver(0.005);
    for (int step = 0; step < 10; ++step) {
        solver.propagateStep(psi, Vmap);
        std::cout << "Step " << step << " complete.\n";
    }

    saveWavefunctionMagnitude("wave_final.csv", psi.psi, grid.Nx, grid.Ny);

    std::cout << "Simulation finished.\n";

    return 0;
}

#include "Grid.hpp"
#include "Wavefunction.hpp"
#include "Solver.hpp"
#include "PotentialBarrier.hpp"
#include "Utils.hpp"

#include <filesystem>
#include <iostream>
#include <string>

// ---------- Simulation parameters ----------
constexpr int NX = 128;            // Number of grid points in x
constexpr int NY = 128;            // Number of grid points in y
constexpr double X_MAX = 40.0;     // Max x-coordinate
constexpr double Y_MAX = 40.0;     // Max y-coordinate

constexpr double POTENTIAL_HEIGHT = 8.0;   // V0 for Gaussian barrier
constexpr double BARRIER_X_CENTER = 0.0;   // x-center of barrier
constexpr double BARRIER_Y_CENTER = 0.0;   // y-center of barrier
constexpr double BARRIER_SIGMA_X = 2.0;    // width of barrier in x
constexpr double BARRIER_SIGMA_Y = 1e6;    // width of barrier in y

constexpr double WAVE_X0 = -10.0;          // initial wavefunction x-position
constexpr double WAVE_Y0 = 0.0;            // initial wavefunction y-position
constexpr double WAVE_SIGMA_X = 2.0;       // width of initial wavefunction in x
constexpr double WAVE_SIGMA_Y = 2.5;       // width of initial wavefunction in y
constexpr double WAVE_KX0 = 0.0;           // initial momentum (or phase) along x

constexpr double TIME_STEP = 0.005;        // solver time step
constexpr int NUM_STEPS = 100;             // total simulation steps

constexpr const char* DATA_FOLDER = "wave_data";  // folder to save wavefunction CSVs

// ---------- Main program ----------
int main() {
    // Create folder for wavefunction data
    std::filesystem::create_directory(DATA_FOLDER);

    // Create grid
    Grid grid(NX, NY, X_MAX, Y_MAX);

    // Choose potential
    GaussianBarrier barrier(POTENTIAL_HEIGHT,
                            BARRIER_X_CENTER,
                            BARRIER_Y_CENTER,
                            BARRIER_SIGMA_X,
                            BARRIER_SIGMA_Y);
    auto Vmap = barrier.compute(grid);

    // Save potential in the same folder
    save2DRealArray(std::string(DATA_FOLDER) + "/potential.csv", Vmap, grid.Nx, grid.Ny);

    // Initialize wavefunction
    Wavefunction psi(grid.Nx, grid.Ny);
    psi.initializeGaussian(grid,
                           WAVE_X0, WAVE_Y0,
                           WAVE_SIGMA_X, WAVE_SIGMA_Y,
                           WAVE_KX0);

    saveWavefunctionMagnitude(std::string(DATA_FOLDER) + "/wave_0.csv", psi.psi, grid.Nx, grid.Ny);

    // Time evolution
    Solver solver(TIME_STEP);
    for (int step = 1; step <= NUM_STEPS; ++step) {
        solver.propagateStep(psi, Vmap);
        std::cout << "Step " << step << " complete.\n";

        // Save wavefunction for this timestep
        std::string filename = std::string(DATA_FOLDER) + "/wave_" + std::to_string(step) + ".csv";
        saveWavefunctionMagnitude(filename, psi.psi, grid.Nx, grid.Ny);
    }

    std::cout << "Simulation finished.\n";
    return 0;
}
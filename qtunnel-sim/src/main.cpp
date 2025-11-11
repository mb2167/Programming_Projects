#include "Grid.hpp"
#include "Wavefunction.hpp"
#include "Solver.hpp"
#include "Utils.hpp"
#include "PotentialBarrier.hpp"

#include <filesystem>
#include <iostream>
#include <string>

constexpr int NX = 128;
constexpr int NY = 128;
constexpr double X_MAX = 40.0;
constexpr double Y_MAX = 40.0;

constexpr double POTENTIAL_HEIGHT = 8.0;
constexpr double BARRIER_X_CENTER = 0.0;
constexpr double BARRIER_Y_CENTER = 0.0;
constexpr double BARRIER_SIGMA_X = 2.0;
constexpr double BARRIER_SIGMA_Y = 1e6;

constexpr double WAVE_X0 = -10.0;
constexpr double WAVE_Y0 = 0.0;
constexpr double WAVE_SIGMA_X = 2.0;
constexpr double WAVE_SIGMA_Y = 2.5;
constexpr double WAVE_KX0 = 50.0;

constexpr double TIME_STEP = 0.005;
constexpr int NUM_STEPS = 100;  // just 10 steps for testing

constexpr const char* DATA_FOLDER = "wave_data";

int main() {
    std::filesystem::create_directory(DATA_FOLDER);

    // Grid
    Grid grid(NX, NY, X_MAX, Y_MAX);

    // Potential
    GaussianBarrier barrier(POTENTIAL_HEIGHT, BARRIER_X_CENTER, BARRIER_Y_CENTER,
                            BARRIER_SIGMA_X, BARRIER_SIGMA_Y);
    auto Vmap = barrier.compute(grid);
    save2DRealArray(std::string(DATA_FOLDER)+"/potential.csv", Vmap, NX, NY);

    // Wavefunction
    Wavefunction psi(NX, NY);
    psi.initializeGaussian(grid, WAVE_X0, WAVE_Y0, WAVE_SIGMA_X, WAVE_SIGMA_Y, WAVE_KX0, 0.0);
    saveWavefunctionMagnitude(std::string(DATA_FOLDER)+"/wave_0.csv", psi.psi, NX, NY);

    // Solver
    Solver solver(TIME_STEP, 1.0, 1.0);  // hbar=1, mass=1

    for (int step = 1; step <= NUM_STEPS; ++step) {
        solver.propagateStep(psi, Vmap, grid);
        std::string filename = std::string(DATA_FOLDER) + "/wave_" + std::to_string(step) + ".csv";
        saveWavefunctionMagnitude(filename, psi.psi, NX, NY);
        std::cout << "Step " << step << " complete.\n";
    }

    std::cout << "Simulation finished.\n";
    return 0;
}

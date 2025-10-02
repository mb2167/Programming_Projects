#pragma once
#include <vector>
#include "Particle.h"
#include "MACGrid.h"
#include "PressureSolver.h"

class Simulation {
public:
    float dt;
    float rho;
    MACGrid grid;
    std::vector<Particle> particles;
    PressureSolver solver;

    Simulation(int Nx, int Ny, float dx, float dy, float dt, float rho);

    void step();

private:
    void initializeParticlesInBox();
    void particleToGrid();
    void applyForces();
    void projectPressure();
    void gridToParticle();
    void advectParticles();
    void enforceBoundaries();
};

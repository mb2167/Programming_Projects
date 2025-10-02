#include "Simulation.h"

Simulation::Simulation(int Nx, int Ny, float dx, float dy, float dt, float rho)
    : dt(dt), rho(rho), grid(Nx, Ny) {
    initializeParticlesInBox();
}

void Simulation::step() {
    particleToGrid();
    applyForces();
    projectPressure();
    gridToParticle();
    advectParticles();
    enforceBoundaries();
}

void Simulation::initializeParticlesInBox() {
    int numParticlesX = grid.Nx * 5; // 5 particles per cell in x
    int numParticlesY = grid.Ny * 5 / 2; // fill half box in y
    particles.reserve(numParticlesX * numParticlesY);

    for (int j = 0; j < numParticlesY; j++) {
        for (int i = 0; i < numParticlesX; i++) {
            float px = (i + 0.5f) * (MACGrid::cellSize / 5.0f);
            float py = (j + 0.5f) * (MACGrid::cellSize / 5.0f);
            particles.push_back(Particle{{px, py}, {0.0, 0.0}});
        }
    }
};

void Simulation::particleToGrid() {
    // Reset grid velocities
    std::fill(grid.u.begin(), grid.u.end(), 0.0);
    std::fill(grid.v.begin(), grid.v.end(), 0.0);
    std::vector<int> uCount(grid.u.size(), 0);
    std::vector<int> vCount(grid.v.size(), 0);

    // Transfer particle velocities to grid using simple nearest-neighbor
    for (const auto& p : particles) {
        // Determine which cell the particle is in
        int i = static_cast<int>(p.pos.x / MACGrid::cellSize);
        int j = static_cast<int>(p.pos.y / MACGrid::cellSize);

        // Clamp to valid range
        if (i < 0) i = 0;
        if (i >= grid.Nx) i = grid.Nx - 1;
        if (j < 0) j = 0;
        if (j >= grid.Ny) j = grid.Ny - 1;

        // Nearest u face
        int iu = (p.pos.x < (i + 0.5f) * MACGrid::cellSize) ? i : i + 1;
        if (iu >= 0 && iu <= grid.Nx && j >= 0 && j < grid.Ny) {
            grid.u[grid.idxU(iu, j)] += p.vel.x;
            uCount[grid.idxU(iu, j)]++;
        }

        // Nearest v face
        int jv = (p.pos.y < (j + 0.5f) * MACGrid::cellSize) ? j : j + 1;
        if (i >= 0 && i < grid.Nx && jv >= 0 && jv <= grid.Ny) {
            grid.v[grid.idxV(i, jv)] += p.vel.y;
            vCount[grid.idxV(i, jv)]++;
        }
    }

    // Average contributions
    for (size_t idx = 0; idx < grid.u.size(); idx++) {
        if (uCount[idx] > 0) {
            grid.u[idx] /= uCount[idx];
        }
    }
    for (size_t idx = 0; idx < grid.v.size(); idx++) {
        if (vCount[idx] > 0) {
            grid.v[idx] /= vCount[idx];
        }
    }
};

void Simulation::applyForces() {
    // Add gravity to v velocities
    double gravity = -9.81; // m/s^2
    for (int j = 0; j < grid.Ny + 1; j++) {
        for (int i = 0; i < grid.Nx; i++) {
            double vOld = grid.getV(i, j);
            grid.setV(i, j, vOld + gravity * dt);
        }
    }
};

void Simulation::projectPressure() {
    solver.solve(grid, dt, rho);
};

void Simulation::gridToParticle() {
    for (auto& p : particles) {
        // Determine which cell the particle is in
        int i = static_cast<int>(p.pos.x / MACGrid::cellSize);
        int j = static_cast<int>(p.pos.y / MACGrid::cellSize);

        // Clamp to valid range
        if (i < 0) i = 0;
        if (i >= grid.Nx) i = grid.Nx - 1;
        if (j < 0) j = 0;
        if (j >= grid.Ny) j = grid.Ny - 1;

        // Bilinear interpolation of u and v velocities
        double fx = (p.pos.x - i * MACGrid::cellSize) / MACGrid::cellSize;
        double fy = (p.pos.y - j * MACGrid::cellSize) / MACGrid::cellSize;

        // Interpolate u (x-velocity)
        double u00 = grid.getU(i, j);
        double u10 = grid.getU(i + 1, j);
        double u01 = grid.getU(i, j + 1);
        double u11 = grid.getU(i + 1, j + 1);
        double uInterp = (1 - fx) * (1 - fy) * u00 + fx * (1 - fy) * u10 + (1 - fx) * fy * u01 + fx * fy * u11;

        // Interpolate v (y-velocity)
        double v00 = grid.getV(i, j);
        double v10 = grid.getV(i + 1, j);
        double v01 = grid.getV(i, j + 1);
        double v11 = grid.getV(i + 1, j + 1);
        double vInterp = (1 - fx) * (1 - fy) * v00 + fx * (1 - fy) * v10 + (1 - fx) * fy * v01 + fx * fy * v11;

        p.vel.x = uInterp;
        p.vel.y = vInterp;
    }
};

void Simulation::advectParticles() {
    for (auto& p : particles) {
        p.advect(dt);
    }
};

void Simulation::enforceBoundaries() {
    for (auto& p : particles) {
        if (p.pos.x < 0.0f) {
            p.pos.x = 0.0f;
            p.vel.x *= -0.5f; // simple bounce with damping
        }
        if (p.pos.x > grid.Nx * MACGrid::cellSize) {
            p.pos.x = grid.Nx * MACGrid::cellSize;
            p.vel.x *= -0.5f;
        }
        if (p.pos.y < 0.0f) {
            p.pos.y = 0.0f;
            p.vel.y *= -0.5f;
        }
        if (p.pos.y > grid.Ny * MACGrid::cellSize) {
            p.pos.y = grid.Ny * MACGrid::cellSize;
            p.vel.y *= -0.5f;
        }
    }
};

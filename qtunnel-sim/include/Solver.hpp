#pragma once
#include <vector>
#include <complex>
#include "Wavefunction.hpp"
#include "Grid.hpp"

class Solver {
public:
    double dt;
    double hbar;
    double mass;

    Solver(double dt_, double hbar_=1.0, double mass_=1.0);

    void propagateStep(Wavefunction& wf, const std::vector<double>& V, const Grid& grid);
};

#pragma once
#include "Wavefunction.hpp"
#include <vector>
#include <complex>

class Solver {
public:
    double dt;
    Solver(double dt_);
    void propagateStep(Wavefunction& wf, const std::vector<double>& V);
};

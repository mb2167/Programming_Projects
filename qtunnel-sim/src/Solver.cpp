#include "Solver.hpp"
#include <complex>
#include <cmath>

using namespace std::complex_literals;

Solver::Solver(double dt_) : dt(dt_) {}

void Solver::propagateStep(Wavefunction& wf, const std::vector<double>& V) {
    for (size_t i = 0; i < wf.psi.size(); ++i) {
        wf.psi[i] *= std::exp(-1i * V[i] * dt);
    }
}

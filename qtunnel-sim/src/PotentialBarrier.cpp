#include "PotentialBarrier.hpp"
#include <cmath>

// ---------- Gaussian Barrier ----------
GaussianBarrier::GaussianBarrier(double V0_, double xc_, double yc_, double sx_, double sy_)
    : V0(V0_), x_center(xc_), y_center(yc_), sigma_x(sx_), sigma_y(sy_) {}

std::vector<double> GaussianBarrier::compute(const Grid& grid) const {
    std::vector<double> V(grid.Nx * grid.Ny, 0.0);
    for (int j = 0; j < grid.Ny; ++j) {
        for (int i = 0; i < grid.Nx; ++i) {
            double x = grid.x[i];
            double y = grid.y[j];
            double exponent = -((x - x_center)*(x - x_center)/(2*sigma_x*sigma_x)
                               + (y - y_center)*(y - y_center)/(2*sigma_y*sigma_y));
            V[j*grid.Nx + i] = V0 * std::exp(exponent);
        }
    }
    return V;
}

// ---------- Double Gaussian Barrier ----------
DoubleGaussianBarrier::DoubleGaussianBarrier(double V0_, double separation_, double sigma_)
    : V0(V0_), separation(separation_), sigma(sigma_) {}

std::vector<double> DoubleGaussianBarrier::compute(const Grid& grid) const {
    std::vector<double> V(grid.Nx * grid.Ny, 0.0);
    double offset = separation / 2.0;
    for (int j = 0; j < grid.Ny; ++j) {
        for (int i = 0; i < grid.Nx; ++i) {
            double x = grid.x[i];
            double term1 = std::exp(-(x - offset)*(x - offset)/(2*sigma*sigma));
            double term2 = std::exp(-(x + offset)*(x + offset)/(2*sigma*sigma));
            V[j*grid.Nx + i] = V0 * (term1 + term2);
        }
    }
    return V;
}

// ---------- Step Barrier ----------
StepBarrier::StepBarrier(double V0_, double x_step_)
    : V0(V0_), x_step(x_step_) {}

std::vector<double> StepBarrier::compute(const Grid& grid) const {
    std::vector<double> V(grid.Nx * grid.Ny, 0.0);
    for (int j = 0; j < grid.Ny; ++j) {
        for (int i = 0; i < grid.Nx; ++i) {
            double x = grid.x[i];
            V[j*grid.Nx + i] = (x > x_step) ? V0 : 0.0;
        }
    }
    return V;
}

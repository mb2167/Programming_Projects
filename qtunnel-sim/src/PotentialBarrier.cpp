#include "PotentialBarrier.hpp"
#include <cmath>

// ---------- Gaussian Barrier ----------
/*
V0: Height of the barrier
xc, yc: Center position of the barrier
sx, sy: Standard deviations in x and y directions
*/
GaussianBarrier::GaussianBarrier(double V0_, double xc_, double yc_, double sx_, double sy_)
    : V0(V0_), x_center(xc_), y_center(yc_), sigma_x(sx_), sigma_y(sy_) {}

    std::vector<double> GaussianBarrier::compute(const Grid& grid) const {
        std::vector<double> V(grid.Nx * grid.Ny, 0.0);

        for (int j = 0; j < grid.Ny; ++j) {
            double y = grid.y[j];  // y-coordinate
            for (int i = 0; i < grid.Nx; ++i) {
                double x = grid.x[i];  // x-coordinate

                // 2D Gaussian
                double exponent_x = (x - x_center) * (x - x_center) / (2.0 * sigma_x * sigma_x);
                double exponent_y = (y - y_center) * (y - y_center) / (2.0 * sigma_y * sigma_y);
                double exponent = -(exponent_x + exponent_y);

                V[j * grid.Nx + i] = V0 * std::exp(exponent);
            }
        }

    return V;
}



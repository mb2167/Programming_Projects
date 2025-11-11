#include "Wavefunction.hpp"
#include <complex>
#include <cmath>

Wavefunction::Wavefunction(int Nx_, int Ny_) : Nx(Nx_), Ny(Ny_) {
    psi.resize(Nx * Ny, 0.0);
}

void Wavefunction::initializeGaussian(const Grid& grid,
                                      double x0, double y0,
                                      double sigmaX, double sigmaY,
                                      double kx0, double ky0) {
    for (int j = 0; j < Ny; ++j) {
        for (int i = 0; i < Nx; ++i) {
            double x = grid.x[i];
            double y = grid.y[j];
            double envelope = std::exp(-((x - x0)*(x - x0)/(2*sigmaX*sigmaX)
                                        + (y - y0)*(y - y0)/(2*sigmaY*sigmaY)));
            std::complex<double> phase = std::exp(std::complex<double>(0,1)*(kx0*x + ky0*y));
            psi[j*Nx + i] = envelope * phase;
        }
    }
}

#include <iostream>
#include <fstream>
#include <vector>
#include <complex>
#include <string>

void saveRealArray(const std::string& filename, const std::vector<double>& data, int Nx, int Ny) {
    std::ofstream file(filename);
    for (int j = 0; j < Ny; ++j) {
        for (int i = 0; i < Nx; ++i)
            file << data[j*Nx + i] << (i == Nx-1 ? '\n' : ' ');
    }
}

void save2DRealArray(const std::string& filename, const std::vector<double>& data, int Nx, int Ny) {
    std::ofstream file(filename);
    for (int j = 0; j < Ny; ++j) {
        for (int i = 0; i < Nx; ++i) {
            file << data[j * Nx + i];
            if (i < Nx - 1) file << ",";
        }
        file << "\n";
    }
}

void saveWavefunctionMagnitude(const std::string& filename,
                               const std::vector<std::complex<double>>& psi,
                               int Nx, int Ny) {
    std::ofstream file(filename);
    for (int j = 0; j < Ny; ++j) {
        for (int i = 0; i < Nx; ++i) {
            double mag2 = std::norm(psi[j * Nx + i]);
            file << mag2;
            if (i < Nx - 1) file << ",";
        }
        file << "\n";
    }
}

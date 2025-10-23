#pragma once
#include <string>
#include <vector>
#include <complex>

void save2DRealArray(const std::string& filename, const std::vector<double>& data, int Nx, int Ny);
void saveRealArray(const std::string& filename, const std::vector<double>& data, int Nx, int Ny);
void saveWavefunctionMagnitude(const std::string& filename,
                               const std::vector<std::complex<double>>& psi,
                               int Nx, int Ny);

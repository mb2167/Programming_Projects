#pragma once
#include "Grid.hpp"
#include <vector>

class PotentialBarrier {
public:
    virtual ~PotentialBarrier() = default;
    virtual std::vector<double> compute(const Grid& grid) const = 0;
};

// --- Concrete Barrier Types ---
class GaussianBarrier : public PotentialBarrier {
public:
    double V0, x_center, y_center, sigma_x, sigma_y;
    GaussianBarrier(double V0_, double xc_, double yc_, double sx_, double sy_);
    std::vector<double> compute(const Grid& grid) const override;
};

class DoubleGaussianBarrier : public PotentialBarrier {
public:
    double V0, separation, sigma;
    DoubleGaussianBarrier(double V0_, double separation_, double sigma_);
    std::vector<double> compute(const Grid& grid) const override;
};

class StepBarrier : public PotentialBarrier {
public:
    double V0, x_step;
    StepBarrier(double V0_, double x_step_);
    std::vector<double> compute(const Grid& grid) const override;
};

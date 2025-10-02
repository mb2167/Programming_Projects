#pragma once
#include "MACGrid.h"

class PressureSolver {
public:
    PressureSolver();
    void solve(MACGrid& grid, float dt, float rho);
};

#include <iostream>
#include <fstream>
#include <vector>
#include "body.h"
#include "simulation.h"
#include "utils.h"

int main() {
    std::ofstream out(getOutputDir() + "/trajectory.csv");

    std::vector<Body> bodies = {
        {1e24, {0, 0, 1e7}, {0, 0, 0}}, 
        {1e24, {1e7, 0, 1e7}, {0, 1e3, 0}}, 
        {1e24, {0, 1e7, 0}, {-1e3, 0, 0}}
    };

    double timeStep = 1; // seconds
    int steps = 10000;

    for (int step = 0; step < steps; ++step) {
        simulateStep(bodies, timeStep, out, step);
    }

    out.close();
    return 0;
}

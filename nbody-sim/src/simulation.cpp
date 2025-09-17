#include "simulation.h"
#include "physics.h"

void simulateStep(std::vector<Body>& bodies, double timeStep, std::ofstream& out, int step) {
    auto accelerations = computeAccelerations(bodies);
    velocityUpdate(bodies, accelerations, 0.5 * timeStep);
    positionUpdate(bodies, timeStep);
    accelerations = computeAccelerations(bodies);
    velocityUpdate(bodies, accelerations, 0.5 * timeStep);

    out << step;
    for (auto& body : bodies) {
        out << "," << body.position.x << "," << body.position.y << "," << body.position.z;
    }
    out << "\n";
}

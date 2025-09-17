#include "physics.h"
#include <cmath>

const double G = 6.67430e-11; // gravitational constant

Vector3 computeGravitationalForce(const Body& a, const Body& b) {
    Vector3 direction = b.position - a.position;
    double distance = std::sqrt(direction.x * direction.x +
                                direction.y * direction.y +
                                direction.z * direction.z);
    if (distance == 0) return {0, 0, 0};
    double forceMagnitude = (G * a.mass * b.mass) / (distance * distance);
    return direction * (forceMagnitude / distance);
}

std::vector<Vector3> computeAccelerations(const std::vector<Body>& bodies) {
    std::vector<Vector3> accelerations(bodies.size(), {0,0,0});
    for (size_t i = 0; i < bodies.size(); ++i) {
        for (size_t j = 0; j < bodies.size(); ++j) {
            if (i != j) {
                accelerations[i] += computeGravitationalForce(bodies[i], bodies[j]) * (1.0 / bodies[i].mass);
            }
        }
    }
    return accelerations;
}

void velocityUpdate(std::vector<Body>& bodies, const std::vector<Vector3>& accelerations, double factor) {
    for (size_t i = 0; i < bodies.size(); ++i) {
        bodies[i].velocity = bodies[i].velocity + accelerations[i] * factor;
    }
}

void positionUpdate(std::vector<Body>& bodies, double timeStep) {
    for (auto& body : bodies) {
        body.position = body.position + body.velocity * timeStep;
    }
}

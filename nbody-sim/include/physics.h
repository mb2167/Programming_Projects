#pragma once
#include <vector>
#include "body.h"

Vector3 computeGravitationalForce(const Body& a, const Body& b);
std::vector<Vector3> computeAccelerations(const std::vector<Body>& bodies);
void velocityUpdate(std::vector<Body>& bodies, const std::vector<Vector3>& accelerations, double factor);
void positionUpdate(std::vector<Body>& bodies, double timeStep);

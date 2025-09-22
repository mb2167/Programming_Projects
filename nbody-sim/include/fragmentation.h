#pragma once

#include <vector>
#include "body.h"
#include "vector3.h"

// --- Fragmentation Score Components ---
double computeMaterialFactor(const Body& body);
double computeGravityResistance(const Body& body);
double computeImpactEnergy(const Body& target, const Body& impactor, double relativeVelocity);
double computeSpinFactor(const Body& body);
double computeTemperatureFactor(const Body& body);

// Combined score in [0,1]
double computeFragmentationScore(const Body& target, const Body& impactor, double relativeVelocity);

// --- Fragment Generation ---
std::vector<Body> generateFragments(const Body& parent, double fragmentationScore, const Vector3& impactVelocity);

std::vector<double> distributeFragmentMasses(double totalFragmentMass);
std::vector<Vector3> assignFragmentVelocities(const std::vector<double>& fragmentMasses,
                                              const Vector3& impactVelocity);

void enforceMomentumConservation(std::vector<Body>& fragments, const Vector3& originalMomentum);
void enforceEnergyBudget(std::vector<Body>& fragments, double availableEnergy);

// --- Fragment Positioning ---
Vector3 sampleEjectionPoint(const Body& a, const Body& b);

#endif // FRAGMENTATION_H

#include "fragmentation.h"
#include "constants.h"
#include <cmath>
#include <random>

// --- Fragmentation Score Components ---

double computeMaterialFactor(const Body& body) {
    double porosity = std::min(body.porosity, 1.0 - eps);
    double brittleness = std::min(body.brittleness, 1.0 - eps);
    double FragmentationFactor = (1.0 - porosity) * (1.0 - brittleness);

    return FragmentationFactor;
}


double computeGravityResistance(const Body& body) {
    double surfaceGravityNormalized(const Body& body) {
    constexpr double minGravity = 1e-5; // tiny rubble pile asteroid
    constexpr double maxGravity = 30.0; // ~Jupiter upper bound

    double g = GravitationalConstant * body.mass / (body.radius * body.radius);

    double logMin = std::log1p(minGravity);
    double logMax = std::log1p(maxGravity);
    double logG   = std::log1p(g);

    double norm = (logG - logMin) / (logMax - logMin);
    double FragmentationFactor = std::clamp(norm, 0.0, 1.0);

    return FragmentationFactor;
    }

}

#include <cmath>
#include <algorithm>

double computeImpactEnergy(const Body& target, const Body& impactor) {
    // Vector from target to impactor
    Vector3 impactVector = impactor.position - target.position;

    // Relative velocity
    Vector3 relVel = impactor.velocity - target.velocity;

    // Project relative velocity onto collision normal (impactVector)
    double distance = impactVector.magnitude();
    if (distance == 0) distance = 1e-6; // avoid division by zero

    Vector3 impactNormal = impactVector / distance; // normalized
    double normalVelocity = relVel.dot(impactNormal); // velocity along impact line

    // Ignore negative values (receding bodies don’t fragment)
    normalVelocity = std::max(0.0, normalVelocity);

    // Reduced mass
    double m1 = target.mass;
    double m2 = impactor.mass;
    double reducedMass = (m1 * m2) / (m1 + m2);

    // Impact energy along normal
    double impactEnergy = 0.5 * reducedMass * normalVelocity * normalVelocity;

    // Target binding energy
    double bindingEnergy = (3.0 / 5.0) * GravitationalConstant * m1 * m1 / target.radius;

    // Fragmentation factor
    double FragmentationFactor = std::clamp(impactEnergy / bindingEnergy, 0.0, 1.0);

    return FragmentationFactor;
}


double computeSpinFactor(const Body& body) {
    // TODO: implement ratio of centrifugal to gravitational acceleration
    double surfaceGravity = (G * body.mass) / (body.radius * body.radius);
    double centrifugal = body.angularVelocity.x * body.angularVelocity.x * body.radius; 
    double FragmentationFactor = std::min(1.0, centrifugal / surfaceGravity);

    return FragmentationFactor;

}

double computeTemperatureFactor(const Body& body) {
    FragmentationFactor = std::clamp(body.temperature / body.meltTemperature, 0.0, 1.0);

    return FragmentationFactor;
}

double computeFragmentationScore(const Body& target, const Body& impactor, double relativeVelocity) {
    GravitationalFactor = computeGravityResistance(target);
    MaterialFactor = computeMaterialFactor(target);
    ImpactFactor = computeImpactEnergy(target, impactor, relativeVelocity);
    SpinFactor = computeSpinFactor(target);
    TemperatureFactor = computeTemperatureFactor(target);

    double TotalScore = GravitationalFactor * MaterialFactor * ImpactFactor * SpinFactor * TemperatureFactor;

    return TotalScore;
}

// --- Fragment Generation ---

std::vector<Body> generateFragments(const Body& parent, double fragmentationScore, const Vector3& impactVelocity) {
    // TODO: create fragments from parent body
    return {};
}

std::vector<double> distributeFragmentMasses(double totalFragmentMass) {
    // TODO: implement power-law fragment mass distribution
    return {};
}

std::vector<Vector3> assignFragmentVelocities(const std::vector<double>& fragmentMasses,
                                              const Vector3& impactVelocity) {
    // TODO: assign velocities (smaller fragments faster)
    return {};
}

void enforceMomentumConservation(std::vector<Body>& fragments, const Vector3& originalMomentum) {
    // TODO: rescale fragment velocities to conserve momentum
}

void enforceEnergyBudget(std::vector<Body>& fragments, double availableEnergy) {
    // TODO: rescale velocities to not exceed available kinetic energy
}

// --- Fragment Positioning ---

Vector3 sampleEjectionPoint(const Body& a, const Body& b) {
    // TODO: random point on intersection edge, perpendicular to surfaces
    return {0.0, 0.0, 0.0};
}

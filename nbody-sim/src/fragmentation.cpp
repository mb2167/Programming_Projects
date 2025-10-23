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
    Vector3 impactVector = impactor.position - target.position;

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

std::vector<double> distributeFragmentMasses(double totalFragmentMass) {
    std::vector<double> fragmentMasses;
    double remainingMass = totalFragmentMass;

    float fragmentationExponent = 2.5f;                // slope for power-law bias
    double minFragmentMass = 0.001 * totalFragmentMass; // minimum allowed fragment mass

    std::random_device randomDevice;
    std::mt19937 randomEngine(randomDevice());
    std::uniform_real_distribution<double> uniformDistribution(0.0, 1.0);

    while (remainingMass > minFragmentMass) {
        double randomFraction = uniformDistribution(randomEngine);  

        // Power-law distributed fragment mass
        double fragmentMass = remainingMass * std::pow(randomFraction, fragmentationExponent);

        // Clamp to [minFragmentMass, remainingMass]
        fragmentMass = std::clamp(fragmentMass, minFragmentMass, remainingMass);

        fragmentMasses.push_back(fragmentMass);
        remainingMass -= fragmentMass;
    }

    // Add leftover as one final fragment
    if (remainingMass > 0) {
        fragmentMasses.push_back(remainingMass);
    }

    return fragmentMasses;
}

std::vector<Vector3> assignFragmentVelocities(const std::vector<double>& fragmentMasses,
                                              const Vector3& impactVelocity) {
    std::vector<Vector3> fragmentVelocities;
    fragmentVelocities.reserve(fragmentMasses.size());

    // Compute total fragment mass
    double totalFragmentMass = 0.0;
    for (double fragmentMass : fragmentMasses) {
        totalFragmentMass += fragmentMass;
    }

    // Parameters
    double velocityScale = 1.0;   // v0, tunable scaling constant
    double beta = 1.0 / 3.0;      // typical exponent

    // Random direction generator
    std::random_device randomDevice;
    std::mt19937 randomEngine(randomDevice());
    std::uniform_real_distribution<double> uniformDistribution(0.0, 1.0);
    std::uniform_real_distribution<double> uniformAngle(0.0, 2.0 * M_PI);

    for (double fragmentMass : fragmentMasses) {
        // Normalized mass ratio
        double massRatio = fragmentMass / totalFragmentMass;

        // Velocity magnitude from scaling law
        double fragmentSpeed = velocityScale * std::pow(massRatio, -beta);

        // Random isotropic direction
        double z = 2.0 * uniformDistribution(randomEngine) - 1.0;
        double theta = uniformAngle(randomEngine);
        double r = std::sqrt(1.0 - z * z);

        Vector3 randomDirection(r * std::cos(theta),
                                r * std::sin(theta),
                                z);

        // Final velocity = impact velocity + scaled random component
        Vector3 fragmentVelocity = impactVelocity + randomDirection * fragmentSpeed;

        fragmentVelocities.push_back(fragmentVelocity);
    }

    return fragmentVelocities;
}

std::vector<Body> generateFragments(const Body& parent, 
                                    double fragmentationScore, 
                                    const Vector3& impactVelocity) {
    // 1. Decide how much of parent breaks up
    double totalFragmentMass = parent.mass * fragmentationScore;

    // 2. Distribute that into a mass spectrum
    auto fragmentMasses = distributeFragmentMasses(totalFragmentMass);

    // 3. Assign velocities using scaling law
    auto fragmentVelocities = assignFragmentVelocities(fragmentMasses, impactVelocity);

    // 4. Create fragment objects
    std::vector<Body> fragments;
    for (size_t i = 0; i < fragmentMasses.size(); ++i) {
        Body fragment;
        fragment.mass = fragmentMasses[i];
        fragment.velocity = fragmentVelocities[i];
        fragment.position = parent.position;  // start at parent center (could randomize)
        fragments.push_back(fragment);
    }

    return fragments;
}



void enforceMomentumConservation(std::vector<Body>& fragments,
                                 const Vector3& parentMomentum) {
    // Compute current momentum
    Vector3 fragmentMomentum(0.0, 0.0, 0.0);
    double totalMass = 0.0;

    for (const auto& frag : fragments) {
        fragmentMomentum += frag.velocity * frag.mass;
        totalMass += frag.mass;
    }

    // Difference in momentum
    Vector3 momentumError = fragmentMomentum - parentMomentum;

    // Velocity correction to apply to all fragments
    Vector3 velocityCorrection = momentumError / totalMass;

    for (auto& frag : fragments) {
        frag.velocity -= velocityCorrection;
    }
}


void enforceEnergyBudget(std::vector<Body>& fragments, double availableEnergy) {
    // Compute current KE
    double currentEnergy = 0.0;
    for (const auto& frag : fragments) {
        currentEnergy += 0.5 * frag.mass * frag.velocity.lengthSquared();
    }

    // If too high, rescale velocities
    if (currentEnergy > availableEnergy && currentEnergy > 0.0) {
        double scale = std::sqrt(availableEnergy / currentEnergy);
        for (auto& frag : fragments) {
            frag.velocity *= scale;
        }
    }
}

// --- Fragment Positioning ---

Vector3 sampleEjectionPoint(const Body& a, const Body& b) {
    // TODO: random point on intersection edge, perpendicular to surfaces
    return {0.0, 0.0, 0.0};
}

#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <string>
#include <filesystem>

const double G = 6.67430e-11; // gravitational constant

// ----------------- Utility -----------------
std::string getSourceDir() {
    std::string path = __FILE__;
    return std::filesystem::path(path).parent_path().string();
}

// ----------------- Vector Struct -----------------
struct Vector3 {
    double x, y, z;
    Vector3 operator+(const Vector3& other) const {
        return {x + other.x, y + other.y, z + other.z};
    }
    Vector3 operator-(const Vector3& other) const {
        return {x - other.x, y - other.y, z - other.z};
    }
    Vector3 operator*(double scalar) const {
        return {x * scalar, y * scalar, z * scalar};
    }
    Vector3& operator+=(const Vector3& other) {
        x += other.x; y += other.y; z += other.z;
        return *this;
    }
};

// ----------------- Body Struct -----------------
struct Body {
    double mass;
    Vector3 position;
    Vector3 velocity;
};

// ----------------- Physics -----------------
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

// ----------------- Simulation -----------------
void simulateStep(std::vector<Body>& bodies, double timeStep, std::ofstream& out, int step) {
    // 1. Compute accelerations
    auto accelerations = computeAccelerations(bodies);

    // 2. First half velocity update
    velocityUpdate(bodies, accelerations, 0.5 * timeStep);

    // 3. Position update
    positionUpdate(bodies, timeStep);

    // 4. Recompute accelerations
    accelerations = computeAccelerations(bodies);

    // 5. Second half velocity update
    velocityUpdate(bodies, accelerations, 0.5 * timeStep);

    // Save positions
    out << step;
    for (auto& body : bodies) {
        out << "," << body.position.x << "," << body.position.y << "," << body.position.z;
    }
    out << "\n";
}

// ----------------- Main -----------------
int main() {
    std::ofstream out(getSourceDir() + "/trajectory.csv");

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

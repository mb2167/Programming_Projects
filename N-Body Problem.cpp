#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <string>
#include <filesystem>

const double G = 6.67430e-11; // gravitational constant

std::string getSourceDir() {
    std::string path = __FILE__;               // full path of this .cpp file
    return std::filesystem::path(path).parent_path().string();
}

std::ofstream out(getSourceDir() + "/trajectory.csv");

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
    };
};

struct Body {
    double mass;
    Vector3 position;
    Vector3 velocity;
};

Vector3 computeGravitationalForce(const Body& a, const Body& b) {
    Vector3 direction = b.position - a.position;
    double distance = std::sqrt(direction.x * direction.x + direction.y * direction.y + direction.z * direction.z);
    if (distance == 0) return {0, 0, 0}; // avoid division by zero
    double forceMagnitude = (G * a.mass * b.mass) / (distance * distance);
    return direction * (forceMagnitude / distance); // normalize and scale
};



int main() {
    std::vector<Body> bodies = {
        {1e24, {0, 0, 1e7}, {0, 0, 0}}, // Body 1
        {1e24, {1e7, 0, 1e7}, {0, 1e3, 0}}, // Body 2
        {1e24, {0, 1e7, 0}, {-1e3, 0, 0}} // Body 3
    };

    double timeStep = 1; // seconds
    int steps = 10000;

    for (int step = 0; step < steps; ++step) {
        std::vector<Vector3> forces(bodies.size(), {0, 0, 0});

        // Compute forces
        for (size_t i = 0; i < bodies.size(); ++i) {
            for (size_t j = 0; j < bodies.size(); ++j) {
                if (i != j) {
                    forces[i] = forces[i] + computeGravitationalForce(bodies[i], bodies[j]);
                }
            }
        }

        // Update velocities and positions
        for (size_t i = 0; i < bodies.size(); ++i) {
            Vector3 acceleration = forces[i] * (1.0 / bodies[i].mass);
            bodies[i].velocity = bodies[i].velocity + acceleration * timeStep;
            bodies[i].position = bodies[i].position + bodies[i].velocity * timeStep;
        }
        out << step;
        for (auto& body : bodies) {
            out << "," << body.position.x << "," << body.position.y << "," << body.position.z;
        }
        out << "\n";
    }
    out.close();

    // Output final positions
    for (const auto& body : bodies) {
        std::cout << "Position: (" << body.position.x << ", " << body.position.y << ", " << body.position.z << ")\n";
    }

    return 0;
};
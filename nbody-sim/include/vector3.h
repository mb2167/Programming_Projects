#pragma once
#include <cmath>

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

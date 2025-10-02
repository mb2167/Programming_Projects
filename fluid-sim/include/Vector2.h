#pragma once
#include <cmath>

struct Vector2 {
    double x, y;

    // Constructors
    Vector2();
    Vector2(double x, double y);

    // Operators
    Vector2 operator+(const Vector2& other) const;
    Vector2 operator-(const Vector2& other) const;
    Vector2 operator*(double scalar) const;
    Vector2 operator/(double scalar) const;
    Vector2& operator+=(const Vector2& other);

    // Math functions
    double dot(const Vector2& other) const;
    double cross(const Vector2& other) const;
    double length() const;
    double lengthSquared() const;
    Vector2 normalised() const;

};

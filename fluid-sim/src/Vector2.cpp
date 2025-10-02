#include "Vector2.h"

// Constructors
Vector2::Vector2() : x(0.0), y(0.0) {}
Vector2::Vector2(double x_, double y_) : x(x_), y(y_) {}

// Operators
Vector2 Vector2::operator+(const Vector2& other) const {
    return {x + other.x, y + other.y};
}
Vector2 Vector2::operator-(const Vector2& other) const {
    return {x - other.x, y - other.y};
}
Vector2 Vector2::operator*(double scalar) const {
    return {x * scalar, y * scalar};
}
Vector2 Vector2::operator/(double scalar) const {
    return {x / scalar, y / scalar};
}
Vector2& Vector2::operator+=(const Vector2& other) {
    x += other.x;
    y += other.y;
    return *this;
}

// Math functions
double Vector2::dot(const Vector2& other) const {
    return x * other.x + y * other.y;
}
double Vector2::cross(const Vector2& other) const {
    return x * other.y - y * other.x;
}
double Vector2::length() const {
    return std::sqrt(x * x + y * y);
}
double Vector2::lengthSquared() const {
    return x * x + y * y;
}
Vector2 Vector2::normalised() const {
    double len = length();
    if (len > 1e-8) {
        return {x / len, y / len};
    } else {
        return {0.0, 0.0};
    }
}

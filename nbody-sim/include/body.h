#pragma once
#include "vector3.h"

struct Body {
    // Core properties
    double mass;          // kg
    double radius;        // m
    double density;       // kg/m^3

    // State vectors
    Vector3 position;     // m
    Vector3 velocity;     // m/s
    Vector3 angularVelocity; // rad/s (for spin)

    // Material properties
    double porosity;      // 0 = solid, 1 = highly porous
    double brittleness;   // 0 = ductile, 1 = brittle

    // Thermal state
    double temperature;   // K
    double meltTemperature; // K

};

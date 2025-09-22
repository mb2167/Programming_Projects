#pragma once

#include <vector>
#include "body.h"
#include "vector3.h"

// Simple collision check
bool checkCollision(const Body& a, const Body& b);

// Handles outcome: merge, bounce, or fragmentation
std::vector<Body> handleCollision(const Body& a, const Body& b);

#endif // COLLISION_H

#include "collision.h"
#include "fragmentation.h"
#include <cmath>

bool checkCollision(const Body& a, const Body& b) {
    float dx = a.position.x - b.position.x;
    float dy = a.position.y - b.position.y;
    float dz = a.position.z - b.position.z;

    float radii = a.radius + b.radius;

    return (dx * dx + dy * dy + dz * dz) <= (radii * radii);
}


std::vector<Body> handleCollision(const Body& a, const Body& b) {
    // TODO:
    // 1. Compute relative velocity
    // 2. Compute fragmentation score
    // 3. If score > threshold → generate fragments
    // 4. Else → merge or bounce
    return {};
}

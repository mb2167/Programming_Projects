#pragma once
#include "Vector2.h"

struct Particle {
    Vector2 pos;
    Vector2 vel;

    void advect(float dt);
};

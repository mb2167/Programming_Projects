#include "Particle.h"

void Particle::advect(float dt) {
    pos += vel * dt;
}
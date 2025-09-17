#pragma once
#include <vector>
#include <fstream>
#include "body.h"

void simulateStep(std::vector<Body>& bodies, double timeStep, std::ofstream& out, int step);

#include <iostream>
#include <fstream>
#include <vector>
#include "utils.h"

int main() {
    std::ofstream out(getOutputDir() + "/output.csv");

    
    out.close();
    return 0;
}
#include <iostream>
#include <fstream>
#include <vector>

int main() {
    std::ofstream out(getOutputDir() + "/output.csv");

    
    out.close();
    return 0;
}
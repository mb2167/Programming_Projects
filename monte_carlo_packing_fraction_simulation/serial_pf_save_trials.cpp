/* 
The program is the same as the previous version, but it includes parts that save the trial and packing fraction
data to a txt file. This was added as another file as it could add potential slow down due to the extra functionality
that does not affect the MPI tests
*/

#include <iostream>
#include <vector>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <random>
#include <chrono>
#include <fstream>

struct Circle {
    double x, y;    //define x coordinate and y coordinate for the Circle structure
};

//Checks whether the two input circles are overlapping
bool isOverlapping(const Circle& a, const Circle& b, double r) {
    double dx = a.x - b.x;
    double dy = a.y - b.y;
    return (dx*dx + dy*dy) < 4*r*r;         //Checks if the square of the distance between the circle centres is less than the square of diameter
}

// Timer class for high-resolution timing.
class vtimer_t {
    private:
        std::chrono::high_resolution_clock::time_point start_time;
        std::chrono::high_resolution_clock::time_point end_time;

    public:
        void start() {
            // Record the start time
            start_time = std::chrono::high_resolution_clock::now();
        }

        void stop() {
            // Record the end time
            end_time = std::chrono::high_resolution_clock::now();
        }

        double elapsed_time() const {
            // Calculate and return the elapsed time in seconds
            return 1.e-9 * double(std::chrono::duration_cast<std::chrono::nanoseconds>(end_time - start_time).count());
        }
};

//Random number generator class
class rng {
    std::mt19937 mt;
    std::uniform_real_distribution<double> dist;

public:
    void seed(unsigned int random_seed) {
        dist = std::uniform_real_distribution<double>(0.0, 1.0);
        mt.seed(random_seed);
    }

    double grnd() {
        return dist(mt);
    }
};

int main() {

    vtimer_t timer;
    timer.start();
    //Variable initialisation

    int maxNoChangeTrials;
    std::cout << "================================================" << std::endl;
    std::cout << "Hard Sphere Packing Fraction Simulation" << std::endl;
    std::cout << "Enter max trials without change (e.g., 10000): ";
    std::cin >> maxNoChangeTrials;
    
    if (maxNoChangeTrials <= 0) {
        std::cerr << "Error: Trials must be a positive integer." << std::endl;
        return 1;
    }
    
    const double box_length = 200.0;
    const double circ_radius = 1.234;
    double previous_PF = 0.0;
    double current_PF = 0.0;
    int trial = 0;
    int noChangeCount = 0;                              //Count how many trials there are without a change in the packing fraction
    std::vector<Circle> circles;                        //Array to hold all the valid circles
    rng randomGenerator;                                //Create an instance of the rng class

    randomGenerator.seed(static_cast<unsigned int>(time(nullptr)));

    std::ofstream outFile("packing_fraction_data.txt"); // Create an ofstream object for output

    // Check if file is open
    if (!outFile.is_open()) {
        std::cerr << "Failed to open file for writing." << std::endl;
        return 1;
    }

    while (noChangeCount < maxNoChangeTrials) {
        Circle newCircle = {box_length * randomGenerator.grnd(), box_length * randomGenerator.grnd()};      //Generate a circle at a random location
        bool valid = true;

        for (const auto& circle : circles) {
            if (isOverlapping(circle, newCircle, circ_radius)) {
                valid = false;
                break;
            }
        }
        //If the circle is not overlapping and within the bounds of the box
        if (valid && newCircle.x + circ_radius <= box_length && newCircle.y + circ_radius <= box_length\
                  && newCircle.x - circ_radius >= 0 && newCircle.y - circ_radius >= 0) {
            circles.push_back(newCircle);                                                                   //Add circle to the array
            previous_PF = current_PF;
            current_PF = M_PI * circles.size() * circ_radius * circ_radius / (box_length * box_length);

            if (previous_PF == current_PF) {
                noChangeCount++;
            } else {
                noChangeCount = 0;                      // Reset counter if there's a change
            }
        } else {
            noChangeCount++;                            // Increment if no circle is added
        }

        trial++;

        //Every 10000 trials display the results
        if (trial % 10000 == 0) {
            std::cout << "Trial: " << trial << "\tPacking Fraction: " << current_PF << "\tnoChangeCount: "<< noChangeCount << std::endl;
            outFile << trial <<"\t"<< current_PF << std::endl; // Write to file

        }
    }
    timer.stop();
    std::cout << "Final Packing Fraction: " << current_PF << std::endl;
    std::cout << "Time taken: " << timer.elapsed_time() << std::endl;
    std::cout << "Circles in the segment (0, 0.025L):" << std::endl;

    //Display every circle within the bounds of the given area
    for (const auto& circle : circles) {
        if (circle.x < 0.025 * box_length && circle.y < 0.025 * box_length) {
            std::cout << "Circle at (" << circle.x << ", " << circle.y << ")" << std::endl;
        }
    }

    outFile.close();
    return 0;
}

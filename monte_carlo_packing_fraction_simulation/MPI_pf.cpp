/*
This program determines the packing fraction via MPI parallel code

It saves the circle coordinates of rank 0 and 1 in a .txt file
*/

#include <iostream>
#include <vector>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <mpi.h>
#include <random>
#include <chrono>
#include <fstream>
#include <string>

// Timer class
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
            // Return the elapsed time
            return 1.e-9 * double(std::chrono::duration_cast<std::chrono::nanoseconds>(end_time - start_time).count());
        }
};

// Random number generator class
class rng {
    std::mt19937 mt; // Mersenne Twister generator
    std::uniform_real_distribution<double> dist; // Uniform distribution

    public:
        rng() : dist(0.0, 1.0) {
            // Initialize the uniform distribution between 0.0 and 1.0
        }

        void seed(unsigned int random_seed) {
            // Seed the generator
            mt.seed(random_seed);
        }

        double grnd() {
            // Generate a random number using the distribution
            return dist(mt);
        }
};

// Checks whether the two input circles are overlapping
bool isOverlapping(const std::vector<double>& a, double bx, double by, double r) {
    double dx = a[0] - bx;
    double dy = a[1] - by;
    return (dx * dx + dy * dy) < 4 * r * r; // Checks if the square of the distance between the circle centres is less than the square of diameter
}

// Send border circles to another MPI process.
void sendBorderCircles(const std::vector<double>& circles, int destination, MPI_Request& request) {
    MPI_Isend(circles.data(), circles.size(), MPI_DOUBLE, destination, 0, MPI_COMM_WORLD, &request);
}

// Function to receive border circles from another MPI process.
void receiveBorderCircles(std::vector<double>& circles, int source, MPI_Request& request) {
    MPI_Status status;
    int count;
    // Probe for incoming data to determine its size
    MPI_Probe(source, 0, MPI_COMM_WORLD, &status);
    MPI_Get_count(&status, MPI_DOUBLE, &count);
    // Resize the vector to fit the incoming data
    circles.resize(count);
    MPI_Irecv(circles.data(), count, MPI_DOUBLE, source, 0, MPI_COMM_WORLD, &request);
}

int main(int argc, char** argv) {

    vtimer_t timer;
    timer.start();              // Create an instance of the timer class and start the timer

    MPI_Init(&argc, &argv);

    int size, rank;
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    MPI_Request sendRequestRight, sendRequestLeft;
    MPI_Request recvRequestRight, recvRequestLeft;

    // Define values for each rank's adjacent neighbour
    int leftNeighbour = rank - 1;
    int rightNeighbour = rank + 1;

    // Initialise variables
    const double box_length = 200.0;
    const double circ_radius = 1.234;
    double current_PF = 0.0;
    int trial = 0;                              // Count how many trials there are without a change in the packing fraction
    int noChangeCount = 0;                      // Counts for how many trials there is not change to the packing fraction
    const int maxNoChangeTrials = 1000000/size; // Define how many trials of no change the program should run for
    double sub_box_length = box_length / size;  // Box dimensions for each MPI task

    rng randomGenerator;                        // Instance of the random generator and add a seed dependent on the rank
    randomGenerator.seed(static_cast<unsigned int>(time(nullptr)) + rank);
    
    // Initialise vectors to hold all the cirlces
    std::vector<double> vector_Circles, vector_receivedLeftBorderCircles, vector_receivedRightBorderCircles,
                        vector_ownLeftBorderCircles, vector_ownRightBorderCircles;
    
    bool TerminateCondition = false;
    while (!TerminateCondition) {

        // Create a circle at a random location
        std::vector<double> newCircle = {sub_box_length * rank + sub_box_length * randomGenerator.grnd(), box_length * randomGenerator.grnd()};
        
        // Assume the circle is valid
        bool valid = true;

        // If the rank's box is at the edge of the entire box, don't generate a circle that overlaps with the border
        bool ignoreLeftBorder = (leftNeighbour != -1);
        bool ignoreRightBorder = (rightNeighbour != size);
        bool leftBorderCircle = false;
        bool rightBorderCircle = false;

        // Check if the circle does not overlap with any of the already existing circles
        for (size_t i = 0; i < vector_Circles.size(); i += 2) {
            if (isOverlapping(newCircle, vector_Circles[i], vector_Circles[i + 1], circ_radius)) {
                valid = false;
                break;
            }
        }

        // Check if the circle is within the bounds of the box
        if (valid) {
            if (newCircle[0] <= sub_box_length * (rank + 1) && newCircle[1] + circ_radius <= box_length
                && newCircle[0] >= sub_box_length * rank && newCircle[1] - circ_radius >= 0
                && newCircle[0] >= circ_radius && newCircle[0] <= box_length - circ_radius) {

                // Add circle to left border vectors if it is within the acceptable range
                if (newCircle[0] < sub_box_length * rank + circ_radius*2 && ignoreLeftBorder) {
                    vector_ownLeftBorderCircles.push_back(newCircle[0]);
                    vector_ownLeftBorderCircles.push_back(newCircle[1]);
                    leftBorderCircle = true;
                
                // Add circle to right border vectors if it is within the acceptable range
                } else if (newCircle[0] > sub_box_length * (rank + 1) - circ_radius*2 && ignoreRightBorder) {
                    vector_ownRightBorderCircles.push_back(newCircle[0]);
                    vector_ownRightBorderCircles.push_back(newCircle[1]);
                    rightBorderCircle = true;
                }
            } else {
                valid = false;
                noChangeCount++;
            }
        } else {
            noChangeCount++;
        }

        // If the left neighbour is not the edge send and receive border circles from them
        if (leftNeighbour >= 0) {
            sendBorderCircles(vector_ownLeftBorderCircles, leftNeighbour, sendRequestLeft);
            receiveBorderCircles(vector_receivedLeftBorderCircles, leftNeighbour, recvRequestRight);

            MPI_Wait(&sendRequestLeft, MPI_STATUS_IGNORE);
            MPI_Wait(&recvRequestRight, MPI_STATUS_IGNORE);
        }
        // If the right neighbour is not the edge send and receive border circles from them
        if (rightNeighbour < size) {
            sendBorderCircles(vector_ownRightBorderCircles, rightNeighbour, sendRequestRight);
            receiveBorderCircles(vector_receivedRightBorderCircles, rightNeighbour, recvRequestLeft);

            MPI_Wait(&sendRequestRight, MPI_STATUS_IGNORE);
            MPI_Wait(&recvRequestLeft, MPI_STATUS_IGNORE);
        }

        if(valid){
            // Check if it is overlapping with any of the received circles from the left neighbour, if so then they are not valid
            if (ignoreLeftBorder && !vector_ownLeftBorderCircles.empty() && leftBorderCircle) {
                for (size_t i = 0; i < vector_receivedLeftBorderCircles.size(); i += 2) {
                    if (isOverlapping(newCircle, vector_receivedLeftBorderCircles[i], vector_receivedLeftBorderCircles[i + 1], circ_radius)) {
                        vector_ownLeftBorderCircles.pop_back(); // Remove y-coordinate
                        vector_ownLeftBorderCircles.pop_back(); // Remove x-coordinate
                        valid = false;
                        break;
                    }
                }
            }
            // Check if it is overlapping with any of the received circles from the right neighbour, if so then they are not valid
            if (ignoreRightBorder && !vector_ownRightBorderCircles.empty() && rightBorderCircle) {
                for (size_t i = 0; i < vector_receivedRightBorderCircles.size(); i += 2) {
                    if (isOverlapping(newCircle, vector_receivedRightBorderCircles[i], vector_receivedRightBorderCircles[i + 1], circ_radius)) {
                        vector_ownRightBorderCircles.pop_back(); // Remove y-coordinate
                        vector_ownRightBorderCircles.pop_back(); // Remove x-coordinate
                        valid = false;
                        break;
                    }
                }
            }
        }
        // If the circle is still valid, add it to the main circle vector and update the packing fraction
        if(valid){
            vector_Circles.push_back(newCircle[0]);
            vector_Circles.push_back(newCircle[1]);
            current_PF = M_PI * (vector_Circles.size() / 2) * circ_radius * circ_radius / (box_length * box_length);

        }

        trial++;
        // Output the MPI rank, trial number and current packing fraction if the trial is a multiple of 1000
        if (trial % 1000 == 0) {
            std::cout << "Rank: " << rank << "\tTrial: " << trial << "\tCurrent Packing Fraction: " << current_PF << std::endl;
        }

        // If all the processes have exceeded the maxNoChangeTrials, exit the loop
        int globalNoChangeCount;
        MPI_Allreduce(&noChangeCount, &globalNoChangeCount, 1, MPI_INT, MPI_MIN, MPI_COMM_WORLD);
        TerminateCondition = (globalNoChangeCount >= maxNoChangeTrials);
    }

    MPI_Barrier(MPI_COMM_WORLD);
    // Gather all packing fractions from all processes
    double total_PF;
    MPI_Reduce(&current_PF, &total_PF, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
    // Stop the timer
    timer.stop();
    double elapsed_time = timer.elapsed_time();
    double min_time, max_time;

    // Find the maximum and minimum time taken for each process
    MPI_Reduce(&elapsed_time, &min_time, 1, MPI_DOUBLE, MPI_MIN, 0, MPI_COMM_WORLD);
    MPI_Reduce(&elapsed_time, &max_time, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);

    // Output the final packing fraction, with the minimum and maximum time elapsed
    if (rank == 0) {
        std::cout << "Final Packing Fraction: " << total_PF << std::endl;
        std::cout << "Minimum Time Elapsed: " << min_time << std::endl;
        std::cout << "Maximum Time Elapsed: " << max_time << std::endl;
    }

    // Save the circle coordinates to a file
    if (rank == 0 || rank == 1) {
        std::string filename = "coordinates" + std::to_string(rank) + ".txt";
        std::ofstream outFile(filename);
        for (size_t i = 0; i < vector_Circles.size(); i += 2) {
            outFile << vector_Circles[i] << " " << vector_Circles[i + 1] << std::endl;
        }
        outFile.close();
    }

    MPI_Finalize();

    return 0;
}

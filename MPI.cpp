#include <mpi.h>
#include <stdio.h>
#include <iostream>
#include <stdlib.h>
#include <math.h>
#include <time.h>

//Define the number of iterations and the range of x
#define n 100
#define a 0
#define b 5000

// Calculate the step size
#define dx (b-a)/n

/**
 * @brief Calculates the value of the function f(x) = 5258*x^3 + x*e^5.
 * 
 * @param x The input value for the function.
 * @return The output value of the function.
 */
double f(double x){
    return 5258*pow(x,3)+x*exp(5);
}

/**
 * Calculates the value of the i-th iteration of the function f(x) = a + dx * i.
 * @param i The iteration number.
 * @return The value of the i-th iteration of the function.
 */
double iterationLi(double i){
    return a+dx*i;
}


/**
 * @brief Calculates the value of H for a given li.
 * 
 * @param li The value of li.
 * @return The value of H.
 */
double getH(double li){
    return f(li+dx/2);
}

/**
 * Calculates the area of a rectangle with base length li and height getH(li).
 * @param li The base length of the rectangle.
 * @return The area of the rectangle.
 */
double getArea(double li){
    return getH(li)*dx;
}



/**
 * @brief Main function that initializes MPI, calculates the area under the curve using the rectangle rule, and prints the result.
 * 
 * @param argc Number of command line arguments
 * @param argv Command line arguments
 * @return int Exit status of the program
 */ 
int main(int argc, char** argv) {
  
  // Define the process name
  std::string name = "Process";

  // Define variables for rank, size, loop counter, and calculation results
  int rank, size, i;
  double start, stop, area, elapsed;
  double max_elapsed, total_area;

  // Initialize the MPI environment
  MPI_Init(NULL, NULL);

  // Get the rank of the process
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);

  // Get the number of processes
  MPI_Comm_size(MPI_COMM_WORLD, &size);
  
  // Initialize area to 0
  area = 0;

  // Calculate the start and stop indices for this process
  start = n/size*rank;
  stop = n/size*(rank+1);

  // Print the rank, size, start, and stop indices
  printf("My rank %d of %d. Start: %f. Stop: %f\n",rank,size,start,stop);

  // Synchronize all processes
  MPI_Barrier(MPI_COMM_WORLD);

  // Start the timer
  elapsed = MPI_Wtime();

  // Calculate the area for this process's indices
  for (i=start;i<stop;i++){
    area+= getArea(iterationLi(i)); // update area with the calculated area
  }

  // Stop the timer and calculate the elapsed time
  elapsed = MPI_Wtime() - elapsed;

  // Reduce all of the local elapsed times into the total elapsed time. Gets the Max time elapsed.
  MPI_Reduce(&elapsed, &max_elapsed, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);

  // Reduce all of the local areas into the total area
  MPI_Reduce(&area, &total_area, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

  // If this is the master process, print the total elapsed time and total area
  if (rank == 0) {
    printf("%s %d stores %f local time: %f\n",name.c_str(),rank, area, elapsed);

    printf("\n\nElapsed: %f\nArea: %f\n\n\n", max_elapsed,total_area);

    } else { // For all other processes
    // Send the local area and elapsed time to the master process

        MPI_Send(&area, 1, MPI_DOUBLE, 0, 1, MPI_COMM_WORLD);
        MPI_Send(&elapsed, 1, MPI_DOUBLE, 0, 1, MPI_COMM_WORLD);

        // Print the process name, rank, local area, and local elapsed time
        printf("%s %d sent %f local time: %f\n",name.c_str(),rank, area, elapsed); // Converts the string to a char array
    }

    // Finalize the MPI environment
    MPI_Finalize();
    return 0;
}
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#define N 512  // Large matrix size for longer execution time
#define ITERATIONS 100  // Adjust to ensure ~10 mins runtime

void matrix_multiply(int A[N][N], int B[N][N], int C[N][N]) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            C[i][j] = 0;
            for (int k = 0; k < N; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

int main() {
    static int A[N][N], B[N][N], C[N][N]; // Large static allocation

    // Initialize matrices with values
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            A[i][j] = i + j;
            B[i][j] = i - j;
        }
    }

    printf("Benign application started.\n");
    clock_t start = clock();

    for (int iter = 0; iter < ITERATIONS; iter++) {
        matrix_multiply(A, B, C);

        // Introduce a small delay to reduce CPU load (optional)
        usleep(50000);  // Sleep for 50 milliseconds

        // Print progress every 10 iterations
        if (iter % 10 == 0) {
            printf("Iteration %d completed.\n", iter);
        }
    }

    clock_t end = clock();
    double elapsed_time = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Benign application finished. Total runtime: %.2f seconds\n", elapsed_time);

    return 0;
}

#include "./aes_source/attack.h"
#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

#define memory_barrier asm volatile ("fence rw, rw;")
#define THRESHOLD 3000 // filter outliers, could be model-specific
#define SAMPLES 300
#define REPEAT 1 // Repeat each measurement and take average

extern u32 Td0[256];
extern u32 Td1[256];
extern u32 Td2[256];
extern u32 Td3[256];

int flush_array[256 * 1024] = {0}; // Array for cache pollution
void init_array(int *buffer);
void victim_function(aes_t pt, aes_t ct, AES_KEY aeskey, int index);
uint32_t time_collection[SAMPLES] = {0}; // Time collection for measurements

// Function to print round keys (console only)
void print_last_two_round_keys(AES_KEY aeskey) {
    const u32 *round_keys = aeskey.rd_key;
    for (int j = 0; j <= 14; j++) {
        fprintf(stdout, "Round Key %d: ", j);
        for (int i = 0; i < 4; i++) {
            fprintf(stdout, "%08x ", round_keys[j * 4 + i]);
        }
        fprintf(stdout, "\n");
    }
}

void clflush(void *addr) {
    asm volatile ("fence rw, rw;");
    volatile char *p = (volatile char *)addr;
    for (int i = 0; i < 4000; i += 8) {
        volatile char tmp = *(p + i);
        asm volatile ("" : : "r"(tmp) : "memory");
    }
    asm volatile ("fence rw, rw;");
}


// // RISC-V specific clflush (assumes a specific method to flush cache)
// static inline void clflush(void *v) {
//     asm volatile ("fence rw, rw");
//     // Implement a mechanism to ensure the cache line is evicted
//     // Use a store followed by a fence as a possible workaround
//     asm volatile ("sw zero, 0(%0)" : : "r" (v) : "memory");
//     asm volatile ("fence rw, rw");
// }

// // Cache values
// #define L1_SETS 64
// #define L1_SET_BITS 6 // log2Ceil(L1_SETS)
// #define L1_WAYS 8 // Number of ways in the cache
// #define L1_BLOCK_SZ_BYTES 64
// #define L1_BLOCK_BITS 6 // log2Ceil(L1_BLOCK_SZ_BYTES)

// // Calculate the size of the L1 cache in bytes
// #define L1_SZ_BYTES (L1_SETS * L1_WAYS * L1_BLOCK_SZ_BYTES) // Total size of L1 cache in bytes

// #define FULL_MASK 0xFFFFFFFFFFFFFFFF
// #define TAG_MASK (FULL_MASK << (L1_SET_BITS + L1_BLOCK_BITS))
// #define SET_MASK (~(TAG_MASK | ((1ULL << L1_BLOCK_BITS) - 1)))
// #define OFF_MASK ((1ULL << L1_BLOCK_BITS) - 1)

// uint8_t dummyMem[5 * L1_SETS * L1_BLOCK_SZ_BYTES];

// /**
//  * Flush the cache of the address given since RV64 does not have a
//  * clflush type of instruction. Clears any set that has the same idx bits
//  * as the address input range.
//  *
//  * Note: This does not work if you are trying to flush dummyMem out of the
//  * cache.
//  *
//  * @param addr starting address to clear the cache
//  */
// void clflush(void *addr) {
//     // Cast addr to uint64_t to get the address
//     uint64_t address = (uint64_t)addr;

//     // Find the number of cache lines to clear
//     uint64_t numSetsClear = (L1_SZ_BYTES / L1_BLOCK_SZ_BYTES); // Number of cache lines to clear

//     // Check if the address is valid
//     if (numSetsClear > L1_SETS) {
//         numSetsClear = L1_SETS; // Don't exceed the number of sets
//     }

//     // Temp variable used for nothing
//     uint8_t dummy = 0;

//     // Loop through each cache line to flush
//     for (uint64_t i = 0; i < numSetsClear; ++i) {
//         // Compute the set index
//         uint64_t setIndex = (address >> L1_BLOCK_BITS) & (L1_SETS - 1);
        
//         // Loop through each way in the set
//         for (uint64_t j = 0; j < L1_WAYS; ++j) {
//             // Evict the cache line
//             dummy = *((uint8_t *)(dummyMem + (setIndex * L1_BLOCK_SZ_BYTES) + (j * L1_BLOCK_SZ_BYTES)));
//         }
//     }
// }

// Delay loop function
void delayloop(int iterations) {
    for (volatile int i = 0; i < iterations; i++) {
        // Do nothing, just waste time
    }
}

// Read timestamp counter
uint32_t rdtscp(void) {
    uint32_t time;
    asm volatile ("rdtime %0" : "=r"(time));
    asm volatile ("fence rw, rw;");
    return time;
}
uint32_t rdcycle(void) {
    uint32_t cycles;
    asm volatile ("rdcycle %0" : "=r"(cycles));
    asm volatile ("fence rw, rw;");
    return cycles;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <test_byte>\n", argv[0]);
        return 1;
    }

    int test_byte = atoi(argv[1]);
    u32 *tb_ptr = Td0;

    if ((test_byte % 4) == 1)
        tb_ptr = Td1;
    else if ((test_byte % 4) == 2)
        tb_ptr = Td2;
    else if ((test_byte % 4) == 3)
        tb_ptr = Td3;

    srand(time(NULL));
    aes_t key, out;
    AES_KEY aeskey;
    init_array(flush_array);

    // Set Key
    toBinary("00112233445566778899aabbccddeeff", key);
    AES_set_decrypt_key(key, 128, &aeskey);

    const u32 *rk = aeskey.rd_key;
    print_last_two_round_keys(aeskey);

    // Randomly generate ciphertext
    aes_t in[SAMPLES];
    for (int i = 0; i < SAMPLES; i++) {
        randAes(in[i]);
    }
    
    // Warm-up delay
    for (int d = 0; d < 50; d++) {
        delayloop(0x800000);
    }

    // Open the output CSV file
    FILE *output_file = fopen("output.csv", "w");
    if (!output_file) {
        fprintf(stderr, "Error opening output.csv for writing\n");
        return 1;
    }

    // Write the CSV headers
    fprintf(output_file, "Measurement,Byte,ACCESS\n");

    for (int i = 0; i < SAMPLES; i++) {
        uint64_t overall_time = 0;
        for (int j = 0; j < REPEAT; j++) {
            int index = rand() % 256;
           // printf("Index Random %d \n", index); // Debug print
#if ESTDEF
            clflush(&flush_array[index << 10]);
            memory_barrier;
#endif

#if !ESTDEF
            // Preload tables into cache
            AES_decrypt(in[i], out, &aeskey);
            AES_decrypt(in[i], out, &aeskey);
            AES_decrypt(in[i], out, &aeskey);
            AES_decrypt(in[i], out, &aeskey);
            memory_barrier;
            memory_barrier;
#endif
            clflush(tb_ptr);
            memory_barrier;

            // Start measurement
            uint32_t time_start = rdcycle();
            //printf("Measurement %d, Start Time: %u\n", i, time_start); // Debug print
            victim_function(in[i], out, aeskey, index);
            memory_barrier;
            uint32_t time_end = rdcycle();
            memory_barrier;
            //printf("Measurement %d, End Time: %u\n", i, time_end); // Debug print
            // Filter outliers
            uint32_t elapsed_time = time_end - time_start;
            memory_barrier;
            //printf("Measurement %d, Elapsed: %u\n", i, elapsed_time); // Debug print
            overall_time += (elapsed_time < THRESHOLD) ? elapsed_time : THRESHOLD;
        }

        // Store the average measurement
        time_collection[i] = overall_time / REPEAT;

        // Write results to the CSV file
        fprintf(output_file, "%d,%d,%d\n", time_collection[i], (in[i][test_byte] >> 4), AES_decrypt2(in[i], out, &aeskey, 0));
    }

    // Close the output file
    fclose(output_file);
    return 0;
}

void init_array(int *buffer) {
    for (size_t k = 0; k < 256; ++k) {
        size_t x = ((k * 167) + 13) & (0xff);
        buffer[k * 1024] = x;
    }
}

void victim_function(aes_t in, aes_t out, AES_KEY aeskey, int index) {
#if ESTDEF
    volatile int next_index = flush_array[index << 10]; // Prevent optimization
#endif
    AES_decrypt(in, out, &aeskey); // Execute the victim function
}

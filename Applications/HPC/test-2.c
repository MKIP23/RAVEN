#include <stdio.h>
#include <stdint.h>


static inline uint64_t rdtsc() {
    uint64_t val;
    asm volatile ("rdcycle %0" : "=r"(val));
    return val;
}

static inline void delay_cycles(uint64_t delay) {
    uint64_t start = rdtsc();
    while (rdtsc() - start < delay);
}

static inline void read_counters(uint64_t *c3, uint64_t *c4, uint64_t *c5) {
    asm volatile ("csrr %0, hpmcounter3" : "=r"(*c3));
    delay_cycles(1000);
    asm volatile ("csrr %1, hpmcounter4" : "=r"(*c4));
    delay_cycles(1000);
    asm volatile ("csrr %2, hpmcounter5" : "=r"(*c5));
}

// static inline void read_counters(uint64_t *c3, uint64_t *c4, uint64_t *c5) {
//     asm volatile (
//         "csrr %0, hpmcounter3\n"
//         "fence\n"
//         "csrr %1, hpmcounter4\n"
//         "fence\n"
//         "csrr %2, hpmcounter5\n"
//         "fence\n"
//         : "=r"(*c3), "=r"(*c4), "=r"(*c5));
// }

int main() {
    uint64_t bm, dcm, icm;
    read_counters(&bm, &dcm, &icm);
    
    dprintf(1, "Commit.branchMispredicts: %lu\n", bm);
    dprintf(1, "l1dcaches.overallMisses.total: %lu\n", dcm);
    dprintf(1, "l1icaches.overallMisses.total: %lu\n", icm);
    
    return 0;
}


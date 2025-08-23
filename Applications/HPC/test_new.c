#include <stdio.h>
#include <stdint.h>

static inline uint64_t read_counter3() {
    uint64_t val;
    asm volatile ("csrr %0, hpmcounter3" : "=r"(val));
    return val;
}
static inline uint64_t read_counter4() {
    uint64_t val;
    asm volatile ("csrr %0, hpmcounter4" : "=r"(val));
    return val;
}

static inline uint64_t read_counter5() {
    uint64_t val;
    asm volatile ("csrr %0, hpmcounter5" : "=r"(val));
    return val;
}

int main() {
    uint64_t bm = read_counter3();
    printf("Commit.branchMispredicts: %lu\n", bm);

    uint64_t dcm = read_counter4();
    printf("l1dcaches.overallMisses.total: %lu\n", dcm);

    uint64_t icm = read_counter5();
    printf("l1icaches.overallMisses.total: %lu\n", icm);

    return 0;
}

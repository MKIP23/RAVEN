#ifndef FR_H
#define FR_H

#define likely(expr) __builtin_expect(!!(expr), 1)

/* Ensure cacheline alignment */
// #define __cacheline_aligned \
//   __attribute__((__aligned__(64), \
//                  __section__(".data..cacheline_aligned")))

#define __cacheline_aligned __attribute__((aligned(64)))

/* Read CPU cycle counter */
static inline size_t rdcycle() {
    size_t val;
    asm volatile("rdcycle %0" : "=r"(val));
    return val;
}

/* Memory access to bring data into the cache */
static inline void maccess(void *addr) {
    asm volatile("ld a7, (%0)" : : "r"(addr) : "a7", "memory");
}

/* Flush I-cache (instruction cache) */
static inline void fencei() {
    asm volatile("fence.i");
}

/* Flush D-cache (data cache), requires CMO extension */
static inline void flush(void *addr) {
    asm volatile("xor a7, a7, a7\n"
                 "add a7, a7, %0\n"
                 "cbo.flush 0(%0)\n\t"
                 : : "r"(addr) : "a7", "memory");
}

/* Probe timing for access latency (using rdcycle) */
static inline unsigned long probe_timing(char *addr) {
    unsigned long start, end;
    asm volatile (
        "rdcycle %0\n"
        : "=r"(start));
    maccess(addr);
    asm volatile (
        "rdcycle %0\n"
        : "=r"(end));
    return end - start;
}

#endif

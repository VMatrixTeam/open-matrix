#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>

int randomData;

char* getRandomString(char* dest, const char* src, int len) {
  int src_len = strlen(src);
  int i;
  for (i = 0; i < len; i++) {
    unsigned int temp;
    read(randomData, &temp, sizeof(temp));
    temp %= src_len;
    dest[i] = src[temp];
  }
  dest[len] = '\0';
  return dest;
}

unsigned int getRandomNumber(unsigned int from, unsigned int to) {
  unsigned int res;
  read(randomData, &res, sizeof(res));
  return res % (to - from + 1) + from;
}

int main(int argc, char const *argv[]) {
  randomData = open("/dev/urandom", O_RDONLY);
  char string[100000];
  const char * index = "1234567890";

  printf("%s\n",
    getRandomString(string, index, getRandomNumber(1, 100000))
  );

  close(randomData);

  return 0;
}

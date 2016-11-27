#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
  char x;
  int result = 0;

  while(scanf("%c", &x) != EOF && x != '\n') {
    result += x - '0';
  }

  printf("%d\n", result);

  return 0;
}

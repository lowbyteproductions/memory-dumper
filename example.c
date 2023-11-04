#include <stdio.h>
#include <unistd.h>
#include <malloc.h>

#define MAX_STR_LEN 256

void get_strings(char* stack_str, char* heap_str) {
  printf("[Stack String] >> ");
  fgets(stack_str, MAX_STR_LEN, stdin);

  printf("[Heap String] >> ");
  fgets(heap_str, MAX_STR_LEN, stdin);
}

void clear_screen() {
  printf("\x1b[2J\x1b[0;0H"); // ✨ ANSI magic ✨
}

void simulate_crash() {
  printf("Program has become unresponsive!\n");
  sleep(60 * 60 * 5);
}

int main() {
  char stack_str[MAX_STR_LEN];
  char* heap_str = malloc(MAX_STR_LEN);

  get_strings(stack_str, heap_str);
  clear_screen();
  simulate_crash();

  free(heap_str);

  return 0;
}

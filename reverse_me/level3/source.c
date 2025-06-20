#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void ___syscall_malloc()
{
	printf("Nope.\n");
	exit(1);
}
void ____syscall_malloc()
{
	printf("Good job.\n");
	return ;
}


int main()
{
	char const password[] = "********";
	char const format[] = "%23s";
	char input[24] = {0};
	char buffer[9];

	printf("Please enter key: ");

	if (scanf(format, input) != 1)
		___syscall_malloc();

	if (input[1] != '2' || input[0] != '4')
		___syscall_malloc();

	fflush(stdin);

	memset(buffer, 0, 9);
	buffer[0] = '*';
	int padding = 2;
	int multiplier = 1;
	char* input_ptr = input;
	char	numbers[4] = {0};
	while (strlen(buffer) < 8) {
		numbers[0] = input_ptr[padding + (multiplier * 0)];
		numbers[1] = input_ptr[padding + (multiplier * 1)];
		numbers[2] = input_ptr[padding + (multiplier * 2)];
		buffer[strlen(buffer)] = atoi(numbers);
		input_ptr += 3;
	}
	if (strcmp(buffer, password) == 0)
		____syscall_malloc();
	else
		___syscall_malloc();
}

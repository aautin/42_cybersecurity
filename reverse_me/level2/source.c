#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void ok()
{
	printf("Good job.\n");
	exit(0);
}

void no()
{
	printf("Nope.\n");
	exit(1);
}

int main()
{
	const char password[] = "delabere";
	const char format[] = "%23s";
	char input[24] = {0};

	printf("Please enter key: ");

	if (scanf(format, input) != 1)
		no();

	if (input[0] != '0' || input[1] != '0')
		no();

	char buffer[9];
	memset(buffer, 0, sizeof(buffer));
	buffer[0] = 'd';

	char* input_ptr = input + 2;
	int buf_idx = 1;

	while (buf_idx < 8) {
		if (strlen(input_ptr) >= 3) {
			char temp = input_ptr[3];
			input_ptr[3] = '\0';

			int number = atoi(input_ptr);
			buffer[buf_idx++] = number;

			input_ptr[3] = temp;
			input_ptr += 3;
		} else {
			no();
		}
	}

	buffer[8] = '\0';

	if (strcmp(buffer, password) == 0)
		ok();
	else
		no();
}

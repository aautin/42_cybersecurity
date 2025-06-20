#include <stdio.h> // printf, scanf
#include <string.h> // strcmp

int main()
{
	char input[94] = {0};
	char const password[] = "__stack_check";

	printf("Please enter key: ");

	scanf("%s", input);
	printf("%s", password);
	if (strcmp(input, password) == 0)
		printf("Good job.\n");
	else
		printf("Nope.\n");

	return 0;
}

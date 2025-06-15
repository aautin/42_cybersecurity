#include <ctype.h>
#include <fcntl.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "parsing.h"
#include "hmac.h"

void	pexit(char* msg, unsigned int code) {
	perror(msg);
	exit(code);
}

void	set_key(char* filename) {
	int	fd_in = open(filename, O_RDONLY);
	if (fd_in == -1)
		pexit(filename, 1);

	int	fd_out = open("key.hex", O_RDWR | O_CREAT | O_TRUNC, 440);
	if (fd_out == -1)
		pexit("key.hex", 1);

	char* key = get_content_from_fd(fd_in);
	if (key == NULL)
		pexit("get_content_from_fd()", 1);

	int	i;
	for (i = 0; key[i] != '\0'; ++i) {
		if (hex_char_to_val(key[i] != -1))
			continue;
		break;
	}

	if (key[i] != '\0' || i < 64) {
		char* message = "./ftotp: error: key must be 64 (or more) hexadecimal characters";
		write(2, message, strlen(message));
		exit(1);
	}


	write(fd_out, key, strlen(key));
	close(fd_in);
	close(fd_out);
}

uint32_t totp(uint8_t* key, uint64_t key_size);
uint32_t	get_totp(char* filename)
{
	int	fd = open(filename, O_RDONLY);
	if (fd == -1)
		pexit(filename, 1);

	char* key = get_content_from_fd(fd);
	if (key == NULL)
		pexit("get_content_from_fd()", 1);

	int	i;
	for (i = 0; key[i] != '\0'; ++i) {
		if (hex_char_to_val(key[i] != -1))
			continue;
		break;
	}

	if (key[i] != '\0' || i < 64) {
		char* message = "./ftotp: error: key must be 64 (or more) hexadecimal characters";
		write(2, message, strlen(message));
		exit(1);
	}

	uint8_t*	key_inbytes;
	size_t		key_inbytes_length = hex_to_bytes(key, &key_inbytes);

	uint32_t	totp_code = totp(key_inbytes, key_inbytes_length / 8);
	free(key_inbytes);

	return totp_code;
}

int main(int argc, char** argv)   
{
	if (argc != 3 || argv[1][0] != '-' || (argv[1][1] != 'k' && argv[1][1] != 'g')) {
		char* message = "Usage: ./ft_otp -k/-g FILENAME\n";
		write(2, message, strlen(message));
		return 0;
	}

	if (argv[1][1] == 'k')
		set_key(argv[2]);
	else if (argv[1][1] == 'g')
		printf("%d\n", get_totp("key.hex"));
}

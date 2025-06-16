#include <ctype.h>
#include <fcntl.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>


#include "parsing.h"
#include "hmac.h"


# define ENCRYPT(value, shift) ((value << shift) | (value >> (8 - shift)))

void	pexit(char* msg, unsigned int code)
{
	perror(msg);
	exit(code);
}
void	wexit(char* msg, unsigned int code)
{
	write(2, msg, strlen(msg));
	exit(code);
}

void encrypt(char* key) {
    const size_t SHIFT = (getuid() % 7) + 1;
    for (int i = 0; key[i] != '\0'; ++i)
        key[i] = (char)(((unsigned char)key[i] << SHIFT) | ((unsigned char)key[i] >> (8 - SHIFT)));
}

void decrypt(char* key) {
    const size_t SHIFT = (getuid() % 7) + 1;
    for (int i = 0; key[i] != '\0'; ++i)
        key[i] = (char)(((unsigned char)key[i] >> SHIFT) | ((unsigned char)key[i] << (8 - SHIFT)));
}

void	set_key(char* filename)
{
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

	if (key[i] != '\0' || i < 64)
		wexit("./ftotp: error: key must be 64 (or more) hexadecimal characters\n", 1);

	encrypt(key);

	write(fd_out, key, strlen(key));
	close(fd_in);
	close(fd_out);
}

uint32_t totp(uint8_t* key, uint64_t key_size);
uint32_t get_code(char* filename)
{
	int	fd = open(filename, O_RDONLY);
	if (fd == -1)
		pexit(filename, 1);

	char* key = get_content_from_fd(fd);
	if (key == NULL)
		pexit("get_content_from_fd()", 1);

	decrypt(key);

	if (key[0] == '\0')
		wexit("./ftotp: error: key.hex is empty\n", 1);
		
	int	i;
	for (i = 0; key[i] != '\0'; ++i) {
		if (hex_char_to_val(key[i] != -1))
			continue;
		break;
	}

	if (key[i] != '\0' || i < 64)
		wexit("./ftotp: error: key must be 64 (or more) hexadecimal characters\n", 1);

	
	uint8_t*	key_inbytes;
	size_t		key_inbytes_length = hex_to_bytes(key, &key_inbytes);

	uint32_t	totp_code = totp(key_inbytes, key_inbytes_length / 8);
	free(key_inbytes);

	return totp_code;
}

int main(int argc, char** argv)   
{
	if (argc != 3 || argv[1][0] != '-' || (argv[1][1] != 'k' && argv[1][1] != 'g'))
		wexit("Usage: ./ft_otp -k/-g FILENAME\n", 1);

	if (argv[1][1] == 'k')
		set_key(argv[2]);
	else if (argv[1][1] == 'g')
		printf("%d\n", get_code("key.hex"));
}

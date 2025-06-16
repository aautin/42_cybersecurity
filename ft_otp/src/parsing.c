#include <string.h>
#include <stdint.h>
#include <stdlib.h>

int hex_char_to_val(char c)
{
	if ('0' <= c && c <= '9') return c - '0';
	if ('a' <= c && c <= 'f') return c - 'a' + 10;
	if ('A' <= c && c <= 'F') return c - 'A' + 10;
	return -1;
}

size_t hex_to_bytes(const char *hex, uint8_t **out)
{
	size_t	char_len = strlen(hex);
	size_t	bit_len = char_len * 4;
	size_t	len = (bit_len / 8) + ((bit_len % 8) != 0);
	*out = calloc(len, sizeof(uint8_t));

	for (size_t i = 0; i < char_len; ++i) {
		int		it = hex_char_to_val(hex[i]);

		size_t	byte_pos = i / 2;
		size_t	bit_pos = ((i + 1) % 2) * 4;

		(*out)[byte_pos] |= (it << bit_pos);
	}
	return bit_len;
}

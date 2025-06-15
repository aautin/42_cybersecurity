#include <string.h>
#include <stdlib.h>

#include "hmac.h"
#include "utils.h"

#define IPAD 0x36
#define OPAD 0x5c

void hmac(char* key, void (*hash)(t_list*, uint32_t*), uint32_t* result)
{
	uint8_t*	bin;
	size_t		bit_len = hex_to_bytes(key, &bin);

	if (bit_len > 512) {
		uint32_t hash_result[5] = {0};
		sha1(bin, bit_len, hash_result);
		
		free(bin);
		bin = calloc(20, sizeof(uint8_t));

		memcpy(bin, hash_result, 20);
		bit_len = 20 * 8;
	}

	pad(&bin, (bit_len / 8) + ((bit_len % 8) != 0));
	bit_len = 64 * 8;

	uint8_t	key_ipad[64];
	uint8_t	key_opad[64];
	for (size_t i = 0; i < 64; ++i) {
		key_ipad[i] = bin[i] ^ IPAD;
		key_opad[i] = bin[i] ^ OPAD;
	}
	free(bin);

	
	print_bytes(bin, bit_len);
}

int main(int argc, char** argv)
{
	if (argc != 2)
		return 0;

	uint32_t result[5] = {0};
	hmac(argv[1], NULL, result);

	print_hmac_result(result);
	return 0;
}

#include <string.h>
#include <stdlib.h>

#include "endian.h"
#include "hmac.h"
#include "mysha1.h"
#include "utils.h"

#define IPAD 0x36
#define OPAD 0x5c

uint8_t* concatenate(
	uint8_t* left, uint8_t* right,
	size_t size_l, size_t size_r,
	uint64_t* size_result)
{
	*size_result = size_l + size_r;
	uint8_t* result = malloc(*size_result);
	if (!result) {
		*size_result = 0;
		return NULL;
	}

	memcpy(result, left, size_l);
	memcpy(result + size_l, right, size_r);

	return result;
}

void hmac(uint8_t* key, uint64_t key_size,
		  uint8_t* C, uint64_t C_size,
		  bool (*hash)(uint8_t*, uint64_t, uint32_t*), uint32_t* result)
{
	
	uint8_t key_buffer[64] = {0};
	if (key_size > 64) {
		uint32_t hash_result[5] = {0};
		hash(key, key_size * 8, hash_result);
		for (int i = 0; i < 5; ++i)
			hash_result[i] = endian32(hash_result[i]);

		memcpy(key_buffer, hash_result, 20);
		key_size = 20;
	}
	else
		memcpy(key_buffer, key, key_size);

	uint8_t	key_ipad[64];
	uint8_t	key_opad[64];
	for (size_t i = 0; i < 64; ++i) {
		key_ipad[i] = key_buffer[i] ^ IPAD;
		key_opad[i] = key_buffer[i] ^ OPAD;
	}

	uint8_t* it;
	uint32_t result_temp[5];
	uint64_t content_len;

	it = concatenate(key_ipad, C, 64, C_size, &content_len);
	content_len *= 8;

	hash(it, content_len, result_temp);
	free(it);

	for (int i = 0; i < 5; ++i)
		result_temp[i] = endian32(result_temp[i]);

	it = concatenate(key_opad, (uint8_t*) result_temp, 64, 20, &content_len);
	content_len *= 8;

	hash(it, content_len, result);
	free(it);
}

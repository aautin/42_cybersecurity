#include <stdint.h>
#include <stdio.h>

#include "endian.h"

#include "hmac.h"

uint32_t dynamic_truncate(uint32_t hmac_result[5]) {
    uint8_t hash[20];
	for (int i = 0; i < 5; ++i) {
		hash[i*4 + 0] = (hmac_result[i] >> 24) & 0xFF,
		hash[i*4 + 1] = (hmac_result[i] >> 16) & 0xFF,
		hash[i*4 + 2] = (hmac_result[i] >> 8) & 0xFF,
		hash[i*4 + 3] = hmac_result[i] & 0xFF;
	}

	int offset = hash[19] & 0x0f;
	uint32_t bin_code = ((hash[offset] & 0x7f) << 24) |
						(hash[offset + 1] << 16) |
						(hash[offset + 2] << 8) |
						(hash[offset + 3]);
    return bin_code;
}

uint32_t	totp(uint8_t* key, uint64_t key_size)
{
	uint64_t	counter = endian64(get_time_counter());
	uint8_t*	counter_ptr = (uint8_t*) &counter;
	
	uint32_t	result[5];
	hmac(key, key_size, counter_ptr, 8, sha1, result);
	
	uint32_t code = dynamic_truncate(result);
    return code % 1000000;
}

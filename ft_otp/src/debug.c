#include <stdint.h>
#include <stdio.h>

void print_bytes(uint8_t *key_bin, size_t bit_len)
{
	printf("key_bin[%zu]: ", bit_len);
	for (size_t i = 0; i < bit_len / 8; ++i) {
		printf("%02x ", key_bin[i]);
	}
	printf("\n");
}

void print_hmac_result(uint32_t *result)
{
	// Assuming result is an array of 5 uint32_t values
	// This function prints the HMAC result in a readable format
	printf("HMAC result[160]: ");
	for (int i = 0; i < 5; ++i) {
		printf("%08x ", result[i]);
	}
	printf("\n");
}

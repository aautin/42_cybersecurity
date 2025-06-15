#ifndef HMAC_H
# define HMAC_H

#include "list.h"
#include "mysha1.h"

uint8_t* concatenate(uint8_t* left, uint8_t* right,
					 size_t size_l, size_t size_r,
					 uint64_t* size_result);

void	hmac(uint8_t* key, uint64_t key_size,
			 uint8_t* C, uint64_t C_size,
			 bool (*hash)(uint8_t*, uint64_t, uint32_t*), uint32_t* result);

#endif

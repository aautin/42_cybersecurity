#ifndef HMAC_H
# define HMAC_H

#include "list.h"
#include "sha1.h"

void	hmac(char* key, void (*hash)(t_list*, uint32_t*), uint32_t* result);

#endif

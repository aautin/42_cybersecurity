#ifndef UTILS_H
# define UTILS_H

# include <stdint.h>

// parsing
int		hex_char_to_val(char c);
size_t	hex_to_bytes(const char *hex, uint8_t **out);
void	pad(uint8_t **src, size_t byte_len);

// debug
void	print_bytes(uint8_t *key_bin, size_t bit_len);
void	print_hmac_result(uint32_t *result);

#endif

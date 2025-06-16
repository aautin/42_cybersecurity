#include <time.h>
#include <stdint.h>

uint64_t get_time_counter() {
	time_t now = time(NULL);
	return now / 30;
}

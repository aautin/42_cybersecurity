#ifndef SPOOFER_H
# define SPOOFER_H

# include "utils.h"

typedef struct s_spoofer {
	state*	state;
	pcap_t*	pcap;
}	spoofer_t;

void*	spoof(void* arg);

#endif
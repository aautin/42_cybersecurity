#ifndef UTILS_H
# define UTILS_H

# include <stdbool.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <pthread.h>
# include <pcap.h>

typedef enum e_request_type {
	SRC_TO_TARGET,
	TARGET_TO_SRC,
	OTHER
}	request_type;

typedef enum e_poison {
	KEEP_GOING,
	DO_NOTHING,
	STOP
}	poison_t;

typedef struct s_state{
	unsigned char	inquisitor_mac[6];

	unsigned char	source_ip[4];
	unsigned char	source_mac[6];

	unsigned char	target_ip[4];
	unsigned char	target_mac[6];

	int		count;
	int		is_source_poisoned;
	int		is_target_poisoned;
}	state;

char*		find_inquisitor_mac(char** envp);
char**		split(const char* str, char delimiter);
int			set_user(state** user, char** addresses, char* inquisitor_mac);
int			set_pcap(pcap_t** pcap, const char* name);

#endif
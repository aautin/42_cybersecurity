#ifndef MYSIGNAL_H
# define MYSIGNAL_H

# include <signal.h>
# include "utils.h"

void		sig_handler(int signum);
void		set_signal();
poison_t	get_status();
void		set_status(poison_t new_status);

#endif
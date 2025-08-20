#include "mysignal.h"

pthread_mutex_t	mutex;
poison_t		status;

void sig_handler(int signum)
{
	if (signum == SIGINT) {
		printf("Caught SIGINT\n");
		pthread_mutex_lock(&mutex);
		status = STOP;
		pthread_mutex_unlock(&mutex);
	}
}

void set_signal()
{
	pthread_mutex_init(&mutex, NULL);
	status = KEEP_GOING;

	struct sigaction sa;
	sa.sa_handler = sig_handler;
	sa.sa_flags = 0;
	sigemptyset(&sa.sa_mask);
	sigaction(SIGINT, &sa, NULL);
}

poison_t get_status()
{
	pthread_mutex_lock(&mutex);
	poison_t current_status = status;
	pthread_mutex_unlock(&mutex);

	return current_status;
}

void set_status(poison_t new_status)
{
	pthread_mutex_lock(&mutex);
	status = new_status;
	pthread_mutex_unlock(&mutex);
}

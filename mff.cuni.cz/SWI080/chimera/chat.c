/*
 * Chimera Chat
 *
 * Original Authors:
 *  Rama Alebouyeh (rama@cs.ucsb.edu)
 *  Matthew Allen (msa@cs.ucsb.edu)
 *
 * Modified for Middleware Course:
 *  Vlastimil Babka (babka@dsrg.mff.cuni.cz)
 *  Martin Decky (decky@dsrg.mff.cuni.cz)
 *
 */

#include <stdio.h>
#include <unistd.h>

#ifdef __cplusplus
extern "C" {
#endif

#include "chimera.h"

#ifdef __cplusplus
}
#endif

#define BUF_MAX 256

extern char *optarg;
extern int optind;


/* First user-defined message available */
#define CHIMERA_USER_MSG 11

/* Message type number for private (client->client) messages */
#define MSG_CHAT (CHIMERA_USER_MSG + 10)

#define MSG_JOIN (CHIMERA_USER_MSG + 14)
#define MSG_CHANNEL (CHIMERA_USER_MSG + 15)
#define MSG_LEAVE (CHIMERA_USER_MSG + 16)

static ChimeraState *state;  /* Chimera state */
static Key my_key;           /* Hash key of this client */
static char *client_name;    /* Name of this client */

#include "channels.cpp"

/* Upcall for message forward event
 *
 * Used here just to print debugging info.
 *
 */
static void upcall_forward(Key **kp, Message **mp, ChimeraHost **hp)
{
	/* Upcall can change the values, hence double pointers */
	Key *k = *kp;
	Message *m = *mp;
	ChimeraHost *h = *hp;

	fprintf(stderr, "** Routing message type %d (%s) to %s via %s:%d **\n",
		m->type, m->payload, get_key_string(k), h->name, h->port);
}


/* Upcall for host membership change notification
 *
 * Used here just to print debugging info.
 *
 */
static void upcall_update(Key *k, ChimeraHost *h, int joined)
{
	fprintf(stderr, "Node %s (%s:%d) %s neighbor set\n", get_key_string(k),
		h->name, h->port, joined ? "joined" : "leaving");
}


/* Upcall for message deliver event
 *
 */
static void upcall_deliver(Key *k, Message *m)
{
	/* Determine the message type */
	if (m->type == MSG_CHAT) {
		/* Ignore messages for other clients, delivered here because such
		 * a client is not in the network */
		printf("** received MSG %s for %s **\n", m->payload, get_key_string(k));
		if (strcmp(get_key_string(k), get_key_string(&my_key)) == 0) {
		 	/* Print the chat message */
			printf(">>>>> %s <<<<<\n", m->payload);
		}
	} else if (m->type == MSG_CHANNEL) {
		printf("** received CHANNEL-MSG %s **\n", m->payload);
		on_channel_message(k, m);
	} else if (m->type == MSG_JOIN) {
		printf("** received JOIN %s **\n", m->payload);
		on_channel_join(k, m);
	} else if (m->type == MSG_LEAVE) {
		printf("** received LEAVE %s **\n", m->payload);
		on_channel_leave(k, m);

	} else if (m->type >= CHIMERA_USER_MSG) {
		/* Message types below 10 are reserved
		 * for internal Chimera messages */
		 fprintf (stderr, "** Unknown message of type %d and size %d payload %s **\n",
		 	m->type, m->size, m->payload);
	}
}


/* Send private chat message
 *
 * Send chat message to a peer with given @peer_name
 *
 */
static void msg_chat(char *peer_name, char *message)
{
	/* Hash the peer_name to obtain peer's key */
	Key peer_key;
	key_makehash(state->log, &peer_key, peer_name);

	/* Construct the chat message to contain
	 * also this client's name */
	char buf[BUF_MAX];
	int len = snprintf(buf, BUF_MAX, "%s: %s", client_name, message);

	fprintf (stderr, "** msg_chat %s <- %s **\n",
		 	peer_name, message);
	chimera_send(state, peer_key, MSG_CHAT, len + 1, buf);
}


static void usage(char *prname)
{
	fprintf(stderr, "Usage: %s [-j bootstrap:port] port name\n", prname);
}


int main (int argc, char *argv[])
{
	int opt;
	char *hn = NULL;
	int port, joinport;
	ChimeraHost *host = NULL;
	int i, j;

	/* Command line parsing */
	while ((opt = getopt(argc, argv, "j:")) != EOF) {
		switch ((char) opt) {
			case 'j':
				for (i = 0; (optarg[i] != ':') && (i < strlen(optarg)); i++);
				optarg[i] = 0;
				hn = optarg;
				sscanf(optarg + (i + 1), "%d", &joinport);
				break;
			default:
				fprintf(stderr, "Invalid option %c\n", (char) opt);
				usage(argv[0]);
				return 1;
		}
	}

	if ((argc - optind) != 2) {
		usage(argv[0]);
		return 1;
	}
	port = atoi(argv[optind]);
	client_name = argv[optind + 1];

	/* Initalize Chimera on given port */
	state = chimera_init(port);
	if (state == NULL) {
		fprintf(stderr, "Unable to initialize Chimera\n");
		return 1;
	}

	/* Create reference to bootstrap host */
	if (hn != NULL)
		host = host_get(state, hn, joinport);

	/* Override default hash key (created from host and port)
	 * with key created by hashing client's name */
	key_makehash(state->log, &my_key, client_name);
	chimera_setkey(state, my_key);

	/* Register upcall functions */
	chimera_forward(state, upcall_forward);
	chimera_deliver(state, upcall_deliver);
	chimera_update(state, upcall_update);

	/* Register the MSG_CHAT type
	 * with acknowledged delivery */
	chimera_register(state, MSG_CHAT, 1);
	chimera_register(state, MSG_CHANNEL, 1);
	chimera_register(state, MSG_JOIN, 1);
	chimera_register(state, MSG_LEAVE, 1);

	/* Logging to stderr */
	log_direct(state->log, LOG_WARN, stderr);
	log_direct(state->log, LOG_ROUTING, stderr);

	/* Join chimera network, possibly with bootstrap host */
	chimera_join(state, host);

	printf("** Welcome to Chimera Chat                                   **\n");
	printf("** Available commands:                                       **\n");
	printf("**  msg <peer> <message>      - send private message to peer **\n");
	printf("**  join <#channel>           - join a channel               **\n");
	printf("**  send <#channel> <message> - send message to channel      **\n");
	printf("**  leave <#channel>          - leave a channel              **\n");
	printf("** Hi, %s **\n", client_name);

	/* Main client loop */
	char tmp[BUF_MAX];
	while (fgets(tmp, BUF_MAX, stdin) != NULL) {
		char *cmd;      /* Chat command */
		char *name;     /* Peer of channel name */
		char *message;  /* Message to send */

		if (strlen(tmp) > 2) {
			/* Crude command parsing into the three parts */
			int last;
			for (i = 0; (tmp[i] != '\n') && (i < BUF_MAX); i++);
			tmp[i] = 0;
			last = i;
			cmd = tmp;

			for (i = 0; (tmp[i] != ' ') && (i < last); i++);
			tmp[i++] = 0;
			name = tmp + i;

			for (; (tmp[i] != ' ') && (i < last); i++);
			tmp[i++] = 0;
			message = tmp + i;
			i++;

			if (strcmp(cmd, "msg") == 0) { /* Send private message */
				fprintf(stderr, "Sending private message to %s: %s\n",
					name, message);
				msg_chat(name, message);
			} else if (strcmp(cmd, "join") == 0) { /* Join a channel */
				fprintf(stderr, "Joining channel %s\n", name);
				channel_join(name);
			} else if (strcmp(cmd, "send") == 0) { /* Send message to channel */
				fprintf(stderr, "Sending message to channel %s: %s\n",
					name, message);
				channel_send(name, message);
			} if (strcmp(cmd, "leave") == 0) { /* Leave a channel */
				fprintf(stderr, "Leaving channel %s\n", name);
				channel_leave(name);
			}
		}
	}

	return 0;
}

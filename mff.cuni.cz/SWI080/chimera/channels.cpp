
#include <map>
#include <set>
#include <vector>
#include <string>

using namespace std;

typedef set <string> UserList;

typedef map <string, UserList *> Channels;

static Channels channels;

static void msg_chat(char *peer_name, char *message);


/* Send private chat message
 *
 * Send chat message to a peer with given @peer_name
 *
 */
static void channel_chat(char *peer_name, char *message)
{
	/* Hash the peer_name to obtain peer's key */
	Key peer_key;
	key_makehash(state->log, &peer_key, peer_name);

	char buf[BUF_MAX];
	int len = snprintf(buf, BUF_MAX, "%s", message);

	fprintf (stderr, "** msg_chat %s <- %s **\n",
		 	peer_name, message);
	chimera_send(state, peer_key, MSG_CHAT, len + 1, buf);
}

/* Send channel message
 *
 * Send chat message to a channel
 *
 */
void channel_send(char *channel, char *message)
{
	/* Hash */
	Key peer_key;
	key_makehash(state->log, &peer_key, channel);

	/* Construct the chat message to contain
	 * also this client's name */
	char buf[BUF_MAX];
	int len = snprintf(buf, BUF_MAX, "%s (%s): %s", client_name, channel, message);
	chimera_send(state, peer_key, MSG_CHANNEL, len + 1, buf);
}

/* Send channel message
 *
 * Send enter/leave message
 *
 */
void channel_join(char *channel)
{
	/* Hash */
	Key peer_key;
	key_makehash(state->log, &peer_key, channel);

	/* Construct the chat message to contain
	 * also this client's name */
	char buf[BUF_MAX];
	int len = snprintf(buf, BUF_MAX, "%s", client_name);
	chimera_send(state, peer_key, MSG_JOIN, len + 1, buf);
}

void channel_leave(char *channel)
{
	/* Hash */
	Key peer_key;
	key_makehash(state->log, &peer_key, channel);

	/* Construct the chat message to contain
	* also this client's name */
	char buf[BUF_MAX];
	int len = snprintf(buf, BUF_MAX, "%s", client_name);
	chimera_send(state, peer_key, MSG_LEAVE, len + 1, buf);
}

static UserList *getChannel(Key *channel)
{
	UserList *ul;

	string ch = string(get_key_string(channel));

	Channels::iterator iter = channels.find(ch);
	if ( iter == channels.end() ) {
		fprintf(stderr, "** Unknown channel %s **\n",
			get_key_string(channel) );

		ul = new UserList();
		channels.insert(pair<string, UserList *>(ch, ul));
	}
	else {
		ul = iter->second;
	}
	return ul;
}

/**
 *  received message for channel
 */
void on_channel_message(Key *channel, Message *m)
{
	UserList *ul = getChannel(channel);

	for (UserList::const_iterator ulit = ul->begin(); ulit != ul->end(); ++ulit) {


		string username = *ulit;
		char buffer[username.length()+1];
		strcpy(buffer, username.c_str());
	
		printf("** resending %s to %s, channel %s**\n", 
			m->payload, buffer, get_key_string(channel));
		channel_chat(buffer, m->payload);
	}

}

/**
 *  received message for JOIN
 */
void on_channel_join(Key *k, Message *m)
{
	UserList *ul = getChannel(k);

	printf("** adding %s to %s**\n", m->payload, get_key_string(k));

	string *b = new string(m->payload);
	ul->insert(*b);

}


/**
 *  received message for LEAVE
 */
void on_channel_leave(Key *k, Message *m)
{
	UserList *ul = getChannel(k);

	string *username = new string(m->payload);
	UserList::iterator useriter = ul->find(*username);

	fprintf(stderr, "** Removing from %s user %s **\n",
		get_key_string(k), m->payload );

	if (useriter == ul->end()) {
		fprintf(stderr, "** Not found %s in %s **\n",
			 m->payload, get_key_string(k));
		return;
	}
	
	ul->erase(useriter);

}

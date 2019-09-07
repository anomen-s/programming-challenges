#! /bin/sh

echo -e "GET /announce?info_hash=jb%F2%8F%1C%AC%1F%85%E4%E6%0B%C6%E1%0C%BEq%96%F8%F9%3B&numwant=4&peer_id=testxxxxxxxxxxx$1 HTTP/1.1\r\nUser-Agent: shell" | nc -v localhost 6969


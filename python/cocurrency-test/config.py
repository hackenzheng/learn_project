EOL1 = b'\n\n'
EOL2 = b'\n\r\n'

response = b'HTTP/1.0 200 ok\r\nDate:Mon,1 Jan 1996 01:01:01 GMT\r\n'
response += b'Content-Type:text/plain\r\nContent-Length: 13\r\n\r\n'
response += b'Hello, wrold!'

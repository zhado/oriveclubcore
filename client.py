import socket
import sys
import threading

rendezvous = ('35.192.103.193', 55555)

# connect to rendezvous
print('connecting to rendezvous server')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 50001))
sock.sendto(b'0', rendezvous)


while True:
    data = sock.recv(1024).decode()

    if data.strip() == 'ready':
        print('checked in with server, waiting')
        break

data = sock.recv(1024).decode()
peer_ip, peer_sport, peer_dport = data.split(' ')
peer_sport = int(peer_sport)
peer_dport = int(peer_dport)

sock.sendto(b'0',(peer_ip, peer_sport))

print('\ngot peer')
print('  ip:          {}'.format(peer_ip))
print('  source port: {}'.format(peer_sport))
print('  dest port:   {}\n'.format(peer_dport))

def listen():
    while True:
        data = sock.recv(1024)
        print('\rpeer: {}\n> '.format(data.decode()), end='')

listener = threading.Thread(target=listen, daemon=True);
listener.start()

while True:
    msg = input('> ')
    sock.sendto(msg.encode(), (peer_ip,peer_sport))

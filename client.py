#!/bin/python3

import socket
import time
import sys
import threading
import argparse

def get_info_from_server(serv_ip):
    rendezvous = (serv_ip, 55555)

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

    while True:
        data = sock.recv(1024).decode()
        if (data!='0' and data.split(' ')[0]!="peer"):
            peer_ip, peer_sport, peer_dport = data.split(' ')
            peer_sport = int(peer_sport)
            peer_dport = int(peer_dport)
            break
    return sock,peer_ip,peer_sport,peer_dport

def setup_local():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', 50001))
        print("starting as second client. sending to 50002")
        return sock, '127.0.0.1', 50002, 50001
    except OSError:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', 50002))
        print("starting as first client. sending to 50001")
        return sock, '127.0.0.1', 50001, 50002

def main():
    start_time=0

    parser = argparse.ArgumentParser(description='oriveclubcore yay')
    parser.add_argument('--dest_ip')
    parser.add_argument('--dest_port')
    parser.add_argument('--serv_ip')
    parser.add_argument('--local', action='store_true', help='bind to localhost. overrides dest arguments')
    parser.add_argument('--send_mpv', action='store_true', help='send mpv time to peer')
    args = parser.parse_args()

    if(not(args.local)):
        sock, peer_ip, peer_sport, peer_dport=get_info_from_server(args.serv_ip)
    else:
        sock, peer_ip, peer_sport, peer_dport=setup_local()

    if(args.send_mpv):
        # mpv listening bind
        sock_mpv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_mpv.bind(('0.0.0.0', 5000))

        def listen_mpv():
            while True:
                data = sock_mpv.recv(1024)
                sock.sendto(("mpv time: " + data.decode()).encode(), (peer_ip,peer_sport))
                # print("mpv time:" + data.decode())

        listener_mpv = threading.Thread(target=listen_mpv, daemon=True)
        listener_mpv.start()

    sock.sendto(b'0',(peer_ip, peer_sport))

    print('\ngot peer')
    print('  ip:          {}'.format(peer_ip))
    print('  source port: {}'.format(peer_sport))
    print('  dest port:   {}\n'.format(peer_dport))

    def listen():
        while True:
            data = sock.recv(1024)
            if(data=="\\ping".encode()):
                print("got ping")
                sock.sendto("\\pong".encode(), (peer_ip,peer_sport))
            if(data=="\\pong".encode()):
                delta_time=time.perf_counter()-start_time
                time_msg="responce time: " + str(delta_time)
                print(time_msg)
                sock.sendto(time_msg.encode(), (peer_ip,peer_sport))


            print('\rpeer: {}\n> '.format(data.decode()), end='')

    listener = threading.Thread(target=listen, daemon=True)
    listener.start()

    while True:
        try: 
            msg = input('> ')
            if(msg == "\\ping"):
                start_time=time.perf_counter()
            sock.sendto(msg.encode(), (peer_ip,peer_sport))
        except (KeyboardInterrupt, EOFError):
            sock.sendto("peer disconnected".encode(), (peer_ip,peer_sport))
            sys.exit(0)

if __name__ == "__main__":
    main()

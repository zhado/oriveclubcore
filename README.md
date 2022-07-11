# Oriveclubcore
Proof of concept implementation of p2p udp client(s)/rendezvous-server in python.
Also comes with a script to read Mpv time and send it to client python program. 
Can be used to sync movie times with frens : )

Initially based on [this](https://github.com/engineer-man/youtube/tree/master/141). But client code has been completely 
rewritten.

# Usage

For this project to work a rendezvous server with public ip and forwarded port 55555 is required.

This information is given to client program by:

```console
client.py --serv_ip=x.x.x.x
```

It is also possible to use clients locally for testing: 
```console
client.py --local
```
## Mpv
place lua script in ~/.config/mpv/scripts. Or just symlink it from project folder:

```console
ln -s ./output_time_udp.lua ~/.config/mpv/scripts/
```

Script will send time-pos of mpv to local udp port 5000 every second.

Currently this behaviour is not toggleable.

To forward mpv time to peer start client.py with:

```console
client.py --serv_ip=x.x.x.x --send_mpv
```

# NAT
Should work with full-cone and restricted-cone NATs.

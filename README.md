# Hetzner-Proxmox

post-up echo 1 > /proc/sys/net/ipv4/ip_forward

post-up iptables -t nat -A PREROUTING -p tcp -d 95.216.13.119 --dport 9000 -i enp193s0f0np0 -j DNAT --to-destination 10.10.0.100:9000
post-down iptables -t nat -D PREROUTING -p tcp -d 95.216.13.119 --dport 9000 -i enp193s0f0np0 -j DNAT --to-destination 10.10.0.100:9000
post-up iptables -t nat -A PREROUTING -p tcp -d 95.216.13.119 --dport 63389 -i enp193s0f0np0 -j DNAT --to-destination 10.10.0.101:63389 
post-down iptables -t nat -D PREROUTING -p tcp -d 95.216.13.119 --dport 63389 -i enp193s0f0np0 -j DNAT --to-destination 10.10.0.101:63389 

PART  /boot/efi esp 256M
PART  /boot  ext4  1024M
PART  /tmp xfs    10G
PART  /     ext4  100G
PART swap  swap 16G

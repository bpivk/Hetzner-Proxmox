# Hetzner-Proxmox

Running the community Proxmox VE Post Install script
From the web UI select your host on the left and click "Shell" at the top right.

From the shell window run the following command

bash -c "$(wget -qLO - https://github.com/tteck/Proxmox/raw/main/misc/post-pve-install.sh)"
This is the Post Install script made by tteck

It is used to tweak proxmox including removing the subscription nag, configuring community repo's etc.

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


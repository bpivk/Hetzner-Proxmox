# Hetzner-Proxmox

#### Partition proxmox
PART  /boot/efi esp 256M
PART  /boot  ext4  1024M
PART  /tmp xfs    10G
PART  /     ext4  100G
PART swap  swap 16G

Ostane prazen prostor ki ga kasneje uporabiš za particijo ki ostane.
> fpart -l
fpart /dev/xxxxx

------------
#### Running the community Proxmox VE Post Install scriptRunning the community Proxmox VE Post Install script
> bash -c "$(wget -qLO - https://github.com/tteck/Proxmox/raw/main/misc/post-pve-install.sh)"

------------

#### Preparing for SDN functionality
> apt update
apt -y install dnsmasq
apt install libpve-network-perl
apt install frr-pythontools
systemctl disable --now dnsmasq

Now we need to make sure our /etc/network/interfaces file contains the following line at the bottom:
> nano /etc/network/interfaces
![](https://github.com/bpivk/Hetzner-Proxmox/blob/main/Screens/image-17.png?raw=true)source /etc/network/interfaces.d/*

------------
#### Creating the SDN (Virtual Network)
![](https://github.com/bpivk/Hetzner-Proxmox/blob/main/Screens/image-18-1024x627.png?raw=true)
![](https://github.com/bpivk/Hetzner-Proxmox/blob/main/Screens/image-19-1024x503.png?raw=true)
![](https://github.com/bpivk/Hetzner-Proxmox/blob/main/Screens/image-20-1024x566.png?raw=true)
![](https://github.com/bpivk/Hetzner-Proxmox/blob/main/Screens/image-21-1024x505.png?raw=true)
![](https://github.com/bpivk/Hetzner-Proxmox/blob/main/Screens/image-22-1024x433.png?raw=true)
![](https://github.com/bpivk/Hetzner-Proxmox/blob/main/Screens/image-23-1024x491.png?raw=true)

------------
#### Firewall
![](https://github.com/bpivk/Hetzner-Proxmox/blob/main/Screens/image-26.png?raw=true)
![](https://github.com/bpivk/Hetzner-Proxmox/blob/main/Screens/image-27.png?raw=true)
![](https://github.com/bpivk/Hetzner-Proxmox/blob/main/Screens/image-29.png?raw=true)
![](https://github.com/bpivk/Hetzner-Proxmox/blob/main/Screens/image-33.png?raw=true)
![](https://github.com/bpivk/Hetzner-Proxmox/blob/main/Screens/image-34.png?raw=true)

------------
#### Internet access
> nano /etc/network/interfaces.d/sdn

Paste:
> post-up echo 1 > /proc/sys/net/ipv4/ip_forward

------------

#### Port forward
> post-up iptables -t nat -A PREROUTING -p tcp -d [ext_ip] --dport [port] -i [network_card] -j DNAT --to-destination [internal_ip:port]
post-down iptables -t nat -D PREROUTING -p tcp -d [ext_ip] --dport [port] -i [network_card] -j DNAT --to-destination [internal_ip:port]

Example:
> post-up echo 1 > /proc/sys/net/ipv4/ip_forward
post-up iptables -t nat -A PREROUTING -p tcp -d 95.216.13.119 --dport 9000 -i enp193s0f0np0 -j DNAT --to-destination 10.10.0.100:9000
post-down iptables -t nat -D PREROUTING -p tcp -d 95.216.13.119 --dport 9000 -i enp193s0f0np0 -j DNAT --to-destination 10.10.0.100:9000


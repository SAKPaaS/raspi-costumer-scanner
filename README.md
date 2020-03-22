## Background

### Setup headless Raspberry Pi

#### Requirements
* Raspberry Pi 3, Model B
* SD Card with (at least 4GB to hold the rasbian img)
* a laptop with internet access

#### Steps

1. Download rasbian [here](https://www.raspberrypi.org/downloads/raspbian/)
2. Flash rasbian to SD card [here](https://www.raspberrypi.org/documentation/installation/installing-images/)
3. Prepare automatic connection to WIFI and enable SSH [here](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md)
4. Insert SD in Raspberry and connect power supply. There is a red LED, which should turn on. If this red LED blinks
, there might be problems with the power supply or the kernel image. 
5. Ssh into raspberry ``` ssh pi@<IP>```  Find the IP address via getting the own
  IP `hostname -I`, then pinging all available devices `nmap -sn 192.168.0.1/24`, then run `sudo arp -a`and look for
   entries starting with `b8:27:eb:...` (The automatic WIFI connection did not work for
 me, but connecting to the router via LAN allowed to connect to the raspbi).
 



### Monitoring of wifi capable devices
  
#### Switching wlan interface to monitoring mode

In order to monitor all wifi capable devices, the wlan interface of the monitoring device has to be put into a
designated monitoring mode.

##### Worked on my laptop

Installation of airmon-ng via 
 ```
sudo apt-get install aircrack-ng
 ```
Check available interfaces
```bash
sudo ifconfig -a
eth0: ...

lo: ...

wlan0: ...
```
Here wlan0 is the wlan interface.

Check mode of the interface via 
```bash
sudo iwconfig
wlan0     IEEE 802.11  ESSID:"..."  
          Mode:Managed  Frequency:2.437 GHz  Access Point: ...
```
Now switch the mode to monitor via (attention: no access to wifi anymore)
```bash
sudo airmon-ng start wlan0
PHY	Interface	Driver		Chipset

phy0	wlan0		iwlwifi		Intel Corporation Wireless 8260 (rev 3a)

		(mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
		(mac80211 station mode vif disabled for [phy0]wlan0)

```

The monitoring interface `wlan0mon`. Verify via
```bash
sudo iwconfig
lo        no wireless extensions.

eth0      no wireless extensions.

wwp0s20f0u2i12  no wireless extensions.

wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=0 dBm   
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:on
```

To stop the monitoring, run (might take a moment until wifi works again)
```bash
sudo airmon-ng stop wlan0mon
```

##### Edits for Raspberry Pi

The in-build wireless cannot be switched to monitor mode with the canonical driver. But an alternative driver is
 [Nexmon](https://pimylifeup.com/raspberry-pi-nexmon/). 

##### Ressources
 * [aircrack newbie guide](https://www.aircrack-ng.org/doku.php?id=newbie_guide)
 * [aircrack tut](https://www.aircrack-ng.org/doku.php?id=cracking_wpa&s[]=passive&s[]=mode) -> Step 1 - Start the wireless interface in monitor mode
 * [wireshark tut with detailed instructions to switch to monitor mode](https://wiki.wireshark.org/CaptureSetup/WLAN#Monitor_mode)
 * [a python-based monitoring setup on a raspberry](https://www.jbrandsma.com/news/2018/01/02/catching-wifi-probes-using-a-raspberry-pi/)   
 
 
#### Monitoring of packets 

With the monitoring device, we can now check the packets send from other devices. Basically, we can read the contents
 of this package to determine whether this is a client request e.g. a mobile phone and retrieve its MAC address, a
  unique id. With this info, we can determine the amount of active wifi devices. 
  
##### Install [scapy](https://scapy.readthedocs.io/en/latest/introduction.html)

Here with conda
  ```bash
conda create -n raspi-sniff python=3. 
conda activate raspi-sniff
conda install -c conda-forge scapy
```

##### Detect client packages

In the communication protocol between clients and access points (WIFI networks), packets can be either management
, control or data frames. The management type packets are used by clients to look for access points, associate to and
 disassociate from them. At the same time, the management type is used by the access points to reply to searching
  clients. Via scapy, this information can be obtained by checking the packet type (which frame
  ) and the subtype (which action, client or AP). 
  
* [packet frames](https://wifibond.com/2017/07/20/understanding-of-802-11-management-frames/)
* [management frame](https://documentation.meraki.com/MR/WiFi_Basics_and_Best_Practices/802.11_Association_Process_Explained)
* [packet structure scapy](https://scapy.readthedocs.io/en/latest/api/scapy.layers.dot11.html)
* [a short script to detect clients and save them in a list](https://www.sans.org/blog/special-request-wireless-client-sniffing-with-scapy/)

## Background

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


#### Ressources
 * [aircrack newbie guide](https://www.aircrack-ng.org/doku.php?id=newbie_guide)
 * [aircrack tut](https://www.aircrack-ng.org/doku.php?id=cracking_wpa&s[]=passive&s[]=mode) -> Step 1 - Start the wireless interface in monitor mode
 * [wireshark tut with detailed instructions to switch to monitor mode](https://wiki.wireshark.org/CaptureSetup/WLAN#Monitor_mode)
 * [a python-based monitoring setup on a raspberry](https://www.jbrandsma.com/news/2018/01/02/catching-wifi-probes-using-a-raspberry-pi/)   
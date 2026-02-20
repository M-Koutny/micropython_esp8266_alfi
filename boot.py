#boot.py
import network
import utime
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect("Wifi_Name","Wifi_Password")
while not sta_if.isconnected() and utime.time()<10:
    pass
print(sta_if.ifconfig())
import webrepl
webrepl.start()

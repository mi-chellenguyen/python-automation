from datetime import datetime, timedelta
from scapy.all import sniff,Ether,DHCP
from win10toast import ToastNotifier
from decouple import config

# This script will scan the users dhcp network for devices that connect to the users internet
# and will send a notification when a known device is connected.

interface="Wi-Fi"

# How long device needs to have left network to alert it connecting back on
alert_delay = timedelta(seconds=10)

# Known Devices on the network
# contains name of device or MAC address
# and the name to be displayed
familiar_devices = config('FAMILIAR_DEVICES')

def new_device_join(message):
    """
    action when a new device joins network
    """
    toaster = ToastNotifier()
    print(message)
    toaster.show_toast("DHCP Listener",
                       message,
                       duration=15)

def log_device(message):
    print(message)

def find_hostname(pkt):
    for option in pkt[0][DHCP].options:
        if isinstance(option,tuple):
            opt_name, value = option
            if opt_name == "hostname":
                return value.decode()
    return "Unknown"


if __name__ == "__main__":
    print("Listening on interface", interface)

    while True:
        current_time = datetime.now()
        packet = sniff(iface=interface,filter="port 67 or port 68",count=1)
        mac_address=packet[Ether][0].src

        # when packet is found, go through DHCP options to find hostname
        hostname = find_hostname(packet)
        
        if not hostname == "Unknown":
            if hostname in familiar_devices.keys() \
                or mac_address in familiar_devices.keys():
                display_name = familiar_devices[hostname]
                message = "{} has joined the network.".format(display_name)
                new_device_join(message)
            else:
                message = "{} has joined the network at {}.".format(hostname, current_time)
                log_device(message)

        # if current_time > device.last_seen + alert_delay:
        #     new_device_join(say_string)
        # device.last_seen = current_time
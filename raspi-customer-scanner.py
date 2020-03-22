# The previous line ensures that this script is run under the context
# of the Python interpreter. Next, import the Scapy functions:
import urllib
from logging.handlers import RotatingFileHandler

import requests
from scapy.all import *

# Define the interface name that we will be sniffing from, you can
# change this if needed.
LOG_NAME = "raspi-customer-scanner"


def sniff_for_clients(monitoring_interface, sniffing_time_in_sec, loop_count=0):
    logger = logging.getLogger(LOG_NAME)

    observedclients = []

    def sniff_callback(packet):
        # Define our tuple (an immutable list) of the 3 management frame
        # subtypes sent exclusively by clients. I got this list from Wireshark.
        management_type = 0
        client_subtypes = (0, 2, 4)

        logger.debug("Loop {:d}: Detected device MAC {:s} with type {:d} and subtype {:d}".format(loop_count, str(
            packet.addr2),
                                                                                                  packet.type,
                                                                                                  packet.subtype))

        if packet.type == management_type and packet.subtype in client_subtypes:
            # We only want to print the MAC address of the client if it
            # hasn't already been observed. Check our list and if the
            # client address isn't present, print the address and then add
            # it to our list.

            if packet.addr2 not in observedclients:
                logger.debug("Loop {:d}: New client MAC {:s}".format(loop_count, (str(packet.addr2))))
                observedclients.append(packet.addr2)
                logger.debug("Loop {:d}: Current client count {:d}.".format(loop_count, len(observedclients)))

    sniff(iface=monitoring_interface, prn=sniff_callback, timeout=sniffing_time_in_sec)
    return observedclients


def send_to_backend(backend, location_id, occupancy):
    logger = logging.getLogger(LOG_NAME)
    occupancy_data = {
        "clientType": "IOT",
        "occupancy": occupancy
    }
    occupancy_url = urllib.parse.urljoin(backend, "locations/{:s}/occupancy".format(str(location_id)))
    logger.info("Send occupancy {:1f} to {:s}.".format(occupancy, occupancy_url))
    response = requests.post(occupancy_url, json=occupancy_data)
    logger.info("Response: {:d}".format(response.status_code))


def get_occupancy(number_of_clients):
    if number_of_clients < 1:
        return 0.0
    if number_of_clients < 2:
        return 0.5
    else:
        return 0.8


def start_monitoring():
    pass


def stop_monitoring():
    pass


def main(monitoring_interface=None, sniffing_time_in_sec=10, backend=None, location_id=None):
    logger = logging.getLogger(LOG_NAME)
    if monitoring_interface is None:
        logger.info("No monitoring interface specified. Aborting.")
        return sys.exit(-1)

    if backend is None:
        logger.info("No backend specified. Aborting.")
        return sys.exit(-1)

    if location_id is None:
        logger.info("No supermarket specified. Aborting.")
        return sys.exit(-1)

    logger.info(
        "Starting to monitor supermarket {:d} on {:s} with interval of {:d} sec and report to {:s}.".format(
            location_id,
            monitoring_interface,
            sniffing_time_in_sec, backend))

    loop_count = 1
    while True:
        try:
            if loop_count == 2:
                break
            start_monitoring()
            observed_clients = sniff_for_clients(monitoring_interface, sniffing_time_in_sec, loop_count)
            number_of_clients = len(observed_clients)
            logger.info("Loop {:d}: Detected {:d} clients".format(loop_count, number_of_clients))
            occupancy = get_occupancy(number_of_clients)
            stop_monitoring()
            send_to_backend(backend, location_id, occupancy)
            loop_count += 1

        except KeyboardInterrupt:
            break

    sys.exit(0)


if __name__ == '__main__':
    config = {
        "monitoring_interface": "wlan0mon",
        "sniffing_time_in_sec": 10,
        "backend": "https://api.happyhamster.org/v1/",
        "location_id": 353978370
    }
    monitoring_interface = "wlan0mon"
    logger = logging.getLogger(LOG_NAME)
    logger.setLevel("DEBUG")
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    file_handler = RotatingFileHandler("raspi-customer-scanner.log", maxBytes=5000000, backupCount=100)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    main(**config)

import argparse
import paho.mqtt.client as mqtt
import logging
import sys


KEEP_ALIVE_TIME = 60


# The callback for when the client receives a CONNACK response from the server.
def on_connect(mqttc, userdata, flags, rc):
    logging.info("Connected with result code " + str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(mqttc, userdata, msg):
    print(msg.payload.decode("utf-8"))
    sys.exit(0)


# try connect to the host and port
def connect(mqttc, host, port):
    try:
        mqttc.connect(args.host, args.port, KEEP_ALIVE_TIME)
    except Exception as ex:
        logging.error("Connection failed: " + str(ex))
        sys.exit(0)


def subscribe(mqttc, netid, action):
    mqttc.subscribe(f"{netid}/{action}/response", qos=0)


def publish(mqttc, netid, action, message):
    mqttc.publish(f"{netid}/{action}/request", message, qos=0)


# loop forever to receive
def receive(client):
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt Detected!")
        sys.exit(0)


# function to run a series of functions
def run(args):
    mqttc = mqtt.Client(args.netid)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    connect(mqttc, args.host, args.port)
    subscribe(mqttc, args.netid, args.action)
    publish(mqttc, args.netid, args.action, args.message)
    receive(mqttc)


# function to parse arguments
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "netid",
        type=str,
    )
    parser.add_argument(
        "action",
        type=str,
        choices=["lowercase", "uppercase", "reverse", "shuffle", "random"],
    )
    parser.add_argument(
        "message",
        type=str,
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        required=False,
        default=1883,
        help="port to bind to",
    )
    parser.add_argument(
        "--host",
        type=str,
        required=False,
        default="localhost",
        help="default is set to localhost",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        required=False,
        action="store_true",
        help="turn on debugging output",
    )
    return parser.parse_args()


# main function
if __name__ == "__main__":
    args = parse_arguments()
    # if verbose flag is high, turn on verbose
    if args.verbose:
        logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
    run(args)

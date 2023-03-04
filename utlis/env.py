import json

config = json.load(open("config.json"))

BOT_TOKEN = config["BOT_TOKEN"]
RPC_URL = config["RPC_URL"]
DISTRBUTER_ADDRESS = config["DISTRBUTER_ADDRESS"]
BUSD_ADDRESS = config["BUSD_ADDRESS"]
BDF_ADDRESS = config["BDF_ADDRESS"]
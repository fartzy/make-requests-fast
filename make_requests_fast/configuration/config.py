import configparser
import os

from pkg_resources import resource_stream

# Without this line relative paths don't work when calling a script from another file
DIRNAME = os.path.dirname(__file__)
FILENAME = "config.ini"

# Initiate the parser
service_config = configparser.ConfigParser()


CONFIG_PATH = os.path.join(DIRNAME, FILENAME)
if not os.path.exists(CONFIG_PATH):
    CONFIG_PATH = resource_stream(__name__, FILENAME)
    service_config.read_file(CONFIG_PATH)
else:
    service_config.read(CONFIG_PATH)

# Build config
LIBRARY_NAME = service_config["Build"]["library_name"]
LIBRARY_VERSION = service_config["Build"]["library_version"]

# Execute config
TIMEOUT_SECONDS = service_config["Execute"]["timeout_seconds"]
CHUNK_SIZE = service_config["Execute"]["chunk_size"]
LOGGING_DIR = service_config["Execute"]["logging_dir"]

# Deploy config
LIBRARY_NAME = service_config["Deploy"]["library_name"]
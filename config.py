import configparser
import os

__file = None
username = None
password = None

try:
    from xdg.BaseDirectory import xdg_config_home
    __file = xdg_config_home + "/quiosque-dl.conf"
except ImportError:
    __file = os.path.expanduser("~") + "/.quiosque-dl.conf"

if not os.path.exists(__file):
    raise FileNotFoundError


def run():
    global username
    global password
    parser = configparser.ConfigParser()
    parser.read(__file)
    username = parser["User"]["Name"]
    password = parser["User"]["Password"]


run()

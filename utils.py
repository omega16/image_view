

import logging
import sys
import json
import platform 
from pathlib import Path

#TODO Internationalize the package
_=lambda x: x

current_os = platform.system()

view_vars = {
    "max_user_zoom":1.5,
    "min_user_zoom":0.05,
    "user_zoom":0.05
}


def set_logger(name,formate=None,level=None):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler(sys.stdout)
    if formate:
        formatter = logging.Formatter(formate)
    else :
        formatter = logging.Formatter('%(funcName)s:%(name)s:%(levelname)s:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    if level=="debug":
        logger.setLevel(logging.DEBUG)
    elif level=="info":
        logger.setLevel(logging.DEBUG)
    
    return logger



log_configuration = set_logger(__name__+"main",level="debug")



def load_configuration_file(rute):
    if isinstance(rute,Path):
        configuration_path = rute
    elif isinstance(rute,str):
        configuration_path = Path(rute)
    else :
        log_configuration.debug("Configuration must be Path or String not {}".format(type(rute)))
        return False

    if not configuration_path.exists():
        log_configuration.debug("Not found configuration_path : {}".format(
                                str(configuration_path)))
        return False

    if not configuration_path.is_file():
        log_configuration.debug("Isn't file configuration_path : {}".format(
                                str(configuration_path)))
        return False

    try : 
        with open(configuration_path,"r") as configuration_file:
            configuration_raw = configuration_file.read()
    except FileNotFoundError:
        log_configuration.debug("Can't open or read '{}' as configuration file ".format(
                                str(configuration_path)))
        return False

    try :
        configuration = json.loads(configuration_raw)
    except json.decoder.JSONDecodeError as e:
        log_configuration.debug("Invalid configuration file (json error) :'{}'".format(
                                str(configuration_path)))
        log_configuration.debug(e)
        return False

    return configuration






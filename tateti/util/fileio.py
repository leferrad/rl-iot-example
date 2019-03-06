#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.handlers
import json
import tarfile
import os


def get_logger(name='tateti', level='debug', disabled=False):
    """
    Function to obtain a normal logger

    :param name: string
    :param level: string, which can be 'info' or 'debug'
    :param disabled: boolean, if True then the logger won't print anything
    :return: logging.Logger
    """

    levels = {'info': logging.INFO,
              'debug': logging.DEBUG}

    # If the level is not supported, then force it to be info
    if level not in levels:
        level = 'info'
    level = levels[level]

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    # Finally, use this flag to easily disable logging if required
    logger.disabled = disabled

    return logger


def save_dict_as_json(dictobj, filename, pretty_print=True):
    try:
        with open(filename, 'w') as f:
            if pretty_print is True:
                json.dump(dictobj, f, sort_keys=True, indent=4)
            else:
                json.dump(dictobj, f)
        successful = True
    except:
        successful = False
    return successful


def load_json_as_dict(filename):
    try:
        with open(filename, 'r') as f:
            dictobj = json.load(f)
    except:
        dictobj = None
    return dictobj


def compress_tar_files(files, filename):
    if isinstance(files, list) is False:
        files = [files]

    try:
        with tarfile.open(filename, "w:gz") as tar:
            for f in files:
                tar.add(f, arcname=os.path.basename(f))
        successful = True
    except:
        successful = False
    return successful


def decompress_tar_files(filename):
    try:
        with tarfile.open(filename, "r:gz") as tar:
            tar.extractall(path=os.path.dirname(filename))
        successful = True
    except:
        successful = False
    return successful
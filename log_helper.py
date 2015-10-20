#!/usr/bin/env python
import logging
import logging.config
import os
import yaml


def init_logger():
    logging_yaml = 'log.yaml'
    with open(logging_yaml) as f:
        data = yaml.load(f)
    logger_dir = 'log'
    if not os.path.isdir(logger_dir):
        os.mkdir(logger_dir)
    logging.config.dictConfig(data)


def get_logger():
    return logging.getLogger('logger')

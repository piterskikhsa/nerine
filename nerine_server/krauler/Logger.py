#!/usr/bin/env python
# coding: utf-8


import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('log.txt')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(funcName)s in %(filename)s wrote: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

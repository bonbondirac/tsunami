#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2012-8-8

@author: diracfang
'''

import tornado.options
import socket

hostname = socket.gethostname()

if hostname in ('diracfang-VAIO', 'ubuntu'):
    ENV_TAG = 'home'
elif hostname in ('diracfang', 'liubida-desktop'):
    ENV_TAG = 'local'
elif hostname in ('tc_69_54',):
    ENV_TAG = 'dev'
elif hostname in ('tc_69_53', 'tc_6_173', 'tc_6_175'):
    ENV_TAG = 'test'
else:
    ENV_TAG = 'prod'

if ENV_TAG in ('local', 'home'):
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0
    
    MYSQL_HOST = '127.0.0.1'
    MYSQL_PORT = 3306
    MYSQL_USER = 'sohukan'
    MYSQL_PASSWD = 'sohukan'
    MYSQL_DB = 'sohupocketlib'
    MYSQL_MAX_IDLE_TIME = 7 * 3600

if ENV_TAG in ('test',):
    REDIS_HOST = '10.10.69.53'
    REDIS_PORT = 6379
    REDIS_DB = 0
    
    MYSQL_HOST = '10.10.69.53'
    MYSQL_PORT = 3306
    MYSQL_USER = 'sohukan'
    MYSQL_PASSWD = 'sohukan'
    MYSQL_DB = 'sohupocketlibtest'
    MYSQL_MAX_IDLE_TIME = 7 * 3600

if ENV_TAG in ('prod',):
    REDIS_HOST = '10.10.124.177'
    REDIS_PORT = 6379
    REDIS_DB = 0
    
    MYSQL_HOST = '10.10.58.17'
    MYSQL_PORT = 3306
    MYSQL_USER = 'sohupocketlib'
    MYSQL_PASSWD = 'SejJGGk2'
    MYSQL_DB = 'sohupocketlib'
    MYSQL_MAX_IDLE_TIME = 20 * 60


def command_line_options():
    tornado.options.define("port", default=8888, help="run on the given port", type=int)
    tornado.options.parse_command_line()
    
    return tornado.options.options

COMMAND_LINE_OPTIONS = command_line_options()
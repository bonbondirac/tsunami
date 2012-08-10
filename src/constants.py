#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2012-8-8

@author: diracfang
'''
KEY_USER_CHANNEL = 'user.channel:%s-%s' # require env_tag, user_id
BREAK_SYMBOL = '\r\n'
# due to nginx default settings, <60 should be your choice
KEEP_ALIVE_INTERVAL = 30
DEFAULT_CHANNEL = 'default.channel'

msg_config = {
              'sync': {
                       'type': 'command',
                       'message': 'sync',
                       }
              }

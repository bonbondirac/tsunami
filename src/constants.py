#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2012-8-8

@author: diracfang
'''
KEY_USER_CHANNEL = 'user.channel:%s-%s' # require env_tag, user_id
BREAK_SYMBOL = 'br<br />\r\n'
KEEP_ALIVE_INTERVAL = 10
DEFAULT_CHANNEL = 'default.channel'

msg_config = {
              'sync': {
                       'type': 'command',
                       'message': 'sync',
                       }
              }

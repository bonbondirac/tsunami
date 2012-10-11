#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2012-8-8

@author: diracfang
'''
KEY_USER_CHANNEL = 'user.channel:%s-%s' # require env_tag, user_id
KEY_ACCESS_TOKEN_CACHE = 'cache:access.token:%s-%s' # require env_tag, access_token

BREAK_SYMBOL = '\r\n'

DEFAULT_CHANNEL = 'default.channel'

# due to nginx default settings, <60 should be your choice
KEEP_ALIVE_INTERVAL = 30

ACCESS_TOKEN_CACHE_TIMEOUT = 24 * 3600

msg_config = {
              'sync': {
                       'type': 'command',
                       'message': 'sync',
                       }
              }

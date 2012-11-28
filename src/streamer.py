#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2012-8-8

@author: diracfang
'''

import constants
import listener
import settings
import threading
import anyjson
import logging
import time

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

class Streamer(threading.Thread):
    
    def __init__(self, redis_ins):
        super(Streamer, self).__init__()
        self.redis_ins = redis_ins
        self.ps = self.redis_ins.pubsub()
        # establish connection first to prevent multi-threading issue
        self.ps.subscribe(constants.DEFAULT_CHANNEL)
        self.listeners = listener.Listener(redis_ins)
    
    def _get_channel(self, listener):
        channel = constants.KEY_USER_CHANNEL % (settings.ENV_TAG,
                                                listener.get_current_user().get_user_id())
        
        return channel
        
    def add_listener(self, listener):
        channel =  self._get_channel(listener)
        count = self.listeners.add_listener(channel, listener)
        if count == 1:
            self.ps.subscribe(channel)
        
        return None
    
    def remove_listener(self, listener):
        channel = self._get_channel(listener)
        count = self.listeners.remove_listener(channel, listener)
        if count == 0:
            self.ps.unsubscribe(channel)
        
        return None

    def run(self):
#        keep trying when redis connection problem happens
        while True:
            try:
                for received_msg in self.ps.listen():
                    logger.info('broadcasting: %s' % received_msg)
                    if received_msg['type'] == 'message':
                        self._write_streams(received_msg)
            except:
#                use another connection, existing subscribes are lost
                self.ps = self.redis_ins.pubsub()
                time.sleep(1)

    def _write_streams(self, received_msg):
        channel = received_msg['channel']
        channel_listeners = self.listeners.get_channel_listeners(channel)
        for channel_listener in channel_listeners:
            try:
                self._write_one_stream(channel_listener, received_msg)
            except:
                pass
        
        return None
    
    def _write_one_stream(self, channel_listener, received_msg):
        channel_listener.write(self._serialize_msg(received_msg['data']))
        channel_listener.write(constants.BREAK_SYMBOL)
        channel_listener.flush()
        
        return None
    
    def _serialize_msg(self, short_msg):
        new_msg = constants.msg_config.get(short_msg, dict())
        new_msg = anyjson.dumps(new_msg)
        
        return new_msg
    
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
import redis

class Streamer(threading.Thread):
    
    def __init__(self):
        super(Streamer, self).__init__()
        self.redis_ins = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        self.ps = self.redis_ins.pubsub()
        # establish connection first to prevent multi-threading issue
        self.ps.subscribe(constants.DEFAULT_CHANNEL)
        self.listeners = listener.Listener()
    
    def _get_channel(self, listener):
        channel = constants.KEY_USER_CHANNEL % (settings.ENV_TAG, listener.get_current_user())
        
        return channel
        
    def add_listener(self, listener):
        channel =  self._get_channel(listener)
        self.listeners.add_listener(channel, listener)
        self.ps.subscribe(channel)
        
        return None
    
    def remove_listener(self, listener):
        channel = self._get_channel(listener)
        count = self.listeners.remove_listener(channel, listener)
        if count == 0:
            self.ps.unsubscribe(channel)
        
        return None

    def run(self):
        for received_msg in self.ps.listen():
            print received_msg
            if received_msg['type'] == 'message':
                self._write_stream(received_msg)
    
    def _write_stream(self, received_msg):
        channel = received_msg['channel']
        channel_listeners = self.listeners.get_channel_listeners(channel)
        for listener in channel_listeners:
            listener.write(received_msg['data'])
            listener.flush()
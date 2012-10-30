#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2012-8-8

@author: diracfang
'''

import constants
import settings

class Listener(object):
    
    def __init__(self, redis_ins):
        self.redis_ins = redis_ins
        self.listeners = dict()
#        inner variable for the `listeners_counter` property
        self._listeners_count = 0
    
    def add_listener(self, channel, listener):
        channel_listeners = self.get_channel_listeners(channel)
        channel_listeners.add(listener)
        self.listeners[channel] = channel_listeners
        count = len(channel_listeners)
        self.listeners_count += 1
        
        return count
    
    def remove_listener(self, channel, listener):
        channel_listeners = self.get_channel_listeners(channel)
        channel_listeners.discard(listener)
        if not channel_listeners:
            # provide a default value to prevent KeyError
            self.listeners.pop(channel, None)
        else:
            self.listeners[channel] = channel_listeners
        count = len(channel_listeners)
        self.listeners_count -= 1
        
        return count
    
    def get_channel_listeners(self, channel):
        channel_listeners = self.listeners.get(channel, set())
        
        return channel_listeners
    
    def _get_listeners_count(self):
        
        return self._listeners_count
    
    def _set_listeners_count(self, listeners_count):
        counter_key = constants.KEY_CONNECTIONS_COUNT % settings.ENV_TAG
        worker_key = constants.KEY_TSUNAMI_WORKER_ID % (settings.hostname, settings.COMMAND_LINE_OPTIONS.port)
        self.redis_ins.hset(counter_key, worker_key, str(listeners_count))
        self._listeners_count = listeners_count
        
        return self._listeners_count
    
#    property for simplify self._listerners_counter interface
    listeners_count = property(_get_listeners_count, _set_listeners_count)
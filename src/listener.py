#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2012-8-8

@author: diracfang
'''

class Listener(object):
    
    def __init__(self):
        self.listeners = dict()
    
    def add_listener(self, channel, listener):
        channel_listeners = self.get_channel_listeners(channel)
        channel_listeners.add(listener)
        self.listeners[channel] = channel_listeners
        count = len(channel_listeners)
        
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
        
        return count
    
    def get_channel_listeners(self, channel):
        channel_listeners = self.listeners.get(channel, set())
        
        return channel_listeners
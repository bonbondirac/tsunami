'''
Created on 2012-8-7

@author: diracfang
'''

import tornado.ioloop
import tornado.web
import threading
import redis
import constants
import time
import settings


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
        if channel_listeners:
            # provide a default value to prevent KeyError
            self.listeners.pop(channel, None)
        else:
            self.listeners[channel] = channel_listeners
        count = len(channel_listeners)
        
        return count
    
    def get_channel_listeners(self, channel):
        channel_listeners = self.listeners.get(channel, set())
        
        return channel_listeners


class Streamer(threading.Thread):
    
    def __init__(self, redis_ins):
        super(Streamer, self).__init__()
        self.redis_ins = redis_ins
        self.ps = self.redis_ins.pubsub()
        self.listeners = Listener()
    
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
        while True:
#            time.sleep(10)
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


class BaseHandler(tornado.web.RequestHandler):
    
    def get_current_user(self):
        return self.get_argument('user', None)


class MainHandler(BaseHandler):
    
    def get(self):
        self.write('Hello, world!')


class StreamHandler(BaseHandler):
    
    def initialize(self, streamer):
        self.streamer = streamer
        self._stop_signal = False
        
        return None
    
    @tornado.web.asynchronous
    def get(self):
        user = self.get_current_user()
        print 'get connection %s' % user
        if user:
            self.streamer.add_listener(self)
            self._keep_alive_loop()
        else:
            self.finish()
        
        return None
    
    def _keep_alive_loop(self):
        if not self._stop_signal:
            self.write(constants.BREAK_SYMBOL)
            self.flush()
            tornado.ioloop.IOLoop.instance() \
                   .add_timeout(time.time() + constants.KEEP_ALIVE_INTERVAL,
                                lambda: self._keep_alive_loop())
        
        return None
    
    def on_connection_close(self):
        print 'close connection'
        self.streamer.remove_listener(self)
        self._stop_signal = True
        
        return None


def main():
    redis_ins = redis.StrictRedis()
    streamer = Streamer(redis_ins)
    streamer.start()
    
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/stream", StreamHandler, dict(streamer=streamer)),
        ])
    
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
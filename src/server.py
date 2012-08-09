#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2012-8-7

@author: diracfang
'''

import constants
import streamer
import time
import tornado.ioloop
import tornado.web


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
    streamer_ins = streamer.Streamer()
    streamer_ins.start()
    
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/stream", StreamHandler, dict(streamer=streamer_ins)),
        ])
    
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2012-8-7

@author: diracfang
'''

import constants
import streamer
import auth
import time
import redis
import tornado.ioloop
import tornado.web
import tornado.database
import tornado.options
import settings
import logging

logger = logging.getLogger(__name__)


class BaseHandler(tornado.web.RequestHandler):
    
    def get_current_user(self):
        if not hasattr(self, 'user'):
            self.user = auth.User(self.db, self.redis_ins, self.get_cookie('access_token', ''))
        return self.user


class MainHandler(BaseHandler):
    
    def get(self):
        self.write('Hello, world!')


class StreamHandler(BaseHandler):
    
    def initialize(self, db, streamer, redis_ins):
        self.streamer = streamer
        self.db = db
        self.redis_ins = redis_ins
        self._stop_signal = False
        
        return None
    
    @tornado.web.addslash
    @tornado.web.asynchronous
    def get(self):
        self.set_header('Content-Type', 'application/json')
        user = self.get_current_user()
        logger.info('get connection from user: %s' % user.get_user_id())
        if user.get_user():
            self.streamer.add_listener(self)
            self._keep_alive_loop()
        else:
            self.finish()
        
        return None
    
    def _keep_alive_loop(self):
        if not self._stop_signal:
            self.write(constants.BREAK_SYMBOL)
            self.flush()
            tornado.ioloop.IOLoop.instance().add_timeout(
                time.time() + constants.KEEP_ALIVE_INTERVAL, lambda: self._keep_alive_loop()
            )
        
        return None
    
    def on_connection_close(self):
        logger.info('close connection from user: %s' % self.get_current_user().get_user_id())
        self.streamer.remove_listener(self)
        self._stop_signal = True
        
        return None


def command_line_options():
    tornado.options.define("port", default=8888, help="run on the given port", type=int)
    tornado.options.parse_command_line()
    
    return tornado.options.options


def main():
    db = tornado.database.Connection(
        host='%s:%s' % (settings.MYSQL_HOST, settings.MYSQL_PORT),
        database=settings.MYSQL_DB,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWD,
        max_idle_time=settings.MYSQL_MAX_IDLE_TIME,
    )
    
    redis_ins = redis.StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
    )
    
    streamer_ins = streamer.Streamer(redis_ins)
    streamer_ins.start()
    
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/api/2/sync/stream/?", StreamHandler, dict(db=db, streamer=streamer_ins, redis_ins=redis_ins)),
        ])
    
    options = command_line_options()
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
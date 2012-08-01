'''
Created on 2012-6-12

@author: diracfang
'''

import tornado.ioloop
import tornado.web
import time

class MainHandler(tornado.web.RequestHandler):
    cache = None
    
    @tornado.web.asynchronous
    def get(self):
        self.infinite_loop(0)
        
    def infinite_loop(self, counter):
        cls = MainHandler
        if cls.cache:
            self.write('interrupted on %s<br />\n' % cls.cache)
            cls.cache = None
        self.write("Hello world! counter: %d<br />\n" % counter)
        self.flush()
        tornado.ioloop.IOLoop.instance().add_timeout(time.time() + 1,
                                                     lambda: self.infinite_loop(counter + 1))


class InterruptHandler(tornado.web.RequestHandler):
    
    def get(self):
        cls = MainHandler
        cls.cache = str(time.time())
        

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/interrupt", InterruptHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
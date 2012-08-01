'''
Created on 2012-6-12

@author: diracfang
'''

import tornado.ioloop
import tornado.web
import time

class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.infinite_loop(0)
        
    def infinite_loop(self, counter):
        self.write("Hello world! counter: %d<br />\n" % counter)
        self.flush()
        tornado.ioloop.IOLoop.instance().add_timeout(time.time() + 1,
                                                     lambda: self.infinite_loop(counter + 1))
    
    def on_connection_close(self):
        self.finish()
    

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
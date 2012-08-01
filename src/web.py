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
        i = 0
        while True:
            self.write("Hello world! counter: %d<br />\n" % i)
            self.flush()
            i += 1
#            tornado.ioloop.IOLoop.instance().add_timeout(time.time() + 1)
            time.sleep(1)
        self.finish()

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
import bdb


class Yoda(bdb.Bdb):
    run = 0

    def user_call(self, frame, args):
        name = frame.f_code.co_name or "<unknown>"
        print "call", name, args
        self.set_step()  # continue

    def user_line(self, frame):
        print frame.f_locals['__file__'] + '_' + str(frame.f_lineno)
        print [(var, value) for var, value in frame.f_locals.items() if not var.startswith('__')]
        self.set_step()

    def user_return(self, frame, value):
        name = frame.f_code.co_name or "<unknown>"
        print "return from", name, value
        print "continue..."
        self.set_step()  # continue

    def user_exception(self, frame, exception):
        name = frame.f_code.co_name or "<unknown>"
        print "exception in", name, exception
        print "continue..."
        self.set_continue()  # continue

db = Yoda()
db.set_trace()

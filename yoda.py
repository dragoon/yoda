import bdb
import types


class Yoda(bdb.Bdb):
    run = 0

    def _filter_locals(self, local_vars):
        new_locals = []
        for name, value in local_vars.items():
            if name.startswith('__'):
                continue
            if isinstance(value, types.ModuleType):
                continue
            new_locals.append((name, value))
        return new_locals

    def user_call(self, frame, args):
        name = frame.f_code.co_name or "<unknown>"
        print "call", name, args
        self.set_step()  # continue

    def user_line(self, frame):
        print frame.f_locals['__file__'] + '_' + str(frame.f_lineno)
        print self._filter_locals(frame.f_locals)
        self.set_step()

    def user_return(self, frame, value):
        name = frame.f_code.co_name or "<unknown>"
        print "return from", name, value
        self.set_step()  # continue

    def user_exception(self, frame, exception):
        name = frame.f_code.co_name or "<unknown>"
        print "exception in", name, exception
        print "continue..."
        self.set_continue()  # continue

db = Yoda()
db.set_trace()

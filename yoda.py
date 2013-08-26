import bdb
from collections import defaultdict
import types


class Yoda(bdb.Bdb):
    run = 0
    json_results = None
    # TODO: remove one of those
    not_instrumented_types = (types.ModuleType, types.BufferType, types.BuiltinFunctionType,
                              types.TypeType, types.BuiltinMethodType, types.ClassType,
                              types.CodeType, types.ComplexType, types.FileType, types.FrameType,
                              types.FunctionType, types.GeneratorType, types.GetSetDescriptorType,
                              types.SliceType, types.UnboundMethodType, types.XRangeType)
    instrumented_types = (types.DictType, types.StringType, types.BooleanType, types.FloatType,
                          types.IntType, types.ListType, types.LongType, types.NoneType,
                          types.ObjectType, types.UnicodeType, types.TupleType)

    def __init__(self):
        bdb.Bdb.__init__(self)
        self.json_results = defaultdict(lambda: defaultdict(list))

    def _filter_locals(self, local_vars):
        new_locals = []
        for name, value in local_vars.items():
            if name.startswith('__'):
                continue
            if isinstance(value, self.not_instrumented_types):
                continue
            new_locals.append((name, value))
        return new_locals

    def user_call(self, frame, args):
        self.set_step()  # continue

    def user_line(self, frame):
        self.json_results[frame.f_globals['__file__']][frame.f_lineno].append(self._filter_locals(frame.f_locals))
        self.set_step()

    def user_return(self, frame, value):
        name = frame.f_code.co_name or "<unknown>"
        print self.json_results
        print "return from", name, value
        self.set_step()  # continue

    def user_exception(self, frame, exception):
        name = frame.f_code.co_name or "<unknown>"
        print "exception in", name, exception
        print "continue..."
        self.set_continue()  # continue

db = Yoda()
db.set_trace()

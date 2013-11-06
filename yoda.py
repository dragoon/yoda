import bdb
from collections import defaultdict
import types
import os.path
from pymongo import MongoClient
from datetime import datetime

import settings
from reports.html_report import html_report


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
        if not settings.DEBUG:
            self.client = MongoClient(settings.MONGODB_URI)
            self.db = self.client['yoda']
        self._clear_cache()

    def _clear_cache(self):
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
        # TODO: may be also flush on call
        self.set_step()  # continue

    def user_line(self, frame):
        # str line number because mongo do not accept int keys
        lineno = str(frame.f_lineno-1)
        self.json_results[frame.f_globals['__file__']][lineno].append(self._filter_locals(frame.f_locals))
        self.set_step()

    def user_return(self, frame, value):
        if self.json_results:
            for module_file, lines in self.json_results.iteritems():
                if settings.DEBUG:
                    print module_file
                    print lines
                else:
                    collection_name, _ = os.path.splitext(os.path.basename(module_file))
                    collection = self.db['file']
                    item = {'revision': 1,
                            'filename': module_file,
                            'timestamp': datetime.utcnow(),
                            'lines': [{'lineno': lineno, 'data': data} for lineno, data in lines.iteritems()]}
                    collection.insert(item)
                if settings.HTML_REPORT:
                    html_report(settings.REPORT_DIR, [(os.path.basename(module_file),
                                                       {'source_file': module_file,
                                                        'lines': lines})])
            self._clear_cache()
        self.set_step()  # continue

    def user_exception(self, frame, exception):
        name = frame.f_code.co_name or "<unknown>"
        print "exception in", name, exception
        self.set_continue()  # continue

db = Yoda()
db.set_trace()

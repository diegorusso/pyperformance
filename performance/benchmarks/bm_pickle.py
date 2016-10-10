
"""Script for testing the performance of pickling/unpickling.

This will pickle/unpickle several real world-representative objects a few
thousand times. The methodology below was chosen for was chosen to be similar
to real-world scenarios which operate on single objects at a time. Note that if
we did something like

    pickle.dumps([dict(some_dict) for _ in xrange(10000)])

this isn't equivalent to dumping the dict 10000 times: pickle uses a
highly-efficient encoding for the n-1 following copies.
"""

from __future__ import division

import datetime
import random
import sys

import perf.text_runner
import six
from six.moves import xrange
if six.PY3:
    long = int

__author__ = "collinwinter@google.com (Collin Winter)"


DICT = {
    'ads_flags': long(0),
    'age': 18,
    'birthday': datetime.date(1980, 5, 7),
    'bulletin_count': long(0),
    'comment_count': long(0),
    'country': 'BR',
    'encrypted_id': 'G9urXXAJwjE',
    'favorite_count': long(9),
    'first_name': '',
    'flags': long(412317970704),
    'friend_count': long(0),
    'gender': 'm',
    'gender_for_display': 'Male',
    'id': long(302935349),
    'is_custom_profile_icon': long(0),
    'last_name': '',
    'locale_preference': 'pt_BR',
    'member': long(0),
    'tags': ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
    'profile_foo_id': long(827119638),
    'secure_encrypted_id': 'Z_xxx2dYx3t4YAdnmfgyKw',
    'session_number': long(2),
    'signup_id': '201-19225-223',
    'status': 'A',
    'theme': 1,
    'time_created': long(1225237014),
    'time_updated': long(1233134493),
    'unread_message_count': long(0),
    'user_group': '0',
    'username': 'collinwinter',
    'play_count': long(9),
    'view_count': long(7),
    'zip': ''}

TUPLE = (
    [long(x) for x in
        [265867233, 265868503, 265252341, 265243910, 265879514,
         266219766, 266021701, 265843726, 265592821, 265246784,
         265853180, 45526486, 265463699, 265848143, 265863062,
         265392591, 265877490, 265823665, 265828884, 265753032]], 60)


def mutate_dict(orig_dict, random_source):
    new_dict = dict(orig_dict)
    for key, value in new_dict.items():
        rand_val = random_source.random() * sys.maxsize
        if isinstance(key, six.integer_types + (bytes, six.text_type)):
            new_dict[key] = type(key)(rand_val)
    return new_dict


random_source = random.Random(5)  # Fixed seed.
DICT_GROUP = [mutate_dict(DICT, random_source) for _ in range(3)]


def bench_pickle(loops, pickle, options):
    range_it = xrange(loops)

    # micro-optimization: use fast local variables
    dumps = pickle.dumps
    objs = (DICT, TUPLE, DICT_GROUP)
    protocol = options.protocol
    t0 = perf.perf_counter()

    for _ in range_it:
        for obj in objs:
            # 20 dumps
            dumps(obj, protocol)
            dumps(obj, protocol)
            dumps(obj, protocol)
            dumps(obj, protocol)
            dumps(obj, protocol)
            dumps(obj, protocol)
            dumps(obj, protocol)
            dumps(obj, protocol)
            dumps(obj, protocol)
            dumps(obj, protocol)
            dumps(obj, protocol)
            dumps(obj, protocol)
            dumps(obj, protocol)
            dumps(obj, protocol)
            dumps(obj, protocol)
            dumps(obj, protocol)
            dumps(obj, protocol)
            dumps(obj, protocol)
            dumps(obj, protocol)
            dumps(obj, protocol)

    return perf.perf_counter() - t0


def bench_unpickle(loops, pickle, options):
    pickled_dict = pickle.dumps(DICT, options.protocol)
    pickled_tuple = pickle.dumps(TUPLE, options.protocol)
    pickled_dict_group = pickle.dumps(DICT_GROUP, options.protocol)
    range_it = xrange(loops)

    # micro-optimization: use fast local variables
    loads = pickle.loads
    objs = (pickled_dict, pickled_tuple, pickled_dict_group)

    t0 = perf.perf_counter()
    for _ in range_it:
        for obj in objs:
            # 20 loads dict
            loads(obj)
            loads(obj)
            loads(obj)
            loads(obj)
            loads(obj)
            loads(obj)
            loads(obj)
            loads(obj)
            loads(obj)
            loads(obj)
            loads(obj)
            loads(obj)
            loads(obj)
            loads(obj)
            loads(obj)
            loads(obj)
            loads(obj)
            loads(obj)
            loads(obj)
            loads(obj)

    return perf.perf_counter() - t0


LIST = [[list(range(10)), list(range(10))] for _ in xrange(10)]


def bench_pickle_list(loops, pickle, options):
    range_it = xrange(loops)
    # micro-optimization: use fast local variables
    dumps = pickle.dumps
    obj = LIST
    protocol = options.protocol
    t0 = perf.perf_counter()

    for _ in range_it:
        # 10 dumps list
        dumps(obj, protocol)
        dumps(obj, protocol)
        dumps(obj, protocol)
        dumps(obj, protocol)
        dumps(obj, protocol)
        dumps(obj, protocol)
        dumps(obj, protocol)
        dumps(obj, protocol)
        dumps(obj, protocol)
        dumps(obj, protocol)

    return perf.perf_counter() - t0


def bench_unpickle_list(loops, pickle, options):
    pickled_list = pickle.dumps(LIST, options.protocol)
    range_it = xrange(loops)

    # micro-optimization: use fast local variables
    loads = pickle.loads
    t0 = perf.perf_counter()

    for _ in range_it:
        # 10 loads list
        loads(pickled_list)
        loads(pickled_list)
        loads(pickled_list)
        loads(pickled_list)
        loads(pickled_list)
        loads(pickled_list)
        loads(pickled_list)
        loads(pickled_list)
        loads(pickled_list)
        loads(pickled_list)

    return perf.perf_counter() - t0


MICRO_DICT = dict((key, dict.fromkeys(range(10))) for key in xrange(100))


def bench_pickle_dict(loops, pickle, options):
    range_it = xrange(loops)
    # micro-optimization: use fast local variables
    protocol = options.protocol
    obj = MICRO_DICT
    t0 = perf.perf_counter()

    for _ in range_it:
        # 5 dumps dict
        pickle.dumps(obj, protocol)
        pickle.dumps(obj, protocol)
        pickle.dumps(obj, protocol)
        pickle.dumps(obj, protocol)
        pickle.dumps(obj, protocol)

    return perf.perf_counter() - t0


BENCHMARKS = {
    # 20 inner-loops: don't count the 3 pickled objects
    'pickle': (bench_pickle, 20),

    # 20 inner-loops: don't count the 3 unpickled objects
    'unpickle': (bench_unpickle, 20),

    'pickle_list': (bench_pickle_list, 10),
    'unpickle_list': (bench_unpickle_list, 10),
    'pickle_dict': (bench_pickle_dict, 5),
}


def is_module_accelerated(module):
    return getattr(pickle.Pickler, '__module__', '<jython>') == 'pickle'


def prepare_subprocess_args(runner, args):
    if runner.args.pure_python:
        args.append("--pure-python")
    args.extend(("--protocol", str(runner.args.protocol)))
    args.append(runner.args.benchmark)


if __name__ == "__main__":
    runner = perf.text_runner.TextRunner(name='pickle')
    runner.metadata['description'] = "Test the performance of pickling."
    runner.prepare_subprocess_args = prepare_subprocess_args

    parser = runner.argparser
    parser.add_argument("--pure-python", action="store_true",
                        help="Use the C version of pickle.")
    parser.add_argument("--protocol", action="store", default=None, type=int,
                        help="Which protocol to use (default: highest protocol).")
    benchmarks = sorted(BENCHMARKS)
    parser.add_argument("benchmark", choices=benchmarks)

    options = runner.parse_args()
    benchmark, inner_loops = BENCHMARKS[options.benchmark]
    runner.name = options.benchmark
    if options.pure_python:
        runner.name += "_pure_python"
    runner.inner_loops = inner_loops

    if not options.pure_python:
        # C accelerators are enabled by default on 3.x
        if six.PY2:
            import cPickle as pickle
        else:
            import pickle
        if is_module_accelerated(pickle):
            raise RuntimeError("Missing C accelerators for pickle")
    else:
        if six.PY3:
            sys.modules['_pickle'] = None
        import pickle
        if not is_module_accelerated(pickle):
            raise RuntimeError("Unexpected C accelerators for pickle")

    if options.protocol is None:
        options.protocol = pickle.HIGHEST_PROTOCOL
    runner.metadata['pickle_protocol'] = str(options.protocol)
    runner.metadata['pickle_module'] = pickle.__name__

    runner.bench_sample_func(benchmark, pickle, options)

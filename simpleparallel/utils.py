# -*- coding: utf-8 -*-
__title__ = 'simpleparallel'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@gmail.com'
__created_on__ = '05/12/2017'
__copyright__ = "simpleparallel  Copyright (C) 2015  Steven Cutting"
__doc__ = """

Simple extensions to the standard libraries multiprocessing package.

"""

from multiprocessing import cpu_count
import math
import pickle
import warnings


try:
    import cytoolz as tlz
except ImportError:
    import toolz as tlz


# -------------------------------------------------------------------------------

def _try_pickle(obj):
    """
    Attempts to pickle func since multiprocessing needs to do this.
    """
    genericmsg = "Pickling of func (necessary for multiprocessing) failed."

    boundmethodmsg = genericmsg + '\n\n' + """
    func contained a bound method, and these cannot be pickled.  This causes
    multiprocessing to fail.  Possible causes/solutions:
    Cause 1) You used a lambda function or an object's method, e.g.
        my_object.myfunc
    Solution 1) Wrap the method or lambda function, e.g.
        def func(x):
            return my_object.myfunc(x)
    Cause 2) You are pickling an object that had an attribute equal to a
        method or lambda func, e.g. self.myfunc = self.mymethod.
    Solution 2)  Don't do this.\n
    """

    try:
        pickle.dumps(obj)
    except TypeError as e:
        if 'instancemethod' in str(e):
            warnings.warn(boundmethodmsg)
        else:
            warnings.warn(genericmsg)
        raise
    except:
        warnings.warn(genericmsg)
        raise
    return obj


@tlz.curry
def _maybe_try_pickle(testpickle, obj):
    """
    testpickle - True/False - should run _try_pickle on obj.
    """
    if testpickle:
        return _try_pickle(obj)
    else:
        return obj


# -------------------------------------------------------------------------------


@tlz.curry
def _job_count_greater_or_equal_to_1(cpu, offset, coefficient, exp, n_jobs):
    try:
        assert(n_jobs >= 1)
        return n_jobs
    except AssertionError:
        raise ValueError("".join(["set_n_jobs must result in a number greater or equal to 1: ",
                                  "{coe} * ({cpu} + {off}) ** {exp}".format(cpu=cpu,
                                                                            off=offset,
                                                                            coe=coefficient,
                                                                            exp=exp)]))


def set_n_jobs(offset=0, coefficient=1, exp=1, n_cpus=cpu_count()):
    """
    coefficeint * (#CPUs + offset) ** exp
    Defaults to number of virtual CPUs. (n_cpu)

    n_cpus - (default: multiprocessing.cpu_count())
    offset - offset is added to the default amount. (default: 0)
    coefficient - (offset + default) * coefficient. (default: 1)
    exp - (default: 1)

    Rounds up if result is a float.
    """
    return tlz.pipe(n_cpus,
                    lambda n: n + offset,
                    lambda n: n ** exp,
                    lambda n: n * coefficient,
                    math.ceil,
                    int,
                    _job_count_greater_or_equal_to_1(n_cpus,
                                                     offset,
                                                     coefficient,
                                                     exp))


# -------------------------------------------------------------------------------


def _try_check_seq_len(seq, minlen=4):
    try:
        assert(minlen <= len(seq))
    except AssertionError:
        # TODO (sc) Improve error message.
        raise ValueError("Your sequence is not large enough.")
    except TypeError as e:
        if "len()" not in str(e):
            raise e
    return seq

# -*- coding: utf-8 -*-
__title__ = 'simpleparallel'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@gmail.com'
__created_on__ = '05/12/2017'
# __copyright__ = "simpleparallel  Copyright (C) 2015  Steven Cutting"
__doc__ = """

Simple extensions to the standard libraries multiprocessing package.

"""

from multiprocessing import Pool
from multiprocessing.pool import ThreadPool

try:
    import cytoolz as tlz
    import cytoolz.curried as tlzc
except ImportError:
    import toolz as tlz
    import toolz.curried as tlzc

from simpleparallel import utils


# Look into multiprocessing.Pool().map_async() and ThreadPool.map_async()


def _fa_or_fb(pred, fa, fb):
    return lambda cvalue, *args: fa if pred(cvalue) else fb


def _is_greater_than_1(n):
    return 1 < n


@tlz.curry
def pmap(f, seq, n_jobs=utils.set_n_jobs(coefficient=0.5), chunksize=1, testpickle=True):
    utils._maybe_try_pickle(testpickle, f)
    p = Pool(n_jobs)
    return p.imap(f, seq, chunksize=chunksize)


@tlz.curry
def maybe_pmap(f, seq, n_jobs=utils.set_n_jobs(coefficient=0.5), **kwargs):
    return _fa_or_fb(_is_greater_than_1,
                     pmap(f, n_jobs=n_jobs, **kwargs),
                     tlzc.map(f))(n_jobs)(seq)


@tlz.curry
def pmap_unordered(f, seq,
                   n_jobs=utils.set_n_jobs(coefficient=0.5),
                   chunksize=1,
                   testpickle=True):
    utils._maybe_try_pickle(testpickle, f)
    p = Pool(n_jobs)
    return p.imap_unordered(f, seq, chunksize=chunksize)


@tlz.curry
def maybe_pmap_unordered(f, seq, n_jobs=utils.set_n_jobs(coefficient=0.5), **kwargs):
    return _fa_or_fb(_is_greater_than_1,
                     pmap_unordered(f, n_jobs=n_jobs, **kwargs),
                     tlzc.map(f))(n_jobs)(seq)


@tlz.curry
def tmap(f, seq, n_jobs=utils.set_n_jobs(coefficient=10), chunksize=1):
    utils._try_check_seq_len(seq, minlen=n_jobs)
    p = ThreadPool(n_jobs)
    return p.map(f, seq)


@tlz.curry
def maybe_tmap(f, seq, n_jobs=utils.set_n_jobs(coefficient=10), **kwargs):
    return _fa_or_fb(_is_greater_than_1,
                     tmap(f, n_jobs=n_jobs, **kwargs),
                     tlzc.map(f))(n_jobs)(seq)


@tlz.curry
def tmap_unordered(f, seq, n_jobs=utils.set_n_jobs(coefficient=10), chunksize=1):
    utils._try_check_seq_len(seq, minlen=n_jobs)
    p = ThreadPool(n_jobs)
    return p.imap_unordered(f, seq)


@tlz.curry
def maybe_tmap_unordered(f, seq, n_jobs=utils.set_n_jobs(coefficient=10), **kwargs):
    return _fa_or_fb(_is_greater_than_1,
                     tmap_unordered(f, n_jobs=n_jobs, **kwargs),
                     tlzc.map(f))(n_jobs)(seq)

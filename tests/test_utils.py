# -*- coding: utf-8 -*-
__title__ = 'simpleparallel'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@gmail.com'
__created_on__ = '05/12/2017'
__copyright__ = "simpleparallel  Copyright (C) 2015  Steven Cutting"

import pickle

import pytest
from hypothesis import given, reject
import hypothesis.strategies as st

from simpleparallel import utils as u


pickle_xfail = pytest.mark.xfail(raises=pickle.PickleError,
                                 reason="Object cannot be pickled.")
n_job_xfail = pytest.mark.xfail(raises=ValueError,
                                reason="Not valid n_job value.")


@pytest.mark.parametrize("obj",
                         [(u"foobarbaz", ),
                          pickle_xfail((lambda n: n, )),
                          ])
def test___try_pickle(obj):
    """
    Check that _try_pickle raises errors when it should.
    Also, check that it returns the object unaltered when it doesn't raise an error.
    """
    assert(u._try_pickle(obj) == obj)


@pytest.mark.parametrize("obj,tryit",
                         [(u"foobarbaz", True),
                          (lambda n: n, False),
                          pickle_xfail((lambda n: n, True)),
                          ])
def test___maybe_try_pickle(obj, tryit):
    assert(u._maybe_try_pickle(tryit, obj) == obj)


@given(st.integers())
def test___job_count_greater_or_equal_to_1(n_jobs):
    try:
        assert(u._job_count_greater_or_equal_to_1(0, 0, 0, 0, n_jobs) == n_jobs)
    except ValueError:
        reject()


@given(st.lists(st.integers(), min_size=5, max_size=5))
def test__set_n_jobs(args):
    # print args
    try:
        assert(u.set_n_jobs(offset=args[0], n_cpus=args[1]) > 0)
    except ValueError:
        reject()


@given(minlen=st.integers(), args=st.iterables(st.randoms()))
def test___try_check_seq_len(minlen, args):
    try:
        assert(u._try_check_seq_len(args, minlen=minlen))
    except ValueError:
        reject()

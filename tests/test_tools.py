# -*- coding: utf-8 -*-
__title__ = 'simpleparallel'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@gmail.com'
__created_on__ = '05/12/2017'
# __copyright__ = "simpleparallel  Copyright (C) 2015  Steven Cutting"

import threading

import toolz as tlz
from hypothesis import given, reject
import hypothesis.strategies as st

from simpleparallel import tools as stls


@given(n_jobs=st.integers(min_value=1, max_value=3),
       f=st.just(tlz.identity),
       seq=st.one_of(st.lists(st.integers(), average_size=10, max_size=201),
                     st.iterables(st.integers(), average_size=10, max_size=201)))
def test__tmap(n_jobs, f, seq):
    try:
        assert(len(list(stls.maybe_tmap(f, seq, n_jobs=n_jobs))) >= 0)
    except ValueError:
        reject()
    except threading.ThreadError as e:
        if "can't start new thread" in e.message:
            reject()
        else:
            raise e


@given(n_jobs=st.integers(min_value=1, max_value=3),
       chunksize=st.integers(min_value=1, max_value=1),
       f=st.just(tlz.identity),
       seq=st.one_of(st.lists(st.integers(), average_size=10, max_size=201),
                     st.iterables(st.integers(), average_size=10, max_size=201)))
def test__pmap(n_jobs, chunksize, f, seq):
    try:
        len(list(stls.maybe_pmap_unordered(f, seq, n_jobs=n_jobs, chunksize=chunksize))) >= 0
    except ValueError:
        reject()

#! /usr/bin/env bash

env coverage erase
env coverage run -a --source=simpleparallel $(which py.test)
env coverage report -m

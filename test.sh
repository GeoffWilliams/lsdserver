#!/bin/bash
#
# Run all tests including online (database) ones

cd test
python -m unittest discover

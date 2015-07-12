#!/bin/bash
#
# Run all offline tests

cd test
for TESTCASE in $(ls *.py | grep -v mysql) ; do
    python $TESTCASE
done

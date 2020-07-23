#!/bin/bash
export color_prompt=yes
cd 1lims-automation;
export PYTHONPATH='$PYTHONPATH:/1lims-automation';
export LOGURU_LEVEL='DEBUG';


xvfb-run -a nosetests -vs --nologcapture --tc-file=config.ini --with-flaky --force-flaky --max-runs=3 --min-passes=1 -m  ui_testing/testcases/basic_tests/test06_orders.py:OrdersTestCases;


#!/bin/bash

EXECUTION_FILES=(
#    ui_testing/testcases/basic_tests/test002_articles.py
#    ui_testing/testcases/extended_tests/test002_article.py
#    ui_testing/testcases/basic_tests/test004_testunits.py
#    ui_testing/testcases/basic_tests/test003_testplans.py
#    ui_testing/testcases/basic_tests/test005_contacts.py
#    ui_testing/testcases/header_tests/test007_audit_trail.py
#    ui_testing/testcases/header_tests/test010_my_profile.py
#    ui_testing/testcases/header_tests/test011_rolesandpermissions.py

#    ui_testing/testcases/order_tests/test001_orders_active_table.py
    ui_testing/testcases/order_tests/test002_orders_create_edit.py
#    ui_testing/testcases/order_tests/test003_orders_duplicate.py
#    ui_testing/testcases/order_tests/test004_orders_without_article.py
#    ui_testing/testcases/order_tests/test005_order_extended.py
  )

TEST_REG='test[0-9]{3}'


NODE_TOTAL=$1;
NODE_INDEX=$2;
RUN_REF=$3;
RUN_ID=$4;
RUN_NUMBER=$5;
WORK_DIR=$6;
ATTR=$7;
UUID=$8;

echo 'NODE_TOTAL: ' $NODE_TOTAL;
echo 'NODE_INDEX: ' $NODE_INDEX;
echo 'TEST_REG: ' $TEST_REG;
echo 'RUN_REF: ' $RUN_REF;
echo 'RUN_ID: ' $RUN_ID;
echo 'RUN_NUMBER: ' $RUN_NUMBER;
echo 'WORK_DIR: ' $WORK_DIR;
EXECUTION_RESULT=()

for TEST_FILE in "${EXECUTION_FILES[@]}"
 do
   echo 'TEST_FILE: ' $TEST_FILE;
   if [[ $ATTR = "not series" ]]
    then
      docker container run -t -v /dev/shm:/dev/shm -v $WORK_DIR:/1lims-automation -e "PYTHONPATH='$PYTHONPATH:/1lims-automation" -w /1lims-automation 0xislamtaha/seleniumchromenose:83 bash -c "NODE_TOTAL=$NODE_TOTAL NODE_INDEX=$NODE_INDEX nosetests -vs --nologcapture --with-reportportal --rp-config-file rp.ini --rp-uuid $UUID --rp-launch-description=$RUN_REF-$RUN_ID-$RUN_NUMBER --rp-logging-level=WARNING --tc-file=config.ini --tc=browser.headless:True --with-flaky --force-flaky --max-runs=3 --min-passes=1 --with-parallel -A '$ATTR' -m '$TEST_REG' $TEST_FILE"
      EXECUTION_RESULT+=($?)
    else
      docker container run -t -v /dev/shm:/dev/shm -v $WORK_DIR:/1lims-automation -e "PYTHONPATH='$PYTHONPATH:/1lims-automation" -w /1lims-automation 0xislamtaha/seleniumchromenose:83 bash -c "nosetests -vs --nologcapture --with-reportportal --rp-config-file rp.ini --rp-uuid $UUID --rp-launch-description=$RUN_REF-$RUN_ID-$RUN_NUMBER --rp-logging-level=WARNING --tc-file=config.ini --tc=browser.headless:True --with-flaky --force-flaky --max-runs=3 --min-passes=1 -A '$ATTR' -m '$TEST_REG' $TEST_FILE"
      EXECUTION_RESULT+=($?)
   fi
 done

for exit_code in "${EXECUTION_RESULT[@]}"
do
  if [[ $exit_code = 1 ]]
  then
    exit 1;
  fi
done
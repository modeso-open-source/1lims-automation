parallel_template = """
  %s:
    runs-on: ubuntu-20.04
    needs: %s
    if: ${{ always()  &&  !cancelled() }}
    strategy:
      fail-fast: false
      matrix:
        test_cases: [0, 1, 2, 3]

    steps:
      - uses: actions/checkout@master

      - name: pull docker image
        run:  docker pull 0xislamtaha/seleniumchromenose:83

      - name: %s
        if: ${{ always()  &&  !cancelled() }}
        env:
          TEST_FILE: %s
          TEST_REG: test[0-9]{3}
        run: timeout 30m docker container run -t -v /dev/shm:/dev/shm -v `pwd`:/1lims-automation -e "PYTHONPATH='$PYTHONPATH:/1lims-automation" -w /1lims-automation 0xislamtaha/seleniumchromenose:83 bash -c "NODE_TOTAL=${{ strategy.job-total }} NODE_INDEX=${{ matrix.test_cases }} nosetests -vs --nologcapture --with-reportportal --rp-config-file rp.ini --rp-uuid ${{ secrets.UUID }} --rp-launch-description=${{ github.head_ref }}-${{ github.run_id }}-${{ github.run_number }} --rp-logging-level=WARNING --tc-file=config.ini --tc=browser.headless:True  --with-flaky --force-flaky --max-runs=3 --min-passes=1 --with-parallel -A 'not series' -m '$TEST_REG' $TEST_FILE"
"""

series_template = """
  %s:
    runs-on: ubuntu-20.04
    needs: %s
    if: ${{ always()  &&  !cancelled() }}
    strategy:
      fail-fast: false

    steps:
      - uses: actions/checkout@master

      - name: pull docker image
        run:  docker pull 0xislamtaha/seleniumchromenose:83

      - name: %s
        if: ${{ always()  &&  !cancelled() }}
        env:
          TEST_FILE: %s
          TEST_REG: test[0-9]{3}
        run: timeout 30m docker container run -t -v /dev/shm:/dev/shm -v `pwd`:/1lims-automation -e "PYTHONPATH='$PYTHONPATH:/1lims-automation" -w /1lims-automation 0xislamtaha/seleniumchromenose:83 bash -c "nosetests -vs --nologcapture --with-reportportal --rp-config-file rp.ini --rp-uuid ${{ secrets.UUID }} --rp-launch-description=${{ github.head_ref }}-${{ github.run_id }}-${{ github.run_number }} --rp-logging-level=WARNING --tc-file=config.ini --tc=browser.headless:True  --with-flaky --force-flaky --max-runs=3 --min-passes=1 -A 'series' -m '$TEST_REG' $TEST_FILE"
        
"""

parallel_files = [
    "ui_testing/testcases/basic_tests/test002_articles.py",
    "ui_testing/testcases/basic_tests/test003_testplans.py",
    "ui_testing/testcases/basic_tests/test004_testunits.py",
    "ui_testing/testcases/basic_tests/test005_contacts.py",
    "ui_testing/testcases/header_tests/test007_audit_trail.py",
    "ui_testing/testcases/header_tests/test010_my_profile.py",
    "ui_testing/testcases/header_tests/test011_rolesandpermissions.py"
]

series_files = [
        "ui_testing/testcases/basic_tests/test002_articles.py",
        "ui_testing/testcases/basic_tests/test004_testunits.py",
        "ui_testing/testcases/basic_tests/test003_testplans.py",
        "ui_testing/testcases/basic_tests/test005_contacts.py",
        "ui_testing/testcases/header_tests/test007_audit_trail.py",
        "ui_testing/testcases/header_tests/test010_my_profile.py",
        "ui_testing/testcases/header_tests/test011_rolesandpermissions.py",

        "ui_testing/testcases/extended_tests/test002_article.py",
        "ui_testing/testcases/extended_tests/test003_testunits.py",
        "ui_testing/testcases/order_tests/test001_orders_active_table.py",
        "ui_testing/testcases/order_tests/test002_orders_create_edit.py",
        "ui_testing/testcases/order_tests/test003_orders_duplicate.py",
        "ui_testing/testcases/order_tests/test004_orders_without_article.py",
        "ui_testing/testcases/order_tests/test005_order_extended.py"
    ]

previous_job_name = ''
for file in parallel_files:
    module_name = file.split('/')[-1].split('.')[0]
    level = file.split('/')[-2].split('_')[0]
    job_name = f"execute_{level}_{module_name}_parallel_test_cases"
    result = parallel_template % (job_name, previous_job_name, job_name.replace('_', ' '), file)
    previous_job_name = job_name
    print(result)

for file in series_files:
    module_name = file.split('/')[-1].split('.')[0]
    level = file.split('/')[-2].split('_')[0]
    job_name = f"execute_{level}_{module_name}_series_test_cases"
    result = series_template % (job_name, previous_job_name, job_name.replace('_', ' '), file)
    previous_job_name = job_name
    print(result)

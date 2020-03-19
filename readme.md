# 1lims-autoamtion test suite: 

A fully end-to-end test suite based on selenium and integreted with Travis as a CI/CD tool. The docs below will be focused on developing and contributing to this repo.

### Development tools:
- Python 3.7
- Pycharm 

## Getting started developemt:
Run the following command 
```bash
apt-get install -y python3-dev python3-pip git xvfb
git clone https://github.com/Modeso/1lims-automation.git
cd 1lims-automation
pip3 install -r ui_testing/requirements.txt
```

### Development guidelines:
- Eahc JIRA ticket should only declear one test case.
- Create a branch with the same ID of the JIRA ticket `LIMS-XYZ`. Note that LIMS all capitals.
- Do your magic.
- Do `git status` to check which files did you change.
- Only do `git add` only for the files you wanna merge (stop doing `git add *` or `git add .`)
- Create a PR to merge to the **base branch** of your branch.
- PR should follow those rules:
    - PR name form is `LIMS-XYZ: summary`
    - Description.
    - Local execution results.
- Once there is a green travis, set `ready for review` label.
- Change the JIRA ticket status to `review`.


### Local Execute Test suite:
```bash
apt-get install -y python3-dev python3-pip git xvfb
git clone https://github.com/Modeso/1lims-automation.git
cd 1lims-automation
pip3 install -r ui_testing/requirements.txt
export PYTHONPATH='$PYTHONPATH:./'
# run in head mode
nosetests-3.4 -vs --logging-level=WARNING ui_testing/testcases/basic_tests --tc-file=config.ini --tc=site.password:admin
# run in headless mode
 xvfb-run -a nosetests-3.4 -vs --logging-level=WARNING  --with-flaky --force-flaky --max-runs=3 --no-flaky-report ui_testing/testcases/basic_tests --tc-file=config.ini --tc=site.password:admin
```

### Hints:
For chrome execution, please download the [chromedriver](http://chromedriver.chromium.org/downloads) which is compatible with your chrome browser then move it to `/usr/bin` dir. 


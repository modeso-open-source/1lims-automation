### Execute Test suite:
```bash
apt-get install -y python3-dev python3-pip git xvfb
git clone https://github.com/Modeso/1lims-automation.git
cd 1lims-automation
pip3 install -r requirements.txt
export PYTHONPATH='./'
cd ui_testing
# run in head mode
nosetests-3.4 -vs --logging-level=WARNING --with-flaky --force-flaky --max-runs=3 --no-flaky-report testcases/basic_tests --tc-file=../config.ini --tc=site.password:admin
# run in headless mode
xvfb-run -a nosetests-3.4 -vs --logging-level=WARNING  --with-flaky --force-flaky --max-runs=3 --no-flaky-report testcases/basic_tests --tc-file=../config.ini --tc=site.password:admin
```

### Hints:
For chrome execution, please download the [chromedriver](http://chromedriver.chromium.org/downloads) which is compatible with your chrome browser then move it to `/usr/bin` dir. 

### Running Status:
```bash
xtremx@0xIslamTaha /opt/code/github/modeso/1lims-automation/ui_testing [master *]
± % xvfb-run -a nosetests-3.4 -vs --logging-level=INFO --with-flaky --force-flaky --max-runs=3 --no-flaky-report testcases/basic_tests/test01_login.py --tc-file=../config.ini --tc=site.password:admin
Login with valid data ... ok
Login with non-valid data [with username='admin', password=''] ... ok
Login with non-valid data [with username='', password='admin'] ... ok
Login with non-valid data [with username='', password=''] ... ok
Login with non-valid data [with username=147852963, password=147852963] ... ok
Login with non-valid data [with username='#!@#!@#', password='#!@#!@#!@'] ... ok
Login with non-valid data [with username="' 1==1 &", password="' 1==1 &"] ... ok

----------------------------------------------------------------------
Ran 7 tests in 211.815s

OK



```
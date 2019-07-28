### Execute Test suite:
```bash
apt-get install -y python3-dev python3-pip git xvfb
git clone https://github.com/Modeso/1lims-automation.git
cd 1lims-automation
pip3 install -r requirements.txt
export PYTHONPATH='./'
# run in head mode
nosetests-3.4 -vs --logging-level=WARNING ui_testing/testcases/basic_tests --tc-file=config.ini --tc=site.password:admin
# run in headless mode
 xvfb-run -a nosetests-3.4 -vs --logging-level=WARNING  --with-flaky --force-flaky --max-runs=3 --no-flaky-report ui_testing/testcases/basic_tests --tc-file=config.ini --tc=site.password:admin
```

### Hints:
For chrome execution, please download the [chromedriver](http://chromedriver.chromium.org/downloads) which is compatible with your chrome browser then move it to `/usr/bin` dir. 

### Report:
| ____Hours____ | __Jira Test cases__ | __Coded Test cases__ |__#Line of codes__ |
|---------------|---------------------|----------------------|-------------------|
|     ~50H      |          5          |          31          |      1362         |  

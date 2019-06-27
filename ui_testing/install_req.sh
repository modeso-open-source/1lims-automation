#!/usr/bin/env bash
GREEN='\033[0;32m' # Green color
NC='\033[0m'       # No color
sudo apt-get udpdate && apt-get upgrade
sudo apt-get install -y git python3-pip python3-dev build-essential xvfb

echo -e "${GREEN}** Installing the requirements ...${NC}"
pip3 install -r ui_testing/requirements.txt

echo -e "${GREEN}** Installing chromium ...${NC}"
sudo apt-get install -y chromium-chromedriver
sudo ln -fs /usr/lib/chromium-browser/chromedriver /usr/bin/chromedriver
sudo ln -fs /usr/lib/chromium-browser/chromedriver /usr/local/bin/chromedriver


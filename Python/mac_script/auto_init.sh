#!/bin/bash
#安裝 Home-brew
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

#tools
brew install wget
brew install vim
#python
brew install python3
pip3 install pipenv
pip3 install mail-parser
pip3 install pyquery
pip3 install request
pip3 install ipython
pip3 install mail-parser
#robot
pip3 install robotframework
pip3 install robotframework-selenium2library
pip3 install robotframework-httplibrary
pip3 install robotframework-imaplibrary2
pip3 install robotframework-appiumlibrary
pip3 install Appium-Python-Client

#chrome driver
chrome_version=`/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version | awk '{print $3}' | awk -F . '{print $1}'`
if [ -z "$chrome_version" ]
then
    echo "Please Install Chrome First"
else
    echo "Chrome Version : $chrome_version"
    echo "https://chromedriver.chromium.org/downloads"
    echo "mv chromedriver /usr/local/bin"
fi
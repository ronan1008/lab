*** Settings ***
Library     AppiumLibrary

*** Test Cases ***
Open Application On Android
      Open Application     http://localhost:4723/wd/hub    platformName=Android     deviceName=PNXGAM8932802833    appPackage=com.android.settings   appActivity=.Settings
      Open Application     http://localhost:4723/wd/hub    platformName=Android     deviceName=PNXGAM8932802833    appPackage=com.asiainnovations.ace.taiwan   appActivity=com.asiainnovations.ace.main.MainActivity

 #    [Teardown]     Close Application







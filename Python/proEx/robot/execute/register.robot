*** Settings ***

Documentation	xxxxx
Metadata			Version 0.1
Library		SeleniumLibrary
Resource  ../settings/browser_setting.robot

*** Variables ***
${HOST}		www.proex.io/
${URL}		http://${HOST}/
${MAILURL}	http://10minutemail.net//
${BW}	chrome
${NoGUI}	0
${password}	  Arborabc1234
*** Test Cases ***

Test Register Many Times In Register Page
	Repeat Keyword    5 times    Test Register In Register Page



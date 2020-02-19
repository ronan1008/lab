*** Settings ***

Documentation	xxxxx
Metadata			Version 0.1

Library		SeleniumLibrary
#Library		../library/DisplayLib.py
Resource	../settings/login_setting.robot
Resource	../settings/browser_setting.robot
Resource	../settings/browser_setting.robot
#Suite Setup	DisplayLib.Start	${NoGUI}
#Suite Teardown	DisplayLib.Stop	${NoGUI}

*** Variables ***
${HOST}		www.proex.io/
${URL}		http://${HOST}/
${SSLURL}	https://${HOST}/
${BW}	chrome 
${NoGUI}	0

*** Test Cases ***


Test Click Remote Log Servers Page On Log
	[Setup]	Login WebUI	${URL}	${BW}
#	[Teardown]	Close Browser	
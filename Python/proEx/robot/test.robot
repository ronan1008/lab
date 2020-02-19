*** Settings ***

Documentation	xxxxx
Metadata			Version 0.1

Library		SeleniumLibrary
#Library		../library/DisplayLib.py
Resource	../library/browser_setting.robot
Resource	../library/login_setting.robot
Resource	../library/menu.robot
Resource	../library/log.robot
#Suite Setup	DisplayLib.Start	${NoGUI}
#Suite Teardown	DisplayLib.Stop	${NoGUI}

*** Variables ***
${HOST}		172.17.229.251
${URL}		http://${HOST}/
${SSLURL}	https://${HOST}/
${BW}	chrome 
${NoGUI}	0

*** Test Cases ***


Test Click Remote Log Servers Page On Log
	[Setup]	Login WebUI	${URL}	${BW}
	Goto Log Page
	Clear Remote Log Server
 	Add Remote Log Servers once    7.7.7.1    UDP    515    7.7.7.2    UDP    516    7.7.7.3    TCP    542    7.7.7.4    TCP    514
 	Clear Remote Log Server
 	Add Remote Log Server  192.168.9.1  UDP  514
 	Add Remote Log Server  192.168.9.2  TCP  514
 	Add Remote Log Server  192.168.9.3	UDP  555
	Add Remote Log Server  192.168.9.4  UDP  514
	Add Remote Log Server  192.168.9.5  UDP  114
	Add Remote Log Server  192.168.9.6  UDP  214
 	Disable Remote Log Server	192.168.9.1
 	Disable Remote Log Server	192.168.9.2
	Enable Remote Log Server	192.168.9.2
 	Delete Remote Log Server	192.168.9.3



Test Log Page On Log
	Goto Log Page
	Change Category To System
	Change Severity To Warning
	Change Category To Array
	Change Category To All 
	Change Severity To All
	Click Next Page Button On Log Page
	Click Next Page Button On Log Page
 	Click Prveious Page Button On Log Page
   	Click Last Page Button On Log Page
 	Click First Page Button On Log Page
	Click Refresh Button On Log Page	


Check Log on Log Page
	Goto Log Page
	Check Log On Logpage	Configuration	Notice	Apply changes
	Check Log On Logpage	Configuration	Error	Drive rebuild failed

#	[Teardown]	Close Browser	
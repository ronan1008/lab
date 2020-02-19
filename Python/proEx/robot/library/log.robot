*** Settings ***
Library	../library/CtrlMouseClick.py
Documentation	Log function control
...						include [TOMODIFY]
#Metadata			Version 0.1

*** Keywords ***

Change Category To All
	Change Category To	 All
Change Category To System
	Change Category To	 System
Change Category To Array
	Change Category To	 Array
Change Category To Security
	Change Category To	 Security
Change Category To Configuration
	Change Category To	 Configuration
Change Category To 
	[Arguments]	${cate}
	Click Log Page On Log
	Click Element	//*[@id='logdb-catalog-inputEl']
	Run Keyword If  '${cate}' == 'All'	Click Element	//ul[contains(@class,'x-list-plain')]//li[contains(text(),'System')]/preceding-sibling::li[contains(text(),'All')]
	...							ELSE	Click Element	//ul[contains(@class,'x-list-plain')]//li[contains(text(),'${cate}')]
Change Severity To All
	Change Severity To    All
Change Severity To Error
	Change Severity To    Error
Change Severity To Warning
	Change Severity To    Warning
Change Severity To Notice
	Change Severity To    Notice
Change Severity To
	[Arguments]	${cate}
	Click Log Page On Log
	Click Element	//*[@id='logdb-severity-inputEl']	
	Run Keyword If  '${cate}' == 'All'	Click Element	//ul[contains(@class,'x-list-plain')]//li[contains(text(),'Error')]/preceding-sibling::li[contains(text(),'All')]
	...							ELSE	Click Element	//ul[contains(@class,'x-list-plain')]//li[contains(text(),'${cate}')]


Click Log Page On Log
	Sleep	1s
	Wait Until Element Is Visible  //*[contains(text(),'Diagnostics')]  timeout=10
	Click Element	//a//span[text()='Log']//ancestor::a
	Wait Loading Mask

Click Next Page Button On Log Page
	${status}=	Run Keyword And Return Status	Page Should Contain Element    //a[@data-qtip='Next Page' and not(contains(@class,'disabled'))]
	Run Keyword If	'${status}' == 'True'    Click Element     //*[@data-qtip='Next Page']
	Wait Until Element Is Not Visible	//*[contains(text(),'Loading')]	timeout=240

Click Prveious Page Button On Log Page
	${status}=	Run Keyword And Return Status	Page Should Contain Element    //a[@data-qtip='Previous Page' and not(contains(@class,'disabled'))]
	Run Keyword If	'${status}' == 'True'    Click Element     //*[@data-qtip='Previous Page']	
	Wait Until Element Is Not Visible	//*[contains(text(),'Loading')]	  timeout=240

Click Last Page Button On Log Page    
	${status}=	Run Keyword And Return Status	Page Should Contain Element    //a[@data-qtip='Last Page' and not(contains(@class,'disabled'))]
	Run Keyword If	'${status}' == 'True'    Click Element     //*[@data-qtip='Last Page']	
	Wait Until Element Is Not Visible	//*[contains(text(),'Loading')]	  timeout=240

Click First Page Button On Log Page
	${status}=	Run Keyword And Return Status	Page Should Contain Element    //a[@data-qtip='First Page' and not(contains(@class,'disabled'))]
	Run Keyword If	'${status}' == 'True'    Click Element     //*[@data-qtip='First Page']	
	Wait Until Element Is Not Visible	//*[contains(text(),'Loading')]	  timeout=240

Click Refresh Button On Log Page
	${status}=	Run Keyword And Return Status	Page Should Contain Element    //a[@data-qtip='Refresh' and not(contains(@class,'disabled'))]
	Run Keyword If	'${status}' == 'True'    Click Element     //*[@data-qtip='Refresh']
	Wait Until Element Is Not Visible	//*[contains(text(),'Loading')]	  timeout=240

Click Clear Button On Log Page
	[Documentation] Clear All logs

Click Download Button On Log Page
    [Documentation]   Download Log file
	Click Element   //a[@id='logdb-download']

Clear Remote Log Server
	Click Remote Log Servers Page On Log
	${status}=	Run Keyword And Return Status	Page Should Contain Element	//td[contains(@class,'x-grid-cell-headerId-numbercolumn')]
	Run Keyword If	${status} == True	run keywords
	...	ctrl_mouse_click_elements	//td[contains(@class,'x-grid-cell-headerId-numbercolumn')]
	...	AND		Click Delete Button On Remote Log Servers Page
	...	AND		Click Confirmation Yes
	...	AND		Click Save Button On Remote Log Servers Page
	...	AND		Click Success Ok Button
	...	AND		Click Apply Button On Pages


Add Remote Log Servers once
	[Arguments]	@{logserverList}
	Click Remote Log Servers Page On Log
	:FOR    ${logserverip}    ${protocol}    ${port}    IN    @{logserverList}
	\	Click Add Button On Remote Log Servers Page
	\	Input Remote Log Server Add Log Server Log Server    ${logserverip}
	\	Input Remote Log Server Add Log Server Port    ${port}
	\	Select Protocol To    ${protocol}
	\	Click Add Log Server Save Button
	Click Save Button On Remote Log Servers Page
	Click Success Ok Button
	Click Apply Button On Pages


Add Remote Log Server
	[Arguments]	${logserverip}	${protocol}	${port}
	Click Remote Log Servers Page On Log
	Click Add Button On Remote Log Servers Page
	Input Remote Log Server Add Log Server Log Server	${logserverip}
	Input Remote Log Server Add Log Server Port		${port}
	Select Protocol To	${protocol}
	Click Add Log Server Save Button
	Click Save Button On Remote Log Servers Page
	Click Success Ok Button
	Click Apply Button On Pages

Delete Remote Log Server
	[Arguments]		${logserverip}
	Click Remote Log Servers Page On Log
	Wait Until Element Is Visible  //div[@id='rsyslogservers-body']  timeout=10  
	click Host on Remote Log Servers page	${logserverip}
	sleep	0.2s
	Click Delete Button On Remote Log Servers Page
	Click Confirmation Yes
	Click Save Button On Remote Log Servers Page
	Click Success Ok Button
	Click Apply Button On Pages

click Host on Remote Log Servers page
	[Arguments]		${Host}
	Click Element	//*[contains(text(),'${Host}')]/parent::*[contains(@class,'x-grid-cell-headerId-gridcolumn')]
Enable Remote Log Server
	[Arguments]		${logserverip}
	Click Remote Log Servers Page On Log
	Wait Until Element Is Visible  //div[@id='rsyslogservers-body']  timeout=10  
	${status}=	Run Keyword And Return Status	Page Should Not Contain Element	//*[contains(text(),'${logserverip}')]/../preceding-sibling::*//img[contains(@class,'x-grid-checkcolumn-checked')]
	Run Keyword If	'${status}' == 'True'	Click Element	//*[contains(text(),'${logserverip}')]/../preceding-sibling::*[contains(@class,'checkcolumn')]
	Click Save Button On Remote Log Servers Page
	Click Success Ok Button
	Click Apply Button On Pages

Disable Remote Log Server
	[Arguments]		${logserverip}
	Click Remote Log Servers Page On Log
	Wait Until Element Is Visible  //div[@id='rsyslogservers-body']  timeout=10
	${status}=	Run Keyword And Return Status	Page Should Contain Element	//*[contains(text(),'${logserverip}')]/../preceding-sibling::*//img[contains(@class,'x-grid-checkcolumn-checked')]
	Run Keyword If	'${status}' == 'True'	Click Element	//*[contains(text(),'${logserverip}')]/../preceding-sibling::*[contains(@class,'checkcolumn')]
	Click Save Button On Remote Log Servers Page
	Click Success Ok Button
	Click Apply Button On Pages



Click Add Button On Remote Log Servers Page
	Click Element	//span[contains(@id,'rsyslogservers-add-btnWrap')]

Click Delete Button On Remote Log Servers Page
	Click Element	//span[contains(@id,'rsyslogservers-delete-btnIconEl')]
Click Save Button On Remote Log Servers Page
	Wait Until Element Is Visible	//a[not(contains(@class,'x-item-disabled')) and @id='rsyslogservers-apply']	timeout=240
	Sleep	1s
	Click Element	//span[contains(@id,'rsyslogservers-apply-btnInnerEl')]


Click Remote Log Servers Page On Log
	Sleep	1s
	Wait Until Element Is Visible  //*[contains(text(),'Diagnostics')]  timeout=10
	Click Element	//a//span[text()='Remote Log Servers']//ancestor::a
	Wait Loading Mask

	

Input Remote Log Server Add Log Server Log Server
	[Arguments]	${volname}
	Input Text	//input[@name='host']	${volname}


Select Protocol To
	[Arguments]	${protocol}
	Click Element	//input[@name='protocol']
	Sleep	0.5s
	Click Element	//*[contains(@class,'boundlist')]//*[contains(text(),'${protocol}')]

Input Remote Log Server Add Log Server Port
	[Arguments]	${port}
	Input Text	//*[@name='port']	${port}

Click Add Log Server Save Button
	Wait Until Element Is Visible	//a[not(contains(@class,'x-item-disabled')) and @id='rsyslogserver-ok']	timeout=240
	Sleep	0.2s
	Click Element	//span[contains(@id,'rsyslogserver-ok-btnIconEl')]
	Wait Until Element Is Not Visible 	//*[contains(@id,'rsyslogserver_header_hd-textEl')]	timeout=240
	
Click Success Ok Button
	Wait Until Element Is Visible  //*[contains(text(),'Success')]	timeout=240
	Click Element  //*[contains(text(),'OK')]/ancestor::a[contains(@id,'button')]
	Wait Until Element Is Not Visible	//*[contains(text(),'Success')]	timeout=240

Check Log On Logpage	
		[Arguments]	${category}	${severity}	${event}

		${eventStatus}=	Run Keyword And Return Status	Page Should Contain Element	//*[contains(text(),'${event}')]
		Run Keyword If	'${eventStatus}' == 'False'		Log To Console	: Couldn't found "${category} ${severity} '${event}'" : '${event}' in log
		 
		${severityStatus}=	Run Keyword And Return Status	Page Should Contain Element	//*[contains(text(),'${event}')]/../preceding-sibling::td//div[contains(text(),'${severity}')]
		Run Keyword If	'${severityStatus}' == 'False'		Log To Console	: Couldn't found "${category} ${severity} '${event}'" : '${severity}' in severity

		${categoryStatus}=	Run Keyword And Return Status	Page Should Contain Element	//*[contains(text(),'${event}')]/../preceding-sibling::td//div[contains(text(),'${category}')]
		Run Keyword If	'${categoryStatus}' == 'False'		Log To Console	: Couldn't found "${category} ${severity} '${event}'" :'${category}' in category
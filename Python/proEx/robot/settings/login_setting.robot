*** Settings ***
Documentation	Ui System function control
...				include change language, logout, login etc.
*** Keywords ***

Change Language To
    [Arguments]     ${newLang}
    ${oldLang}=   Get Now Language Setting
    Click Element  //input[contains(@id,'languagecombo-')]
    Click Element  //li[text()='${newLang}']  modifier=False
    Sleep   20s
    Wait Until Page Contains  AccelStor  timeout=None  error=None

Change Language To zh_TW
    Change Language To  正體中文

Change Language To ja_JP
    Change Language To  日本語

Change Language To zh_CN
    Change Language To  简体中文

Change Language To en
    Change Language To  English

Restart System

Shutdown System

Logout UI
    Click Element   //span[contains(@id,'workspace-menu-btnWrap')]  modifier=False
    Sleep  2  reason=None
    ${str}=     Translate String To Right Language String  Logout
    Click Element   //span[contains(text(),'${str}')]/ancestor::a
    ${str}=     Translate String To Right Language String  Yes
    Click Element   //span[contains(text(),'${str}') and ancestor::div[contains(@class,'message')]]/ancestor::a



Continue to Login
    Click Yes in MultiLogin Confirm Window
	Wait Until Page Contains	AccelStor	timeout=240	error=DEBUG
	Result should be contain accelstor
	Wait Until Element is Visible	//*[@atid='volumemanagement']


Result should be contain accelstor
	Page Should Contain	AccelStor


#############################################
# i18n 
#############################################

Get Now Language Setting
    #${REL}=     Get Value  //input[contains(@id,'languagecombo-')]
	${REL}=		Execute Javascript	JAVASCRIPT	return OMV.util.i18n.getLocale();
    [Return]    ${REL}

TSTRLS
    [Documentation]     a.k.a Translate String To Right Language String
    [Arguments]     ${keyword}
    ${str}=  Translate String To Right Language String   ${keyword}
    [Return]    ${str}

Translate String To Right Language String
    [Arguments]     ${keyword}
    Wait Until Page Contains Element  //*[contains(text(),'OMV')]  timeout=20  error=None
    ${now}=     Get Now Language Setting
    ${str}=     Run Keyword If  '${now}'=='zh_TW'    i18nDict.en2tw  ${keyword}
    ...         ELSE IF     '${now}'=='ja_JP'         i18nDict.en2jp   ${keyword}
    ...         ELSE IF     '${now}'=='zh_CN'        i18nDict.en2cn   ${keyword}
    ...         ELSE IF     '${now}'=='en'        i18nDict.en2en  ${keyword}
    [Return]    ${str}

i18nDict.en2tw
	[Arguments]		${word}
	${REL}=		i18nDict	${word}		zh_TW
	[Return]	${REL}
i18nDict.en2cn
	[Arguments]		${word}
	${REL}=		i18nDict	${word}		zh_CN
	[Return]	${REL}
i18nDict.en2jp
	[Arguments]		${word}
	${REL}=		i18nDict	${word}		ja_JP
	[Return]	${REL}
i18nDict.en2en
	[Arguments]		${word}
	[Return]	${word}
i18nDict
	[Arguments]		${word}		${lang}=zh_TW
	${str}=		Execute Javascript	ARGUMENTS	${word}		JAVASCRIPT	return OMV.util.i18nDict.${lang}[arguments[0]];
	[Return]	${str}

#########################################
#   Misc keyword
#########################################

OmvMath
    [Documentation]     Javascript math mothod.
    ...                 eg. give "$s=  OmvMath  1 + 4= " then $s will be get '5'
    [Arguments]  ${str}
    ${REL}=  Execute Javascript  
    ...  var tmp = (((${str}.replace(/=/g,"")).replace(/"/g,'')).replace(/'/g,"")).replace(/ /g,'');
    ...  return eval(tmp);
    [Return]  ${REL}
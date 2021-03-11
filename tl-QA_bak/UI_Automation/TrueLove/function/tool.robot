*** Settings ***
Documentation	常用功能
#Metadata			Version 0.1

*** Keywords ***

Swipe middle To Up On Page
    Sleep    1s
    Swipe By Percent    50    50    50    10    5000
    Sleep    1s
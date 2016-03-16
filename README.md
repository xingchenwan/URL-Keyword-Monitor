# URL-Keyword-Monitor

Monitor a particular web page determined by the user. If user-determined keyword(s) change is detected at the webpage, the programme will send an alert to the user-set email address when the computer is connected to the internet. Changes in other part of the page irrelevant to the keywords set will NOT be reported.

Checking is set to repeat at 3600s (1hr) interval by launchd in Mac OS X. The time and recurring behaviours can be changed by the user.

A log is also kept at a local address for comparison purpose of programme. User may also view the log text to evaluate the details of each programme execution. Log will be cleared when URL/Keywords changed, or when the number of lines exceed an user-set value. 

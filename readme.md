# KEYLOGGER

In this script I have used few things which would be necessary for getting the information from the user like 

I have tried to get KeyStoke details, clipboard details, computer system info details, audio recording and an screenshot and sending the data through gmail
and at last will delete all files after sending of data is done.



## As this is not a full fledged Key Logger so there are few shortcomings like :

1. This works for 3 iterations of short duration but you can change it to run for more time.
1. Also not all details are send after each iterations but after when all iterations have been completed.
1. To make this Key Logger more discrete you can convert this python file to .exe file but when I tried to convert, it is directly deleted by antivirus, so give exception to this file
1. I have also tried to get video recordings but they got of too large size and I was able to deal with flash of webcam if you have any solution let me know



Now to get started what needs to be done to make this Key Logger work:

## Update email address, password , filepath and toaddr
## To make email work enable two factor authentication and create app password in google account which will be used here.

### Apart from above steps few libraries also needs to be installed to make this work:

1. pip install pynput
1. pip install scipy
1. pip install sounddevice
1. pip install cryptography
1. pip install requests
1. pip install Pillow
1. pip install clipboard
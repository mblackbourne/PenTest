#!/usr/bin/env python
# coding=UTF-8
import os
import socket
import sys
import operator
import time
from subprocess import *
from subprocess import Popen
from subprocess import PIPE
import threading
import toolkits
import scapy

questions_list = [
    "Display MANUFACTURER?: ",
    "Display UPTIME?: ",
    "Display WPS?: ",
    "Display ACK?: "
    ]

display_options_list = [
    '--manufacturer',
    '--uptime',
    '--wps',
    '--showack'
]

input_options_list = [
    "Enter TARGET BSSID (MAC address): ",
    "Enter CHANNEL: ",
    "Enter your MONITOR MODE INTERFACE: ",
    "Enter search by ESSID string (if any, leave blank if you don't know or care): ",
    "Save File: "
]

# define a variable so there will be no not-defined errors
target_bssid = ''
target_channel = '1'
target_search_regex = ''
save_file = ''
options_str = ''
mon_mode_interface = ''
#
# def subthread_hidden_ap_decloaker(mon_mode_interface):
#     # import variables
#     cap_file_dir = '/root/Cylon-Raider-Lite/logs'
#     capture_Interface = mon_mode_interface
#     dev_null = open(os.devnull,'w')
#
#     # run the hidden network sniffer in the background
#     # proc_String = "python /root/Cylon-Raider-Lite/sniffHidden.py"
#     # cmd_str = """gnome-terminal -e 'bash -c \""python /root/Cylon-Raider-Lite/sniffHidden.py; exec bash\""""
#     os.system("gnome-terminal -e 'bash -c \"python /root/Cylon-Raider-Lite/sniffHidden.py; exec bash\"'")
#     # os.system(cmd_str)
#
#     return

# def subthread_tcp_dump(mon_mode_interface):
#     timestr = time.strftime("%Y%m%d-%H%M%S")
#     cap_file_dir = '/root/Cylon-Raider-Lite/logs'
#     capture_Interface = mon_mode_interface
#     tcpdump_filename = cap_file_dir + 'tcpdump_monitor_mode_' + timestr + '.pcap'
#     # cmd_str = """tcpdump -i {0} -w {1}""".format(
#     #     str(tcpdump_filename)
#     # )
#
#     # cmd_str = """nohup tcpdump -n -i {0} -w {1} >> {2}_tcpdump_{3}.txt &""".format(
#     #     str(mon_mode_interface),
#     #     str(tcpdump_filename),
#     #     str(tcpdump_filename),
#     #     str(timestr)
#     # )
#
#     # cmd_str = """gnome-terminal -e 'bash -c \""python /root/Cylon-Raider-Lite/tcp_dump_background.py; exec bash\""""
#
#     os.system("gnome-terminal -e 'bash -c \"python /root/Cylon-Raider-Lite/tcp_dump_background.py; exec bash\"'")
#
# # # "gnome-terminal -e 'bash -c \"burpsuite; exec bash\"'"
# #     left = """gnome-terminal -e 'bash -c \""""
# #     right = """; exec bash\"'""""
#     # cmd_str = left + cmd_str + right
#     print cmd_str
#     os.system(cmd_str)
#     return

def user_input_options(mon_mode_interface):

    # question_number = 0
    # target_bssid = str(raw_input(input_options_list[question_number]))

    # question_number = 1
    # target_channel = str(raw_input(input_options_list[question_number]))
    #
    # question_number = 2
    # mon_mode_interface = str(raw_input(input_options_list[question_number]))
    if mon_mode_interface == '':
        mon_mode_interface = 'wlan1mon'

    question_number = 3
    target_search_regex = str(raw_input(input_options_list[question_number]))

    question_number = 4
    save_file = str(raw_input(input_options_list[question_number]))
    if save_file == '':
        save_file = 'unnamed'

    # target_channel = target_channel.strip()
    mon_mode_interface = mon_mode_interface.strip()
    target_search_regex = target_search_regex.strip()
    save_file = save_file.strip()

    print target_search_regex, save_file, mon_mode_interface
    display_options(target_search_regex, save_file, mon_mode_interface)
    return target_search_regex, save_file, mon_mode_interface
options_str = ''

    # cmd_String = """airodump-ng --band abg wlan1mon --encrypt WPA2 --manufacturer -a --write {0}/{1}_monitor_mode_capture.csv --write-interval 5 --output-format csv""".format(
    #     str(cap_file_dir),
    #     str(timestr))

def build_cmd_str_and_begin(target_search_regex, save_file, mon_mode_interface, options_str):
    cap_file_dir = '/root/Cylon-Raider-Lite/logs'
    timestr = time.strftime("%Y%m%d-%H%M%S")


    # append the regex string if entered
    if target_search_regex != '':
        # target_search_regex = '--essid-regex ' + target_search_regex
        target_search_regex = """ --essid-regex "{0}" """.format(str(target_search_regex)
        )


    # This bullshit here is the get TCPDUMP to run in the background
    # but nothing works, even threading, so I tried to make it a popup
    # DOesn't work either even though it should
    capture_Interface = mon_mode_interface
    # tcpdump_filename = cap_file_dir + 'tcpdump_monitor_mode_' + timestr + '.pcap'
    # os.system("gnome-terminal -e 'bash -c \"python /root/Cylon-Raider-Lite/tcp_dump_background.py; exec bash\"'")
    # module_name = '/root/Cylon-Raider-Lite/tcp_dump_background.py'
    # cmd_str = """gnome-terminal -e 'bash -c \"python {0}; exec bash\"""".format(
    #     str(module_name)
    # )
    # os.system(cmd_str)
    print toolkits.red('TCPDump executed')
    # Working code, airodump-ng --band abg
    cmd_str = "airodump-ng --band abg {0} {1} -a --write {2}/{3}_{5}_monitor_mode_capture.csv --write-interval 5 --output-format csv {4}".format(
        str(options_str),
        str(target_search_regex),
        str(cap_file_dir),
        str(timestr),
        str(mon_mode_interface),
        str(save_file)
    )
    print toolkits.red('Airodump-executed')

    # need to fix format

    cmd_str = cmd_str.strip()
    print 'DEBUG: Command string = ' + cmd_str
    # x = threading.Thread(name='subthread_hidden_ap_decloaker', target=subthread_hidden_ap_decloaker(mon_mode_interface))
    # x.start()
    # #y = threading.Thread(name='subthread_tcp_dump', target=subthread_tcp_dump(mon_mode_interface))
    # y.start()
    os.system("gnome-terminal -e 'bash -c \"python /root/Cylon-Raider-Lite/sniffHidden.py; exec bash\"'")
    os.system("gnome-terminal -e 'bash -c \"tcpdump & -w filename.pcap -i wlan1mon; exec bash\"'")

    os.system(cmd_str)
    # dont forget channel

    # x = threading.Thread(name='subthread_hidden_ap_decloaker', target=subthread_hidden_ap_decloaker(mon_mode_interface))
    # x.start()
    #y = threading.Thread(name='subthread_tcp_dump', target=subthread_tcp_dump(mon_mode_interface))
    # y.start()
    if KeyboardInterrupt:

        stop_mon_mode_str = "airmon-ng stop %s" % str(mon_mode_interface)
        #os.system('airmon-ng check kill')
        os.system('killall tcpdump')
        os.system(stop_mon_mode_str)
        os.system('cat /root/Cylon-Raider-Lite/logs/*.csv > /sdcard/Cylon_Raider_Recon.txt')
        os.system('cat /root/Cylon-Raider-Lite/logs/*.csv >/root/Cylon_Raider_Recon.txt')
        # x.terminate()


    return


def display_options(target_search_regex, save_file, mon_mode_interface):
    options_str = ''
    question = 0
    try:
        for questions in questions_list:
            print questions_list[question]
            answer = str(raw_input("Y or N: "))
            answer = answer.replace('y','Y').replace('n','N')
            if answer == 'Y':
                options_str = options_str + ' ' + display_options_list[question]
                print 'DEBUG: Current options selected:\n' + options_str
            question = question + 1
    except Exception:
        pass
    print 'DEBUG: Options = {0}'.format(options_str)

    print """

    Available encryption filters:

    1. \tOPN networks
    2. \tWPA networks
    3. \tWPA2-PSK or MGT-ENT networks
    0. \tNo encryption filter

    """

    encryption_dict = {
        1: 'OPN',
        2: 'WPA',
        3: 'WPA2',
        0: ''
        }

    filter_encryption = None
    filter_encryption = int(raw_input("Would you like to filter by encryption? (Or enter nothing to move on): "))

    try:
        if 0 < filter_encryption < 4:
            filter_encryption = """ --encrypt {0} """.format(
                str(encryption_dict[filter_encryption])
            )
            options_str = options_str + filter_encryption
        if filter_encryption == 0:
            pass
    except filter_encryption > 3 or filter_encryption < 0:
        print 'Please enter a option from 0 to 3!'
        display_options(target_search_regex, save_file, mon_mode_interface)

    build_cmd_str_and_begin(target_search_regex, save_file, mon_mode_interface, options_str)

    return options_str

def find_mon_interface():

    mon_mode_interface = str(raw_input("Enter your monitor mode interface to start (wlan1 usually, leave blank if you don't care): "))

    if mon_mode_interface == '':
        mon_mode_interface = 'wlan1'

    start_mon_mode = "airmon-ng start %s" % mon_mode_interface
    os.system(start_mon_mode)
    mon_mode_interface = mon_mode_interface + 'mon'
    user_input_options(mon_mode_interface)
    return
def main():
    find_mon_interface()
    return
main()

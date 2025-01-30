import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time
import logging
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pydivert
import os
os.chdir("C:\\Users\\TaljaaEb\\Desktop\\service")

import requests
import re
stat_1 = "N"
stat_2 = "N"
stat_3 = "N"
stat_4 = "N"
stat_5 = "N"
stat_6 = "N"

class PurchaseEventHandler(FileSystemEventHandler):
    def __init__(self, logger, transmit_func):
        self.logger = logger
        self.transmit_func = transmit_func

    def on_modified(self, event):
        if event.src_path.endswith('purchase_events.json'):
            with open(event.src_path, 'r') as f:
                purchase_data = json.load(f)
                self.logger.info(f"New purchase event: {purchase_data}")
                self.transmit_func(purchase_data)

class ReplyEventHandler(FileSystemEventHandler):
    def __init__(self, logger, reply_func):
        self.logger = logger
        self.reply_func = reply_func

    def on_modified(self, event):
        if event.src_path.endswith('reply_events.json'):
            with open(event.src_path, 'r') as f:
                reply_data = json.load(f)
                self.logger.info(f"New reply event: {reply_data}")
                self.reply_func(reply_data)

class LineEventHandler(FileSystemEventHandler):
    def __init__(self, logger, line_func):
        self.logger = logger
        self.line_func = line_func

    def on_modified(self, event):
        if event.src_path.endswith('line_events.json'):
            with open(event.src_path, 'r') as f:
                line_data = json.load(f)
                self.logger.info(f"New line event: {line_data}")
                self.line_func(line_data)


class PurchaseMonitorService(win32serviceutil.ServiceFramework):
    _svc_name_ = "A_AppLoggingService"
    _svc_display_name_ = "A_App Logging Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_alive = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

######

    def extract_strings_recursive(test_str, tag):
        # finding the index of the first occurrence of the opening tag
        start_idx = test_str.find("<" + tag + ">")
 
        # base case
        if start_idx == -1:
            return []
 
        # extracting the string between the opening and closing tags
        end_idx = test_str.find("</" + tag + ">", start_idx)
        res = [test_str[start_idx+len(tag)+2:end_idx]]
 
        # recursive call to extract strings after the current tag
        res += extract_strings_recursive(test_str[end_idx+len(tag)+3:], tag)
 
        return res

######
    def main(self):
        logging.basicConfig(filename='c_purchase_monitor.log', level=logging.INFO,
                            format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        logger = logging.getLogger('PurchaseMonitor')

        event_handler0 = LineEventHandler(logger, self.get_line)
        event_handler1 = ReplyEventHandler(logger, self.get_reply)
        observer = Observer()
        observer.schedule(event_handler0, path='.', recursive=False)
        observer.schedule(event_handler1, path='.', recursive=False)
        observer.start()

        try:
            while self.is_alive:
                time.sleep(1)
                with pydivert.WinDivert("tcp.DstPort == 81 and tcp.PayloadLength > 0") as w:
                    for packet in w:
                        payload = packet.payload
                        if bytes("SUCCESS", "utf-8") in payload:
                            dictionary = {
                                "error_code": "",
                                "status": "SUCCESS",
                                "message": "S"
                            }
                            # Serializing json
                            json_object = json.dumps(dictionary, indent=4)
                            # Writing to sample.json
                            with open("reply_events.json", "a") as outfile:
                                outfile.write(json_object)
                        w.send(packet)
                        break
#                get_reply()
#                #get_tile
#                if stat_1 == "Y":
#                    continue
#                #get_lines
#                if stat_1 == "Y" and stat_2 == "Y":
#                    continue
#                #get_reply
#                if stat_1 == "Y" and stat_2 == "Y" and stat_3 == "Y":
#                    continue
#                #notify_host
#                if stat_1 == "Y" and stat_2 == "Y" and stat_3 == "Y" and stat_4 == "Y":
#                    continue
#                #send_lines
#                if stat_1 == "Y" and stat_2 == "Y" and stat_3 == "Y" and stat_4 == "Y" and stat_5 == "Y":
#                    continue
#                #reset
#                if stat_1 == "Y" and stat_2 == "Y" and stat_3 == "Y" and stat_4 == "Y" and stat_5 == "Y" and stat_6 == "Y":
#                    continue
        except KeyboardInterrupt:
            pass
        finally:
            observer.stop()
            observer.join()
            
    def get_reply(self, data):
    #def get_reply():
        pass

            
    def get_line(self, data):
        with requests.Session() as s:
            # An authorised request.
            req = s.get('http://localhost:81/cart_trolley_checkout.html')
            lines = extract_strings_recursive(req.text, "ln")
            logging.info(f"{lines}")
            with open("line_events.json", "w") as outfile:
                    outfile.write(json_object)
    
    def transmit_data(self, data):
        logging.info(f"{data}")
        #store_ip = "192.168.1.100"  # Replace with the store's IP address
        #customer_ip = data.get('customer_ip', '127.0.0.1')

        # Transmit to store
        #self.send_data(store_ip, data)
        #logging.info(f"Data transmitted to store IP: {store_ip}")

        # Transmit to customer
        #self.send_data(customer_ip, data)
        #logging.info(f"Data transmitted to customer IP: {customer_ip}")

    def send_data(self, ip, data):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, 12345))  # Replace 12345 with the actual port number
                s.sendall(json.dumps(data).encode())
        except Exception as e:
            logging.error(f"Failed to send data to {ip}: {str(e)}")

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(PurchaseMonitorService)

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
os.chdir("%USERPROFILE%\\Desktop\\service")

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

class PurchaseMonitorService(win32serviceutil.ServiceFramework):
    _svc_name_ = "C_PurchaseMonitorService"
    _svc_display_name_ = "C_Purchase Monitor Service"

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

    def main(self):
        logging.basicConfig(filename='c_purchase_monitor.log', level=logging.INFO,
                            format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        logger = logging.getLogger('PurchaseMonitor')

        event_handler = ReplyEventHandler(logger, self.get_reply)
        observer = Observer()
        observer.schedule(event_handler, path='.', recursive=False)
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
        except KeyboardInterrupt:
            pass
        finally:
            observer.stop()
            observer.join()
            
    def get_reply(self, data):
        pass
            
    
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

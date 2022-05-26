import pythoncom
from win32.lib import win32serviceutil
from win32 import win32service
from win32 import win32event
from win32 import servicemanager
import traceback
import socket
import time
from service import MoverHandler
import sys
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from shutil import move
from time import sleep
from os import scandir, rename
from os.path import splitext, exists
import config as cfg

class DownloadManagerService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'DownloadManagerService'
    _svc_display_name_ = 'Download Manager'
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)        
        socket.setdefaulttimeout(60)
        
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        # self.run = False
        
    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        self.main()

    def main(self):
        # self.run = True
        try: 
            while rc != win32event.WAIT_OBJECT_0:
                logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
                path = cfg.source_dir
                event_handler = MoverHandler()
                observer = Observer()
                observer.schedule(event_handler, path, recursive=True)
                observer.start()
                try:
                    while True:
                        sleep(5)
                except KeyboardInterrupt:
                    observer.stop()
                observer.join()
                rc = win32event.WaitForSingleObject(self.hWaitStop, 24*60*60*1000)
        except:
            servicemanager.LogErrorMsg(traceback.format_exc()) # if error print it to event log
        
        
        
   
       
        
if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(DownloadManagerService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(DownloadManagerService)
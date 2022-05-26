# AutomateDownloads
 Utility to automatically copy downloaded files to seperate folders based on file extensions

 Edit config.py to match whatever paths you want for your system.
 Run service.py in a terminal and keep it running in the background.
 I tried setting it up as a service for Windows , but it caused a lot of errors ,  so that part is WIP now.
 main.py is not needed , it was being used for the windows service.
 As of now , I am using pyinstaller to make an executable file and keep it running in the background.
 I also use Task Scheduler on Windows to run the exe on startup so it works as good as a service.


from config import cfg
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
from shutil import move
from time import sleep
from os import scandir, rename
from os.path import splitext, exists





def make_unique(path):
    filename, extension = splitext(path)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(path):
        path = f"{filename} ({counter}){extension}"
        counter += 1

    return path


def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(name)
        rename(entry, unique_name)
    move(entry, dest)


class MoverHandler(FileSystemEventHandler):
    # ? THIS FUNCTION WILL RUN WHENEVER THERE IS A CHANGE IN "source_dir"
    # ? .upper is for not missing out on files with uppercase extensions
    def on_modified(self, event):
        with scandir(cfg.source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)
                self.check_model_files(entry , name)
                self.check_exec_files(entry , name)
                self.check_code_files(entry, name)
                self.check_zip_files(entry, name)

    def check_audio_files(self, entry, name):  # * Checks all Audio Files
        for audio_extension in cfg.audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                dest = cfg.dest_audio
                move_file(dest, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):  # * Checks all Video Files
        for video_extension in cfg.video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(cfg.dest_vid, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):  # * Checks all Image Files
        for image_extension in cfg.image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(cfg.dest_img, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_model_files(self, entry, name):  # * Checks all Document Files
        for model_extension in cfg.model_extensions:
            if name.endswith(model_extension) or name.endswith(model_extension.upper()):
                move_file(cfg.dest_models, entry, name)
                logging.info(f"Moved model file: {name}")

    def check_code_files(self, entry, name):  # * Checks all Document Files
        for code_extension in cfg.code_extensions:
            if name.endswith(code_extension) or name.endswith(code_extension.upper()):
                move_file(cfg.dest_code, entry, name)
                logging.info(f"Moved code file: {name}")

    def check_zip_files(self, entry, name):  # * Checks all Document Files
        for zip_extension in cfg.zip_extensions:
            if name.endswith(zip_extension) or name.endswith(zip_extension.upper()):
                move_file(cfg.dest_zip, entry, name)
                logging.info(f"Moved zip file: {name}")                       

    def check_document_files(self, entry, name):  # * Checks all Document Files
        for documents_extension in cfg.document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                move_file(cfg.dest_docs, entry, name)
                logging.info(f"Moved document file: {name}")

    def check_exec_files(self, entry, name):  # * Checks all Document Files
        for exe_extension in cfg.exe_extensions:
            if name.endswith(exe_extension) or name.endswith(exe_extension.upper()):
                move_file(cfg.dest_exe, entry, name)
                logging.info(f"Moved executable file: {name}")


if __name__=='__main__' :
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
# pylint: disable=no-name-in-module
from PyQt5.QtCore import QDataStream, QUrl, QDir, QObject, QMetaObject, QVariant, Q_ARG, QIODevice, QByteArray, QBuffer, pyqtProperty, pyqtSlot, QStringListModel, QSettings
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QGuiApplication, QImage, QIcon
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtQuick import QQuickView

from task_scheduler import Task_scheduler
from messages_for_dialog import get_title_and_message
from random import randint
from pathlib import Path
from glob import glob1
import qml_resource
import pyunsplash
import requests
import ctypes
import sys
import os

import win32com.client
import win32con

class Wallpaper_app(QObject):

    def __init__(self, context, parent=None):
        super(Wallpaper_app, self).__init__(parent)
        self.win = parent
        self.ctx = context
        self.working_path = self.get_current_path()
        self.standart_image_path = f'file:///{self.getWallpaper()}'
        # set settings for the program
        self.set_settings()

    # get title and message to show in user's dialog message
    @pyqtSlot(str, result=QVariant)
    def get_event_message(self, event):
        return get_title_and_message(event)

    @pyqtSlot(str)
    def create_or_add_log(self, message):
        if os.path.exists("log.txt"):
            f = open('log.txt', 'a')
        else:
            f = open("log.txt","w+")
        f.write(message)
        f.close() 

    @pyqtProperty('QVariant')
    def get_working_path(self):
        return self.working_path
    
    @pyqtProperty('QVariant')
    def get_random_image_path(self):
        print(f'Standard path: {self.working_path}\\random_image.jpg')
        return f'{self.working_path}\\random_image.jpg'

    @pyqtProperty('QVariant')
    def get_standart_image_path(self):
        return self.standart_image_path

    # set properties for QML
    def set_properties(self):
        self.win.setProperty("workingPath", self.working_path)
        self.win.setProperty("randomImagePath", f'{self.working_path}\\random_image.jpg')
        self.win.setProperty("standartImagePath", self.standart_image_path)

    # get the picture from the desktop to display in the application at startup
    def getWallpaper(self):
        ubuf = ctypes.create_unicode_buffer(512)
        ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_GETDESKWALLPAPER,len(ubuf),ubuf,0)
        return ubuf.value

    # initialize settings to store the data
    def set_settings(self):
        
        settings_folder_path = f'{self.working_path}\\settings'
        # make path if it doesn't exists
        if not os.path.exists(settings_folder_path):
            os.mkdir("settings")
        
        self.settings = QSettings(f'{settings_folder_path}\\settings.ini', QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)
        self.settings.setValue("wall_from_folder", {})


    @pyqtSlot(result=str)
    def get_current_path(self):
        return str(Path(__file__).parent.absolute())

    @pyqtSlot(result=str)
    def get_current_file_name(self):
        return os.path.realpath(sys.executable)

    @pyqtSlot(str, str, result=bool)
    def set_task_scheduler(self, time_btw_task_repetitions, wall_change_method):
        params = dict()
        params['action_id'] = "Change wallpaper"
        params['action_path'] = self.get_current_file_name()
        params['action_work_dir'] = self.get_current_path()  
        params['time_btw_task_repetitions'] = time_btw_task_repetitions

        if wall_change_method == 'Folder':
            params['action_args'] = "change_wall_from_folder"
            params['description'] = f'Change background wallpaper from folder every {time_btw_task_repetitions}.'
        elif wall_change_method == 'Unsplash':
            params['action_args'] = "download_new_wall_and_set_it"
            params['description'] = f'Download and change background wallpaper every {time_btw_task_repetitions}.'
        task = Task_scheduler(params)
        is_task_created = task.create_task()
        return is_task_created

    @pyqtSlot(result=bool)
    def delete_task_from_task_scheduler(self):
        task = Task_scheduler()
        del_result = task.delete_task()
        return del_result

    @pyqtSlot(str)
    def set_desktop_background_wallpaper_for_windows(self, path_to_wall):
        SPI_SETDESKWALLPAPER = 20 
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path_to_wall, 0)

    @pyqtSlot(str)
    def remember_folder_path(self, qurl_folder_path):
        folder_path = QUrl(qurl_folder_path).toLocalFile()
        self.settings.setValue("wall_from_folder/folder_path", folder_path)

    def is_sym_diff_btw_lists(self, list_1, list_2):
        diff = list(set(list_1).symmetric_difference(set(list_2)))
        if diff:
            return True
        else:
            return False

    # result=QUrl
    # with no args or with args
    @pyqtSlot(result=QVariant)
    @pyqtSlot(bool, str, result=QVariant)
    def set_wall_from_folder(self, from_task_scheduler=True, qurl_folder_path=None):
        
        path_exists = True

        if from_task_scheduler:
            folder_path = self.settings.value("wall_from_folder/folder_path")  
        # create qurl object and get src without a prefix: file:///
        else:
            folder_path = QUrl(qurl_folder_path).toLocalFile()

        # if os.path.exists(folder_path): else...
        if os.path.exists(folder_path):
            path_from_settings = ""
            excluded_walls = list()
            
            # if there's already a path for the walls, then get it
            # to compare with current folder path
            if self.settings.contains("wall_from_folder/folder_path"):
                if not from_task_scheduler:
                    path_from_settings = self.settings.value("wall_from_folder/folder_path")
                if self.settings.contains("wall_from_folder/excluded_walls"):
                    excluded_walls = self.settings.value("wall_from_folder/excluded_walls")
            # if folder path != path_from_settings or it doesn't exists yet,
            # then clear path_from_settings
            elif path_from_settings != folder_path or not self.settings.contains("wall_from_folder/folder_path"):
                self.settings.setValue("wall_from_folder/folder_path", folder_path)
                self.settings.setValue("wall_from_folder/excluded_walls", excluded_walls)

            # get current walls from the folder
            all_walls = self.get_walls_from_folder(folder_path)

            # get the difference between current walls in the folder
            # and excluded walls which have already been applied as
            # desktop wallpapers to calcucate unused random wall
            # old one: walls_for_random = list(set(all_walls).symmetric_difference(set(excluded_walls)))
            walls_for_random = list(set(all_walls) - set(excluded_walls))

            # if all wallpapers have already been used, then
            # clear all excluded walls and start again
            if not walls_for_random:
                excluded_walls = []
                # self.settings.setValue("wall_from_folder/folder_path/excluded_walls", excluded_walls)
                self.settings.setValue("wall_from_folder/excluded_walls", excluded_walls)
                walls_for_random = all_walls
            
            rand_wall_index = randint(0, len(walls_for_random) - 1)

            # add this wall to the exclude list
            excluded_walls.append(walls_for_random[rand_wall_index])
            self.settings.setValue("wall_from_folder/excluded_walls", excluded_walls)
            # set the wall
            path_to_rand_wall = f'{folder_path}/{walls_for_random[rand_wall_index]}'
            self.set_desktop_background_wallpaper_for_windows(path_to_rand_wall)
        else:
            path_exists = False
            path_to_rand_wall = folder_path
            #return output_qurl_path
        return {'path': path_to_rand_wall, 'path_exists': path_exists}

    def get_walls_from_folder(self, folder_path):
        if os.path.exists(folder_path):
            types = ('*.png', '*.jpg')
            pic_files = []
            for file_type in types:
                pic_files.extend(glob1(f'{folder_path}', file_type))
            return pic_files
        else:
            return False

    @pyqtSlot(result=bool)
    def get_unsplash_wallpaper(self):
        # set your Unsplash API key
        pu = pyunsplash.PyUnsplash(api_key='')
        search = pu.photos(type_='random', count=1, featured=True)
        for photo in search.entries:
            pic_url_response = self.get_image_from_url(photo.link_download)
            
        if pic_url_response:
            return True
        else:
            return False

    def get_image_from_url(self, pic_url):
        curr_path = self.get_current_path()
        image_path = f'{curr_path}\\random_image.jpg'
        with open(image_path, 'wb') as handle:
                response = requests.get(pic_url, stream=True)
                
                if not response.ok:
                    # something went wrong
                    print(response)
                    return False

                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)
                # downloading and writing was successful
                return True

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    app.setWindowIcon(QIcon('qrc:///icon.ico'))
    app.setOrganizationName("AndreiMikhalev")
    app.setOrganizationDomain("AndreiMikhalevDomain")

    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    wallpaper_app = Wallpaper_app(ctx)

    # set link to the python class
    ctx.setContextProperty("wallpaper_app", wallpaper_app)

    engine.load(QUrl('qrc:///qml/WallpaperApp.qml'))
    
    if not engine.rootObjects():
        sys.exit(-1)

    window = engine.rootObjects()[0]

    # parse input args
    if len(sys.argv) > 1:
        if sys.argv[1] == 'download_new_wall_and_set_it':
            # get ListModel from QML
            wallpaper_app.get_unsplash_wallpaper()
            path_to_wall = f'{wallpaper_app.working_path}\\random_image.jpg'
            wallpaper_app.set_desktop_background_wallpaper_for_windows(path_to_wall)
            sys.exit(0)
        elif sys.argv[1] == 'change_wall_from_folder':
            # get wallpaperAppWindow object from QML
            wallpaperAppWindow_obj = window.findChild(QObject, "setWallpaperBtnObj")
            QMetaObject.invokeMethod(wallpaperAppWindow_obj, "setWallpaper", Q_ARG(QVariant, "Folder"), Q_ARG(QVariant, True))
            sys.exit(0)
    sys.exit(app.exec_())
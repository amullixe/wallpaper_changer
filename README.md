# Wallpaper changer

This application allows you to automatically change the wallpaper of your Windows desktop using a random selection of pictures from a folder or downloading and set the pictures from Unsplash on your desktop. You can also set the Task Scheduler to automatically install/download wallpapers by setting the time whether it is minute, hour or day.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Note

Please note in order to work with the Unsplash components (download and set random wallpaper from Unsplash site) in this application, you will need an API key. Please enter the key in line 211 of the main.py file.

### Prerequisites

For building from source we need any application that can bundles a Python application and all its dependencies into a single package.
I'll show on example with [Auto PY to EXE](https://pypi.org/project/auto-py-to-exe/).

### Installing

1. Clone the project

2. Install requerement packages from *requirements.txt*: `pip install -r requirements.txt`

3. Generate *.py* file configuration from *qml_resource.qrc* to compile neccecery files (for example *.conf*, *.qml*) into one *.py* file: `pyrcc5 -o resource_rc.py resource.qrc`

4. Install auto-py-to-exe package: `pip install auto-py-to-exe` and open it by entering a command *auto-py-to-exe* to the command line

5. Select option `script location`. Also, at your discretion, you can set the options whether you want the project to be in one file or in one directory, and whether the console will be launched when the application is started (good for debugging). You can see an example of these options in the next screenshot:
![image](https://user-images.githubusercontent.com/43108741/84257615-46001300-ab1e-11ea-982f-39a923e254a8.png)

6. In the Auto PY to EXE click `Convert .py to .exe` and wait for the compilation to complete

8. After bundeling single package will be in the */output/* folder in the folder where you compiled the project

9. After starting the file, the application will look like this:

![image](https://user-images.githubusercontent.com/43108741/84260104-22d76280-ab22-11ea-8af4-77fc8c7fc3dd.png)
![image](https://user-images.githubusercontent.com/43108741/84469845-ad3ad600-ac8a-11ea-9ae5-67f7ddc7ac64.png)
![image](https://user-images.githubusercontent.com/43108741/84470123-4a960a00-ac8b-11ea-876e-1e2c7703b0fe.png)
![image](https://user-images.githubusercontent.com/43108741/84470779-b9279780-ac8c-11ea-8a7a-b10e2f44cbe3.png)

## Built With

* [PyQt5](https://www.riverbankcomputing.com/static/Docs/PyQt5/) - is a Python binding of the cross-platform GUI toolkit Qt, implemented as a Python plug-in.
* [pywin32](https://pypi.org/project/pywin32/) - Python extensions for Microsoft Windows Provides access to much of the Win32 API, the ability to create and use COM objects, and the Pythonwin environment.
* [PyUnsplash](https://github.com/salvoventura/pyunsplash) - An open source Python wrapper for the Unsplash [REST API](https://unsplash.com/developers).

## Authors

* **Andrey Mikhalev** - *Initial work* - [evilixy](https://github.com/evilixy)

## License

This project is licensed under the GPL - see the [LICENSE](LICENSE) file for details
import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import QtQuick.Layouts 1.11
import QtQuick.Dialogs 1.1

ApplicationWindow {
    id: wallpaperAppWindow
    width: 500
    height: 500
    visible: true
    title: 'Wallpaper changer'
    objectName: "wallpaperAppWindowObj"
    property string workingPath
    property string randomImagePath
    property bool isWallDownloaded

    Component.onCompleted: {
        wallpaperAppWindow.workingPath = wallpaper_app.get_working_path;
        wallpaperAppWindow.randomImagePath = wallpaper_app.get_random_image_path;
        currentImage.source = wallpaper_app.get_standart_image_path;
        wallpaperAppWindow.isWallDownloaded = false;
    }

    GridLayout {
        id: grid
        anchors.fill: parent
        rows: 12
        columns: 12
        property double colMulti: grid.width / grid.columns
        property double rowMulti: grid.height / grid.rows

        // get the right size of the element based on the size of the window
        function get_pref_width(item) {
            return colMulti * item.Layout.columnSpan;
        }

        function get_pref_height(item) {
            return rowMulti * item.Layout.rowSpan;
        }

        // first grid's row
        Image {
            id: currentImage
            objectName: "currentImage_object_name"
            Layout.rowSpan: 6
            Layout.columnSpan: 12
            Layout.row: 1
            Layout.column: 1
            Layout.preferredWidth: grid.get_pref_width(this)
            Layout.preferredHeight: grid.get_pref_height(this)
        }

        // second grid's row
        Label {
            id: currentWallpaperLabel
            horizontalAlignment: Text.AlignHCenter
            Layout.rowSpan: 1
            Layout.columnSpan: 12
            Layout.row: 7
            Layout.column: 1
            Layout.preferredWidth: grid.get_pref_width(this)
            Layout.preferredHeight: grid.get_pref_height(this)
            text: "Current wallpaper"
            font.pixelSize: 14
            font.bold: true
            color: "#FFFFFF"
        }

        // third grid's row
        RowLayout {
            Layout.rowSpan: 1
            Layout.columnSpan: 12
            Layout.row: 8
            Layout.column: 1
            Layout.preferredWidth: grid.get_pref_width(this)
            Layout.preferredHeight: grid.get_pref_height(this)
        
            Label {
                id: wallpaperChangeMethodLabel
                Layout.leftMargin: 10
                Layout.rightMargin: 5
                text: "Wallpaper change method:"
                font.pixelSize: 14
                font.bold: true
                color: "#FFFFFF"
            }

            ComboBox {
                id: wallpaperChangeMethodComboBox
                Layout.fillWidth: true
                Layout.leftMargin: 5
                Layout.rightMargin: 10
                currentIndex: 0
                model: ListModel {
                    id: wallpaperChangeMethodComboBoxItems
                    ListElement { text: "Unsplash" }
                    ListElement { text: "Folder" }
                }

                onCurrentIndexChanged: function toggleChooseFolderSection(){
                    if( this.currentIndex == 1 ) {
                        chooseFolderRowLayout.visible = true;
                        downloadWallpaperButton.visible = false;
                    } else {
                        chooseFolderRowLayout.visible = false;
                        downloadWallpaperButton.visible = true;
                    }
                }
            }
        }

        //fourth grid
        RowLayout {
            id: chooseFolderRowLayout
            Layout.rowSpan: 1
            Layout.columnSpan: 12
            Layout.row: 9
            Layout.column: 1
            Layout.preferredWidth: grid.get_pref_width(this)
            Layout.preferredHeight: grid.get_pref_height(this)
            visible: false

            Label {
                id: chooseFolderLabel
                Layout.leftMargin: 10
                Layout.rightMargin: 5
                text: "Choose a folder:"
                font.pixelSize: 14
                font.bold: true
                color: "#FFFFFF"
            }

            TextField {
                id: chooseFolderTextField
                Layout.fillWidth: true
                Layout.leftMargin: 5
                Layout.rightMargin: 10
                validator: RegExpValidator { regExp: /\S+/ }

                MouseArea {
                    anchors.fill: parent
                    onClicked: chooseFolderFileDialog.open()
                }
            }

            FileDialog {
                id: chooseFolderFileDialog
                selectFolder: true
                onAccepted: {
                    chooseFolderTextField.text = chooseFolderFileDialog.fileUrl;
                }
            }
        }

        // fouth grid's row
        RowLayout {
            Layout.rowSpan: 1
            Layout.columnSpan: 12
            Layout.row: 10
            Layout.column: 1
            Layout.preferredWidth: grid.get_pref_width(this)
            Layout.preferredHeight: grid.get_pref_height(this)

            Label {
                id: chooseIntervalLabel
                Layout.leftMargin: 10
                Layout.rightMargin: 5
                text: "Choose interval:"
                font.pixelSize: 14
                font.bold: true
                color: "#FFFFFF"
            }

            TextField {
                id: chooseIntervalTextField
                Layout.fillWidth: true
                Layout.rightMargin: 5
                Layout.leftMargin: 5
                validator: RegExpValidator { regExp: /[0-9]+/ }
            }

            ComboBox {
                id: chooseIntervalComboBox
                Layout.fillWidth: true
                Layout.rightMargin: 10
                Layout.leftMargin: 5
                currentIndex: 0
                textRole: "text"
                model: ListModel {
                    id: chooseIntervalComboBoxItems
                    ListElement { text: "Minutes"; value: "M" }
                    ListElement { text: "Hours"; value: "H" }
                    ListElement { text: "Days"; value: "D" }
                }
                onCurrentIndexChanged: console.debug(chooseIntervalComboBoxItems.get(chooseIntervalComboBox.currentIndex).value)
            }
        }

        // fifth grid's row
        RowLayout {
            Layout.rowSpan: 1
            Layout.columnSpan: 12
            Layout.row: 11
            Layout.column: 1
            Layout.preferredWidth: grid.get_pref_width(this)
            Layout.preferredHeight: grid.get_pref_height(this)

            Button {
                id: downloadWallpaperButton
                Layout.leftMargin: 10
                Layout.rightMargin: 5
                Layout.fillWidth: true
                objectName: "downloadWallpaperObjName"
                property string toolTipTextDownloadWallpaper: qsTr("Download new wallpaper from Unsplash")
                text: qsTr("Download wallpaper")
                ToolTip.visible: toolTipTextDownloadWallpaper ? mouseAreaForTooltip.containsMouse: false
                ToolTip.text: toolTipTextDownloadWallpaper

                MouseArea {
                    id: mouseAreaForTooltip
                    anchors.fill: parent
                    hoverEnabled: true
                    // disable mouse interaction
                    onPressed: mouse.accepted = false;
                    onReleased: mouse.accepted = false;
                    onDoubleClicked: mouse.accepted = false;
                    onPositionChanged: mouse.accepted = false;
                    onPressAndHold: mouse.accepted = false;
                }

                onClicked: function downloadWallpaper() {
                    var is_image_downloaded = wallpaper_app.get_unsplash_wallpaper();
                    var downloadMessage = {};

                    if(is_image_downloaded) {
                        currentImage.source = "file:///" + randomImagePath;
                        wallpaperAppWindow.isWallDownloaded = true;

                        // get success downloaded message
                        downloadMessage = wallpaper_app.get_event_message("download_wall_success");    
                    } else {
                        // get failed downloaded message
                        downloadMessage = wallpaper_app.get_event_message("download_wall_failed");
                    }
                    
                    // do the log and show the result in the dialog message to the user
                    wallpaper_app.create_or_add_log(downloadMessage['message']);
                    customMessageDialog.setSource("CustomMessageDialog.qml", {"title_for_custom_message_dialog": downloadMessage['title'], "text_for_custom_message_dialog": downloadMessage['message'], "message_dialog_visible": true});
                }
            }

            Button {
                id: setWallpaperButton
                objectName: "setWallpaperBtnObj"
                Layout.rightMargin: 5
                Layout.leftMargin: 5
                Layout.fillWidth: true
                text: qsTr("Set wallpaper")
                ToolTip.visible: down
                ToolTip.text: qsTr("Change current wallpaper to the new wallpaper")

                enabled: ((wallpaperChangeMethodComboBox.currentText == 'Folder' && chooseFolderTextField.text != '') || (wallpaperChangeMethodComboBox.currentText == 'Unsplash') && wallpaperAppWindow.isWallDownloaded)

                function setWallpaper(currentMethod, fromPython=false) {
                    var folderData;
                    
                    if(currentMethod == 'Unsplash') {
                        wallpaper_app.set_desktop_background_wallpaper_for_windows(wallpaperAppWindow.randomImagePath);
                    } else {    
                        // if the func called from Python side
                        if(fromPython) {
                            var folderData = wallpaper_app.set_wall_from_folder();
                        } else {
                            var currentFolderPath = chooseFolderTextField.text;
                            var folderData = wallpaper_app.set_wall_from_folder(false, currentFolderPath);
                        }

                        if(folderData['path_exists']) {
                            // set wall in the app
                            currentImage.source = "file:///" + folderData['path'];
                        } // if the path was deleted or moved then delete the task from Task Scheduler and add log it
                        else if(folderData['path_exists'] === false && fromPython === true) {
                            var delete_result = wallpaper_app.delete_task_from_task_scheduler();
                            
                            if(delete_result) {
                                var deleteTaskSuccess = wallpaper_app.get_event_message('delete_task_success');                       
                                wallpaper_app.create_or_add_log(deleteTaskSuccess['message']);
                            } else {
                                var deleteTaskFailed = wallpaper_app.get_event_message('delete_task_failed');                       
                                wallpaper_app.create_or_add_log(deleteTaskFailed['message']);
                            }
                        }       
                    }
                            
                }
                onClicked: setWallpaper(wallpaperChangeMethodComboBox.currentText) 
            }

            Button {
                id: setTaskSchedulerButton
                Layout.rightMargin: 5
                Layout.leftMargin: 10
                Layout.fillWidth: true
                text: qsTr("Set Task schedule")
                ToolTip.visible: down
                ToolTip.text: qsTr("Set Task schedule to change the wallpaper")

                enabled: ((wallpaperChangeMethodComboBox.currentText == 'Folder' && chooseFolderTextField.text != '') || (wallpaperChangeMethodComboBox.currentText == 'Unsplash')) && chooseIntervalTextField.acceptableInput

                onClicked: function setTaskScheduler() {
                    
                    var currentMethod = wallpaperChangeMethodComboBox.currentText;

                    if(currentMethod == 'Folder') {
                        var currentFolderPath = chooseFolderTextField.text;
                        wallpaper_app.remember_folder_path(currentFolderPath);
                    }

                    // get value of time combobox
                    var timeUnit = chooseIntervalComboBoxItems.get(chooseIntervalComboBox.currentIndex).value;
                    var timeValue = chooseIntervalTextField.text;
                    var timeISO8601 = timeValue + timeUnit;

                    var taskCreatedSuccessfully = wallpaper_app.set_task_scheduler(timeISO8601, currentMethod);
                    var taskCreationMessage = {};

                    if(!taskCreatedSuccessfully) {
                        taskCreationMessage = wallpaper_app.get_event_message("create_task_failed");
                    } else {
                        taskCreationMessage = wallpaper_app.get_event_message("create_task_success"); 
                    }

                    customMessageDialog.setSource("CustomMessageDialog.qml", {"title_for_custom_message_dialog": taskCreationMessage['title'], "text_for_custom_message_dialog": taskCreationMessage['message'], "message_dialog_visible": true});
                    wallpaper_app.create_or_add_log(taskCreationMessage['message']);
                }
            }
        }
    }
    // custom message dialog (load only if it necessary)
    Loader {
        id: customMessageDialog
        objectName: "customMssageDialogObject"
        source: "CustomMessageDialog.qml"
    }
}
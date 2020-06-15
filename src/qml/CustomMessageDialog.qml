import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import QtQuick.Layouts 1.11
import QtQuick.Dialogs 1.1

Item {
    id: item_for_messsage_dialog
    property string title_for_custom_message_dialog: ""
    property string text_for_custom_message_dialog: ""
    property bool message_dialog_visible: false
    width: 100

    MessageDialog {
        id: custom_message_dialog
        icon: StandardIcon.Information
        title: item_for_messsage_dialog.title_for_custom_message_dialog
        text: item_for_messsage_dialog.text_for_custom_message_dialog
        visible: item_for_messsage_dialog.message_dialog_visible
        standardButtons: StandardButton.Ok
                
        onAccepted: {
            Qt.quit()
        }
    }
}
import QtQuick 
import QtQuick.Controls
import QtQuick.Layouts 
import Qt.labs.folderlistmodel

ApplicationWindow {
    id: main
    visible: true
    width: screen.width*.8; height: screen.height*.8
    //x: screen.desktopAvailableWidth - width - 12
    //y: screen.desktopAvailableHeight - height - 48
    title: "Image Viewer"
    //flags: Qt.FramelessWindowHint | Qt.Window
    signal move_folder (src: string, dst: string)
    signal move_file (src: string, dst: string)
    signal remove_file (src: string)
    property int i_user: 0
    property string folder_name: "file:" + Qt.application.arguments[1]

    GridView {
        id: gridview
        anchors.fill: parent
        anchors.horizontalCenter: parent.horizontalCenter
        cellWidth: 300; cellHeight: 400
        ScrollBar.vertical: ScrollBar { active: true }


        Dialog {
            id: goto_diag
            modal: true
            title: "Goto User:"
            height: 100
            width: 300
            standardButtons: Dialog.Ok | Dialog.Cancel
            anchors.centerIn: parent       

            TextField {
                id: n_go
                width: parent.width * 0.75
                focus: true
                anchors.horizontalCenter: parent.horizontalCenter
            }

            onAccepted: {
                var iu = parseInt(n_go.text)-1
                if (iu >= 0 && iu < user_list.count) {
                    i_user = iu
                    var f_url = user_list.get(i_user, "fileURL")
                    if (f_url == "_") {
                        i_user = i_user+increase
                        f_url = user_list.get(i_user, "fileURL")
                    }
                    msg.text = "Loading..."
                    img_list.folder = f_url
                    main.title = "Image Viewer " + "["+(i_user+1)+"/"+user_list.count+"] " + f_url
                }
            }
        }

        FolderListModel {
            id: user_list
            nameFilters: [""]
            showDirs: true
            showFiles: false
            showDirsFirst: true
            folder: folder_name
            sortField: "Name"
            caseSensitive: false
            sortCaseSensitive: false
            onStatusChanged: if (user_list.status == FolderListModel.Ready){
                var f_url=""
                if (user_list.count > 0)
                {
                    f_url = user_list.get(i_user, "fileURL")
                    if (f_url == "_")
                    {
                        i_user++
                        f_url = user_list.get(i_user, "fileURL")
                    }
                    msg.text = "Loading..."
                    img_list.folder = ""
                    img_list.folder = f_url
                    main.title = "Image Viewer " + "["+(i_user+1)+"/"+user_list.count+"] " + f_url
                }
            }
        }

        FolderListModel {
            id: img_list
            nameFilters: ["*.jpg", "*.png"]
            showDirs: false
            showFiles: true
            folder: user_list.count>0?user_list.get(i_user, "FileURL"):""
            sortField: "Time"
            sortReversed: true
            onStatusChanged: if (img_list.status == FolderListModel.Ready) {
                msg.text = img_list.folder + "["+img_list.count+"]"
                //gridview.visible = true
                bi.running = false
            }
        }

        Component {
            id: img_delegate
            Loader {
                source: switch(fileSuffix){
                    case "jpg": return "image.qml"
                    case "png": return "image.qml"
                    //case "mp4": return "video.qml"
                }
            }
        }

        model: img_list
        delegate: img_delegate
        focus: true
        Keys.onPressed: (event) => {
            switch(event.key){
                case Qt.Key_QuoteLeft:
                    move_user(i_user, 'l0')
                    break
                case Qt.Key_1:
                    move_user(i_user, 'l1')
                    break
                case Qt.Key_2:
                    move_user(i_user, 'l2')
                    break
                case Qt.Key_3:
                    move_user(i_user, 'block')
                    break
                case Qt.Key_4:
                    //action.text = "4"
                    break
                case Qt.Key_Left:
                    update_imglist(-1)
                    break
                case Qt.Key_Right:
                case Qt.Key_Space:
                case Qt.Key_Enter:
                    update_imglist(1)
                    break
            }
        }

        function move_user(i_user, new_level){
            bi.running = true
            var t_msg = "Moving "+user_list.get(i_user, "fileName")+" to "+new_level
            msg.text = t_msg
            action.text = "Move"
            var file_path = user_list.get(i_user, "filePath")
            var file_name = user_list.get(i_user, "fileName")
            //update_imglist(1)
            move_file(file_path+"/../_/"+file_name+".html", file_path+"/../../"+new_level+"/_/"+file_name+".html")
            move_folder(file_path, file_path+"/../../"+new_level+"/"+file_name)
            update_userlist()
        }

        function update_imglist(increase) {
            var f_url=""
            if (user_list.count > 0)
            {
                i_user = i_user + increase
                if (i_user >= user_list.count) {
                    i_user=user_list.count-1
                    return
                }
                if (i_user <0 ) {
                    i_user=0
                    return
                }
                f_url = user_list.get(i_user, "fileURL")
                if (f_url == "_") {
                    i_user = i_user+increase
                    f_url = user_list.get(i_user, "fileURL")
                }
                //gridview.visible = false
                bi.running = true
                msg.text = "Loading..."
                img_list.folder = f_url
                main.title = "Image Viewer " + "["+(i_user+1)+"/"+user_list.count+"] " + f_url
            }
        }

        function update_userlist() {
            bi.running = true
            user_list.folder = ""
            user_list.folder = folder_name
        }
    }

    menuBar: MenuBar {
        Menu {
            id: menu
            title: qsTr("&File")
            Action { text: qsTr("&New...") }
            Action { text: qsTr("&Open...") }
            Action { text: qsTr("&Save") }
            Action { text: qsTr("Save &As...") }
            MenuSeparator { }
            Action { text: qsTr("&Quit") }
        }
        Menu {
            title: qsTr("&Edit")
            Action { text: qsTr("Cu&t") }
            Action { text: qsTr("&Copy") }
            Action { text: qsTr("&Paste") }
            MenuItem {
                text: qsTr("Goto")
                onTriggered: goto_diag.open()
            }
        }
        Menu {
            title: qsTr("&Help")
            Action { text: qsTr("&About") }
        }
    }

    footer: ToolBar {
        id: footbar
        RowLayout {
            anchors.fill: parent
            ToolButton {
                text: qsTr("‹")
                onClicked: stack.pop()
            }
            Label {
                id: msg
                text: "Title"
                elide: Label.ElideRight
                horizontalAlignment: Qt.AlignHLeft
                verticalAlignment: Qt.AlignVCenter
                Layout.fillWidth: true
            }
            Label {
                id: action
                text: "action"
                elide: Label.ElideRight
                horizontalAlignment: Qt.AlignHLeft
                verticalAlignment: Qt.AlignVCenter
                width: 300
            }
            ToolButton {
                text: qsTr("⋮")
                onClicked: menu.open()
            }
        }
    }
            BusyIndicator {
        id: bi
        width: 100
        height: 100
        anchors.centerIn: parent
        running: true
        
    }


}

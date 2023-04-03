import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
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

        FolderListModel {
            id: user_list
            nameFilters: [""]
            showDirs: true
            showFiles: false
            showDirsFirst: true
            folder: folder_name
            sortField: "Name"
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
            nameFilters: ["*.jpg", "*.png", "*.mp4"]
            showDirs: false
            showFiles: true
            folder: user_list.count>0?user_list.get(i_user, "FileURL"):""
            sortField: "Time"
            sortReversed: true
            onStatusChanged: if (img_list.status == FolderListModel.Ready) {
                msg.text = img_list.folder + "["+img_list.count+"]"
            }
        }

        Component {
            id: img_delegate
            Loader {
                source: switch(fileSuffix){
                    case "jpg": return "image.qml"
                    case "png": return "image.qml"
                    case "mp4": return "video.qml"
                }
            }
        }

        model: img_list
        delegate: img_delegate
        BusyIndicator {
            running: gridview.status == Loader.Loading
            anchors.centerIn: parent
        }

        focus: true
        Keys.onPressed: (event) => {
            switch(event.key){
                case Qt.Key_QuoteLeft:
                    action.text = "Move "+user_list.get(i_user, "fileName")+" to l0"
                    move_file(user_list.get(i_user, "filePath")+"/../_/"+user_list.get(i_user, "fileName")+".html", user_list.get(i_user, "filePath")+"/../../l0/_/"+user_list.get(i_user, "fileName")+".html")
                    move_folder(user_list.get(i_user, "filePath"), user_list.get(i_user, "filePath")+"/../../l0/"+user_list.get(i_user, "fileName"))
                    update_userlist()
                    break
                case Qt.Key_1:
                    action.text = "Move "+user_list.get(i_user, "fileName")+" to l1"
                    move_file(user_list.get(i_user, "filePath")+"/../_/"+user_list.get(i_user, "fileName")+".html", user_list.get(i_user, "filePath")+"/../../l1/_/"+user_list.get(i_user, "fileName")+".html")
                    move_folder(user_list.get(i_user, "filePath"), user_list.get(i_user, "filePath")+"/../../l1/"+user_list.get(i_user, "fileName"))
                    update_userlist()
                    break
                case Qt.Key_2:
                    action.text = "Move "+user_list.get(i_user, "fileName")+" to l2"
                    move_file(user_list.get(i_user, "filePath")+"/../_/"+user_list.get(i_user, "fileName")+".html", user_list.get(i_user, "filePath")+"/../../l2/_/"+user_list.get(i_user, "fileName")+".html")
                    move_folder(user_list.get(i_user, "filePath"), user_list.get(i_user, "filePath")+"/../../l2/"+user_list.get(i_user, "fileName"))
                    update_userlist()
                    break
                case Qt.Key_3:
                    action.text = "Move "+user_list.get(i_user, "fileName")+" to block"
                    move_file(user_list.get(i_user, "filePath")+"/../_/"+user_list.get(i_user, "fileName")+".html", user_list.get(i_user, "filePath")+"/../../block/_/"+user_list.get(i_user, "fileName")+".html")
                    move_folder(user_list.get(i_user, "filePath"), user_list.get(i_user, "filePath")+"/../../block/"+user_list.get(i_user, "fileName"))
                    update_userlist()
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
                msg.text = "Loading..."
                img_list.folder = f_url
                main.title = "Image Viewer " + "["+(i_user+1)+"/"+user_list.count+"] " + f_url
            }
        }

        function update_userlist() {
            user_list.folder = ""
            user_list.folder = folder_name
        }
    }

    BusyIndicator {
        id: bi
        width: 100
        height: 100
        anchors.centerIn: parent
        running: img_list.status == FolderListModel.Loading
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
}

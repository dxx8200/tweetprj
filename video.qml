import QtQuick 2.15
import QtQuick.Controls 2.15
import QtMultimedia 5.15

Column {

    Video {
        id: video
        width : 300
        height : 380
        source: fileURL
        loops: 99999
        muted: true

        anchors.horizontalCenter: parent.horizontalCenter
        MouseArea {
            anchors.fill: parent
            onClicked: {
                video.play()
            }
        }

        Component.onCompleted: {
            video.play()
            msg.text = img_list.folder + "["+img_list.count+"]"
        }

        Keys.onSpacePressed: video.playbackState == MediaPlayer.PlayingState ? video.pause() : video.play()
        Keys.onLeftPressed: video.seek(video.position - 5000)
        Keys.onRightPressed: video.seek(video.position + 5000)
    }
    Text {
        text: fileName;
        anchors.horizontalCenter: parent.horizontalCenter
        y: 380
    }

}
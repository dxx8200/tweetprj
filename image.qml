import QtQuick 2.15
import QtQuick.Controls 2.15

Column {

    Image {
        width: 300; height: 380
        fillMode: Image.PreserveAspectFit
        smooth: true
        source: fileURL
        anchors.horizontalCenter: parent.horizontalCenter
    }
    Text { 
        text: fileName; 
        anchors.horizontalCenter: parent.horizontalCenter
        y: 380
    }

}
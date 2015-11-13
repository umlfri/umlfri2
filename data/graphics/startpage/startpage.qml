import QtQuick 2.0
import QtQuick.Layouts 1.2

Rectangle {
    width: 800;
    height: 600;/*/
    anchors.fill: parent;/**/
    clip: true;
    color: "#D0D0FF";

    Image {
        anchors.top: parent.top;
        anchors.left: parent.left;
        source: "startpage.png"
    }

    Text {
        text: "UML";
        x: 150;
        y: 50;
        font.pointSize: 40;
        font.family: "Arial";
        color: "white";
        style: Text.Outline;
        styleColor: "#8000243E";
    }

    Text {
        text: ".FRI";
        x: 270;
        y: 65;
        font.pointSize: 25;
        font.family: "Arial";
        color: "white";
        style: Text.Outline;
        styleColor: "#8000243E";
    }

    Text {
        text: "2.0";
        x: 360;
        y: 65;
        font.pointSize: 25;
        font.family: "Arial";
        font.bold: true
        color: "white";
        style: Text.Outline;
        styleColor: "#8000243E";
    }

    Rectangle {
        anchors.top: parent.top;
        anchors.topMargin: 200;
        anchors.right: parent.horizontalCenter;
        anchors.rightMargin: 20;
        width: 250;
        height: 150;
        border.color: "#8000243E";
        border.width: 2;
        color: "#200000FF";
        radius: 15;

        GridLayout {
            anchors.fill: parent;
            anchors.leftMargin: 20;
            anchors.rightMargin: 20;

            rows: 3;
            columns: 1;

            Text {
                text: "Create New Project...";
                font.pixelSize: 15;
            }

            Text {
                text: "Open Project...";
                font.pixelSize: 15;
            }

            Text {
                text: "About UML .FRI...";
                font.pixelSize: 15;
            }
        }
    }

    Rectangle {
        anchors.top: parent.top;
        anchors.topMargin: 200;
        anchors.left: parent.horizontalCenter;
        anchors.leftMargin: 20;
        width: 250;
        height: 150;
        border.color: "#8000243E";
        border.width: 2;
        color: "#200000FF";
        radius: 15;
    }
}

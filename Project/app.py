import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QMessageBox

import os
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "D:/융시공/3학년 2학기/Ajou_SocialNetworkAnalysis/Project/Lib/site-packages/PyQt5/Qt5/plugins"


artists = ['ArianaGrande.csv',
 'Beyonce.csv',
 'BillieEilish.csv',
 'BTS.csv',
 'CardiB.csv',
 'CharliePuth.csv',
 'ColdPlay.csv',
 'Drake.csv',
 'DuaLipa.csv',
 'EdSheeran.csv',
 'Eminem.csv',
 'JustinBieber.csv',
 'KatyPerry.csv',
 'Khalid.csv',
 'LadyGaga.csv',
 'Maroon5.csv',
 'NickiMinaj.csv',
 'PostMalone.csv',
 'Rihanna.csv',
 'SelenaGomez.csv',
 'TaylorSwift.csv']

class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.checkboxes = []
        for artist in artists:
            checkbox = QCheckBox(artist, self)
            self.checkboxes.append(checkbox)
            layout.addWidget(checkbox)
        
        self.button = QPushButton('Enter', self)
        self.button.clicked.connect(self.show_selected_artists)
        layout.addWidget(self.button)


        self.setLayout(layout)
        self.setWindowTitle('Music Recommend App')
        self.setGeometry(100,100,300,200)
        self.show()

    def show_selected_artists(self):
        selected_artists = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
        artist_list = ", ".join(selected_artists)
        QMessageBox.information(self, "Selected Artists",f"The selected artists are: {artist_list}")
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SimpleApp()
    sys.exit(app.exec_())
# PROJECT APP YOUTUBE DOWNLOADER - by LEANDRO CARDOSO
# https://github.com/Leandro-Cardoso/APP-YouTube-Downloader

from pytube import YouTube, Playlist

def downloadYoutubeVideo(url, isOnlyAudio = False):
    '''Download a YouTube video or only audio.'''
    if isOnlyAudio:
        YouTube(url).streams.filter(only_audio=True)[0].download('downloads/audios')
    else:
        YouTube(url).streams.get_highest_resolution().download('downloads/videos')

def downloadYoutubePlaylist(playlist, isOnlyAudio = False):
    '''Download a YouTube playlist video or only audio.'''
    playlist = Playlist(playlist)
    for url in playlist:
        downloadYoutubeVideo(url, isOnlyAudio)

def downloadYoutubeLinks(links, isOnlyAudio = False):
    '''Download a YouTube link list (videos and playlists, in video format or audio)'''
    for link in links:
        if 'list' in link:
            downloadYoutubePlaylist(link, isOnlyAudio)
        else:
            downloadYoutubeVideo(link, isOnlyAudio)

# INTERFACE:

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QToolTip, QLabel, QLineEdit, QListWidget, QCheckBox
from PyQt5.QtCore import Qt

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.top = 100
        self.left = 100
        self.width = 1024
        self.height = 720
        self.title = 'YouTube Downloader'

        self.linksList = QListWidget(self)
        self.linksList.move(50, 50)
        self.linksList.resize(self.width / 2 - 60, self.height - 350)
        self.linksList.setStyleSheet('QListWidget {background-color: #999999; color: #ffffff}')
        self.linksList.clicked.connect(self.selectLinkClick)

        self.clearListButton = QPushButton('Clear List', self)
        self.clearListButton.move(50, self.height - 300)
        self.clearListButton.resize((self.width / 2 - 60) / 2, 30)
        self.clearListButton.setStyleSheet('QPushButton {background-color: #B55555; color: #ffffff; font: bold; font-size: 12px} QPushButton:hover {background-color: #FF0000; color: #000000}')
        self.clearListButton.clicked.connect(self.clearListButtonClick)

        self.addLinkButton = QPushButton('Remove Link', self)
        self.addLinkButton.move((self.width / 2 - 60) / 2 + 50, self.height - 300)
        self.addLinkButton.resize((self.width / 2 - 60) / 2, 30)
        self.addLinkButton.setStyleSheet('QPushButton {background-color: #B55555; color: #ffffff; font: bold; font-size: 12px} QPushButton:hover {background-color: #FF0000; color: #000000}')
        self.addLinkButton.clicked.connect(self.removeLinkButtonClick)

        self.addLinkTextBox = QLineEdit(self)
        self.addLinkTextBox.move(50, self.height - 250)
        self.addLinkTextBox.resize(self.width - 300, 30)
        self.addLinkTextBox.setStyleSheet('QLineEdit {background-color: #888888; color: #ffffff; border: 0}')

        self.addLinkButton = QPushButton('Add Link', self)
        self.addLinkButton.move(self.width - 250, self.height - 250)
        self.addLinkButton.resize(200, 30)
        self.addLinkButton.setStyleSheet('QPushButton {background-color: #6B8E23; color: #ffffff; font: bold; font-size: 12px} QPushButton:hover {background-color: #00FF00; color: #000000}')
        self.addLinkButton.clicked.connect(self.addLinkButtonClick)

        self.feedbackLabel = QLabel(self)
        self.feedbackLabel.setText('Crie uma lista de links para download.')
        self.feedbackLabel.move(50, self.height - 200)
        self.feedbackLabel.resize(self.width - 100, 100)
        self.feedbackLabel.setStyleSheet('QLabel {color: #888888; font: bold; font-size: 20px}')
        self.feedbackLabel.setAlignment(Qt.AlignCenter)

        self.onlyAudioCheckbox = QCheckBox(self)
        self.onlyAudioCheckbox.setText('Only audio.')
        self.onlyAudioCheckbox.move(self.width / 2 + 120, self.height - 75)
        self.onlyAudioCheckbox.resize(200, 50)
        self.onlyAudioCheckbox.setStyleSheet('QCheckBox {color: #FF2222; font: bold; font-size: 14px}')

        downloadButton = QPushButton('Download', self)
        downloadButton.move(self.width / 2 - 100, self.height - 75)
        downloadButton.resize(200, 50)
        downloadButton.setStyleSheet('QPushButton {background-color: #000000; color: #ffffff; font: bold; font-size: 24px} QPushButton:hover {background-color: #B22222; color: #000000}')
        downloadButton.clicked.connect(self.downloadButtonClick)

        self.loadWindow()

    def loadWindow(self):
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setStyleSheet('QMainWindow {background-color: #111111}')
        self.show()

    def addLinkButtonClick(self):
        isDuplicate = False
        if len(self.linksList) > 0:
            for i in range(0, len(self.linksList)):
                if self.linksList.item(i).text() == self.addLinkTextBox.text():
                    isDuplicate = True
        if self.addLinkTextBox.text() == '':
            self.feedbackLabel.setText('Plaste a YouTube link to add...')
        elif 'youtube.com' not in self.addLinkTextBox.text() and 'youtu.be' not in self.addLinkTextBox.text():
            self.feedbackLabel.setText('Plaste only a valid YouTube link to add...')
        elif isDuplicate:
            self.feedbackLabel.setText('This link is duplicate. Plaste other YouTube link to add...')
        else:
            self.feedbackLabel.setText('"' + self.addLinkTextBox.text() + '" is added...')
            self.linksList.addItem(self.addLinkTextBox.text())
        self.addLinkTextBox.clear()
        self.addLinkTextBox.setFocus()

    def selectLinkClick(self):
        self.addLinkTextBox.setText(self.linksList.currentItem().text())
        self.feedbackLabel.setText('"' + self.linksList.currentItem().text() + '" is selected...')
    
    def removeLinkButtonClick(self):
        if self.addLinkTextBox.text() != '':
            self.feedbackLabel.setText('"' + self.linksList.currentItem().text() + '" is removed...')
            self.linksList.takeItem(self.linksList.currentRow())
            self.linksList.clearSelection()
            self.addLinkTextBox.clear()
            self.addLinkTextBox.setFocus()
        else:
            self.feedbackLabel.setText('Select or plaste a YouTube link to remove...')

    def clearListButtonClick(self):
        self.linksList.clear()
        self.addLinkTextBox.clear()
        self.addLinkTextBox.setFocus()
        self.feedbackLabel.setText('List cleaned...')

    def downloadButtonClick(self):
        self.feedbackLabel.setText('Downloading list...')
        downloadList = []
        for i in range(0, len(self.linksList)):
            downloadList.append(self.linksList.item(i).text())
        self.linksList.clear()
        if self.onlyAudioCheckbox.isChecked():
            downloadYoutubeLinks(downloadList, True)
        else:
            downloadYoutubeLinks(downloadList, False)
        self.feedbackLabel.setText('Complete download...')

app = QApplication(sys.argv)
MainWindow = Window()
sys.exit(app.exec_())

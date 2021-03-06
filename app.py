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
    urls = Playlist(playlist).video_urls
    print(urls)
    for url in urls:
        downloadYoutubeVideo(url, isOnlyAudio)

# INTERFACE:

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QListWidget, QCheckBox, QProgressBar, QShortcut
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.top = 100
        self.left = 100
        self.width = 1024
        self.height = 720
        self.title = 'YouTube Downloader'
        self.downloadProgress = 0

        # HOTKEYS:
        self.shortcutEsc = QShortcut(QKeySequence('Esc'), self)
        self.shortcutEsc.activated.connect(lambda x:app.quit())
        self.shortcutReturn = QShortcut(QKeySequence('Return'), self)
        self.shortcutReturn.activated.connect(self.addLinkButtonClick)
        self.shortcutEnter = QShortcut(QKeySequence('Enter'), self)
        self.shortcutEnter.activated.connect(self.addLinkButtonClick)
        self.shortcutDelete = QShortcut(QKeySequence('Delete'), self)
        self.shortcutDelete.activated.connect(self.removeLinkButtonClick)
        self.shortcutDel = QShortcut(QKeySequence(','), self)
        self.shortcutDel.activated.connect(self.removeLinkButtonClick)

        self.linksList = QListWidget(self)
        self.linksList.move(50, 50)
        self.linksList.resize(self.width - 100, self.height - 350)
        self.linksList.setStyleSheet('QListWidget {background-color: #FFDAB9; color: #FF0000; border-top-left-radius: 30px; padding: 10px; border-top-right-radius: 30px; font: bold; font-size: 12px; border: 5px solid #ffffff}')
        self.linksList.clicked.connect(self.selectLinkClick)

        self.clearListButton = QPushButton('Clear List', self)
        self.clearListButton.move(50, self.height - 300)
        self.clearListButton.resize((self.width - 100) / 2, 30)
        self.clearListButton.setStyleSheet('QPushButton {background-color: #B22222; color: #ffffff; font: bold; font-size: 12px; border-bottom-left-radius: 30px} QPushButton:hover {background-color: #FF0000}')
        self.clearListButton.clicked.connect(self.clearListButtonClick)

        self.addLinkButton = QPushButton('Remove Link', self)
        self.addLinkButton.move((self.width - 100) / 2 + 50, self.height - 300)
        self.addLinkButton.resize((self.width - 100) / 2 , 30)
        self.addLinkButton.setStyleSheet('QPushButton {background-color: #B22222; color: #ffffff; font: bold; font-size: 12px; border-bottom-right-radius: 30px} QPushButton:hover {background-color: #FF0000}')
        self.addLinkButton.clicked.connect(self.removeLinkButtonClick)

        self.addLinkTextBox = QLineEdit(self)
        self.addLinkTextBox.move(50, self.height - 250)
        self.addLinkTextBox.resize(self.width - 300, 30)
        self.addLinkTextBox.setStyleSheet('QLineEdit {background-color: #ffffff; color: #000000; border-top-left-radius: 15px; border-bottom-left-radius: 15px; padding-left: 10px; font: bold; font-size: 12px}')
        self.addLinkTextBox.setFocus()

        self.addLinkButton = QPushButton('Add Link', self)
        self.addLinkButton.move(self.width - 250, self.height - 250)
        self.addLinkButton.resize(200, 30)
        self.addLinkButton.setStyleSheet('QPushButton {background-color: #6B8E23; color: #ffffff; font: bold; font-size: 12px; border-top-right-radius: 15px; border-bottom-right-radius: 15px} QPushButton:hover {background-color: #00FF00}')
        self.addLinkButton.clicked.connect(self.addLinkButtonClick)

        self.feedbackLabel = QLabel(self)
        self.feedbackLabel.setText('Paste a YouTube link...')
        self.feedbackLabel.move(50, self.height - 200)
        self.feedbackLabel.resize(self.width - 100, 100)
        self.feedbackLabel.setStyleSheet('QLabel {color: #6B8E23; font: bold; font-size: 20px}')
        self.feedbackLabel.setAlignment(Qt.AlignCenter)

        self.progressBar = QProgressBar(self)
        self.progressBar.move(0, self.height - 15)
        self.progressBar.resize(self.width, 15)
        self.progressBar.setValue(self.downloadProgress)
        self.progressBar.setStyleSheet('QProgressBar {background-color: #BDB76B; color: #000000; font: bold; font-size: 14px; text-align: center}')

        downloadButton = QPushButton('Download', self)
        downloadButton.move(self.width / 2 - 100, self.height - 75)
        downloadButton.resize(200, 50)
        downloadButton.setStyleSheet('QPushButton {background-color: #6B8E23; color: #ffffff; font: bold; font-size: 24px; border-radius: 25px} QPushButton:hover {background-color: #00FF00}')
        downloadButton.clicked.connect(self.downloadButtonClick)

        self.onlyAudioCheckbox = QCheckBox(self)
        self.onlyAudioCheckbox.setText('Only audio.')
        self.onlyAudioCheckbox.move(self.width / 2 + 150, self.height - 75)
        self.onlyAudioCheckbox.resize(200, 50)
        self.onlyAudioCheckbox.setStyleSheet('QCheckBox {color: #FF2222; font: bold; font-size: 14px}')

        self.loadWindow()

    def loadWindow(self):
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)
        self.setWindowTitle(self.title)
        self.setStyleSheet('QMainWindow {background-color: #BDB76B}')
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
        self.resetProgressBar()
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

    def createDownloadList(self):
        downloadList = []
        for i in range(0, len(self.linksList)):
            downloadList.append(self.linksList.item(i).text())
        return downloadList

    def increaseProgressBar(self):
        self.downloadProgress += 100 / len(self.linksList)
        self.progressBar.setValue(self.downloadProgress)

    def resetProgressBar(self):
        self.downloadProgress = 0
        self.progressBar.setValue(self.downloadProgress)

    def downloadButtonClick(self):
        downloadList = self.createDownloadList()
        for link in downloadList:
            if self.onlyAudioCheckbox.isChecked():
                if 'playlist' in link:
                    downloadYoutubePlaylist(link, True)
                else:
                    downloadYoutubeVideo(link, True)
            else:
                if 'playlist' in link:
                    downloadYoutubePlaylist(link, False)
                else:
                    downloadYoutubeVideo(link, False)
            self.increaseProgressBar()
        self.linksList.clear()
        self.feedbackLabel.setText('Download complete...')

app = QApplication(sys.argv)
MainWindow = Window()
sys.exit(app.exec_())

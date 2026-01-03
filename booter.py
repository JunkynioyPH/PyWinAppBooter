from PyQt6.QtWidgets import *
from PyQt6.QtCore import QFileInfo, Qt, QTimer
from PyQt6.QtGui import QAbstractFileIconProvider
import os, sys, json

APP = QApplication([])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Modifiable Space
        Canvas = QWidget(self) 
        self.setCentralWidget(Canvas)
        # self.setFixedSize(960,540)
        # self.setMinimumSize(1000,770)
        # self.setMaximumSize(0,0)
        
        # Main Modifiable Space
        VCanvas = QVBoxLayout()
        Canvas.setLayout(VCanvas)
        
        # Top Bar 
        TopBar = QHBoxLayout()
        VCanvas.addLayout(TopBar)
        TopBar.addLayout(self.topBarContent())
        self.navTextBar.setPlaceholderText('Enter a path to scan...')
        self.navTextBar.returnPressed.connect(self._refreshDisplay)
        # self.navTextBar.setText('poggers')
        
        # Main Body
        self.bodyGroup = QGroupBox(" Applications ")
        VCanvas.addWidget(self.bodyGroup)
        self.bodyContainer = QHBoxLayout()
        self.bodyGroup.setLayout(self.bodyContainer)
        
        self.showFullScreen()
        self.setFixedSize(self.size())
        
        self._appsDisplay() # if self.navTextBar.text() != '' else ''

        
    def _appsDisplay(self):
        self.tabPages = QTabWidget()
        self.bodyContainer.addWidget(self.tabPages)
        self.applistContent()
        
    def _refreshDisplay(self):
        try:
            self.bodyContainer.removeWidget(self.tabPages)
            print('[Re-Scan] Clearing')
        except AttributeError:
            print('[Re-Scan] No Tabs to clear')
            
        self._appsDisplay()
        print('[Re-Scan] Re-Index\'d')
        
    def topBarContent(self):
        Layout = QHBoxLayout()
        # Main 
        refresh = QPushButton('Re/Scan')
        refresh.clicked.connect(self._refreshDisplay)
        exit = QPushButton('Exit')
        exit.clicked.connect(sys.exit)
        navBar = QVBoxLayout()
        self.navTextBar = QLineEdit()
        self.navTextBar.setFixedHeight(25)
        navBar.addWidget(self.navTextBar)
        
        Layout.addWidget(exit)
        Layout.addLayout(navBar) # Might change to just add widget, not add layout, i did this thinking i'd add another widget.
        Layout.addWidget(refresh)
        
        # currentPath = QTimer(self)
        # currentPath.setInterval(125)
        # # currentPath.timeout.connect()
        
        Layout.addStretch()
        return Layout
    
    def applistContent(self):
        # ## NOTE: i just need to add refresh logic and add path-change logic aswell
        
        def currentDir(paths:str):
            return os.path.join(self.path,paths)
        def addAppX():
            XContents.addWidget(self.appButton(appPath, (92,68), self.launcher))
            print("[Adding]", index, appPath)
        def newPage():
            # Container
            pageCanvas = QWidget()
            # Each Complete Row
            pageVContents = QVBoxLayout()
            # Each Item Listed
            pageHContents = QHBoxLayout()
            
            # Add Contents to Container
            pageCanvas.setLayout(pageVContents)
            # pageVContents.addStretch()
            pageVContents.addLayout(pageHContents)
            pageHContents.addStretch()
            return pageCanvas, pageVContents, pageHContents
        
        Container, YContents, XContents = newPage()
        tabIndex = 0
        showHidden = False
        navBarPath = self.navTextBar.text()
        self.navTextBar.setText('.\\') if self.navTextBar.text() == '' else 'TODO: set to prev path'
        self.path = "./" if navBarPath == '' else navBarPath
        
        # TODO: Add Path Address bar + Show Hidden
        
        ##################### THE INDEX STARTS ON INDEX 0 ############################
        ### Unsure how to keep this uniform for all resolutions,
        ###  however this is tuned specifically for 1920x1080.
        ###
        ### Though, tested on windowed mode, diff resolutions, it displays well enough.
        ##############################################################################
        index:dict[list[int], int] = {
            "x":[0,(self.width() // 97)],
            "y":[0,(self.height() // 90)]
            }
                
        if os.path.exists(currentDir('.hidden')):
            with open(os.path.join(self.path,'.hidden'), 'r') as file:
                global hiddenList
                hiddenList = file.readlines()
                for name in hiddenList:
                    if not name.endswith('\n'): continue
                    hiddenList[hiddenList.index(name)] = name.removesuffix('\n')
                print(hiddenList)
        else:
            hiddenList = []
        
        self.path = '.\\' if not os.path.exists(self.path) or not os.path.isdir(self.path) else self.path
        self.navTextBar.setText('.\\') if self.path == '.\\' else ''
        appList = os.listdir(self.path)
        # # Total (285 - 19) icons @ 1080p
        for app in appList:
            appPath = os.path.join(self.path, app)
            # loose, .hidden w/ or w/o .extension
            if app.startswith('.') or app.split('.')[0] in hiddenList or app in hiddenList:
                if not showHidden: 
                    print(f"[Hidden] skip {appPath}")
                    continue
            if os.path.isfile(appPath):
                if index.get('x')[0] < index.get('x')[1]:
                    addAppX()
                    index.get('x')[0] += 1
                elif index.get('y')[0] < index.get('y')[1]:
                    index.get('y')[0] += 1
                    XContents.addStretch()
                    XContents = QHBoxLayout()
                    XContents.addStretch()
                    YContents.addLayout(XContents)
                    addAppX()
                    ####################### BUT IT STARTS ON INDEX 1 ON A NEW ROW ######################
                    ##################### THIS BUGS THE SHIT OUT OF ME #################################
                    ## BUT MY GUI LOOKS FINE AND ALL ALIGNED AND NO EXCESS BUTTONS ADDED OR LOST #######
                    index.get('x')[0] = 1
                    print(f'[New Line] {index}')
                else:
                    YContents.addStretch()
                    XContents.addStretch()
                    self.tabPages.addTab(Container,f'Apps_{tabIndex}')
                    tabIndex += 1
                    index.get('x')[0] = 1
                    index.get('y')[0] = 0
                    Container, YContents, XContents = newPage()
                    self.tabPages.addTab(Container,f'Apps_{tabIndex}')
                    print(f'[New Tab] {appPath} {index}')
                    addAppX()
        else:
            print(f'[Adding] Incomplete Tab y:{index.get('y')}') if index.get('y')[0] < index.get('y')[1] else print(f'[Adding] Nice y:{index.get('y')}')
            XContents.addStretch() if index.get('y')[0] < index.get('y')[1] else ''
            self.tabPages.addTab(Container,f'Apps_{tabIndex}') if index.get('y')[0] < index.get('y')[1] else print(f'[Adding] Complete Tab y:{index.get('y')}')
            YContents.addStretch()
            print('[Finish]')
            # self.tabPages.addTab(Container,'Test')
                    
    def appButton(self, path: str, geometry: tuple, callback) -> QPushButton:
        x, y = geometry
        path = os.path.abspath(path)
        button = QPushButton(self)
        button.setFixedSize(x, y)
        button.setStyleSheet("QPushButton {padding: 0px}")
        layout = QVBoxLayout(button)
        layout.setContentsMargins(7, 7, 7, 7)
        layout.setSpacing(2)
        button.setLayout(layout)
        
        icon = QLabel()
        icon.setPixmap(QAbstractFileIconProvider().icon(QFileInfo(path)).pixmap(32, 32))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        appname = QLabel(os.path.basename(path))
        appname.setWordWrap(True)
        appname.setAlignment(Qt.AlignmentFlag.AlignCenter)
        appname.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        layout.addWidget(icon)
        layout.addWidget(appname)
        
        def exec():
            callback(path)
        button.clicked.connect(exec)
        button.setToolTip(path)
        return button
    
    def launcher(self, osCode=None):
        statusCode = os.system(f'START "" "{osCode}"')
        print(f"[ {'OK' if statusCode == 0 else f'ERR {statusCode}'} ] {osCode if osCode else 'No Command Executed'}")
        

WindowInstance = MainWindow()
sys.exit(APP.exec())
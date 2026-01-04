from PyQt6.QtWidgets import *
from PyQt6.QtCore import QFileInfo, Qt
from PyQt6.QtGui import QAbstractFileIconProvider
import darkmode 
import os, sys

APP = QApplication([])
APP.setStyle('Fusion')
APP.setPalette(darkmode.get_mint_blue_dark_palette())
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.rootPath = os.path.abspath('.\\')
        self.historyPath = os.path.join(self.rootPath, '.\\.history')
        print('[Root Path]', self.rootPath, "\n[Root Path]", self.historyPath)
        # self.
        
        
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
        TopBar.addStretch()
        TopBar.addLayout(self.topBarContent())
        self.navTextBar.setPlaceholderText('Enter a path to scan...')
        self.navTextBar.returnPressed.connect(self._refreshDisplay)
        TopBar.addStretch()
        # self.navTextBar.setText('poggers')
         
        # Main Body
        self.bodyGroup = QGroupBox(" Applications ")
        VCanvas.addWidget(self.bodyGroup)
        self.bodyContainer = QHBoxLayout()
        self.bodyGroup.setLayout(self.bodyContainer)
        
        self.showFullScreen()
        self.setFixedSize(self.size())
        
        self._appsDisplay()
        
    # Just display the list
    def _appsDisplay(self):
        self.tabPages = QTabWidget()
        self.bodyContainer.addWidget(self.tabPages)
        self.applistContent()
    
    # refresh from prev path in combo list
    def _refreshFromPrevPath(self):
        self.navTextBar.setText(self.prevPath.currentText())
        self._refreshDisplay()
        
    # clear and re-display
    def _refreshDisplay(self):
        try:
            self.bodyContainer.removeWidget(self.tabPages)
            print('[Re-Scan] Clearing')
        except AttributeError:
            print('[Re-Scan] No Tabs to clear')
        self._updateHistory()
        self._appsDisplay()
        print('[Re-Scan] Re-Index\'d')
    
    # update the history file and update the list
    def _ifPathHistoryExists(self, item):
        with open(self.historyPath,'r') as history:
            historyList = [name.removesuffix('\n') for name in history.readlines()]
            if item in historyList:
                print(f"[History] <{item}> Exists in History")
                return True
            else:
                print(f"[History] <{item}> Does not Exist in History")
                return False
            
    def _updateHistory(self):
        text = self.navTextBar.text()
        # finalScore = 0
        if not self._ifPathHistoryExists(text) and os.path.exists(text):
            ### It's supposed to return a score that if it already matches
            ### something in the ./.history, it wont add it to the list depending on score
            ### but i realised it's partially kinda the same as self._ifPathHistoryExists()
            # with open('.\\.history', 'r') as history:
            #     score = 0
            #     for line in history.readlines():
            #         # i forgot how to do the opposite of this and my head hurt
            #         compareIntersect = set(text) & set(line.removesuffix('\n'))
            #
            #         newScore = len(compareIntersect)
            #         score = newScore if newScore > score else score
            #         print("[_updateHistory] Comparing: ",set(text), set(line.removesuffix('\n')), 'Score:', score)
            #         print('[_updateHistory] Found Common:', compareIntersect, f'{(score / len(text))*100}%')
            #     else:
            #         finalScore = (score / len(text)) * 100
            #         print('[_updateHistory] Score', finalScore)
            # if finalScore < float(95): 
            with open(self.historyPath, 'a') as history:
                history.write(f"{text}\n")
                print(f'[History] Appended <{text}>', )
        self._refreshPrevPathList()
        
    # refresh combobox
    def _refreshPrevPathList(self):
        self.prevPath.clear()
        self.prevPath.setCurrentText(None)
        if os.path.exists(self.historyPath):
            with open(self.historyPath, 'r') as history:
                for name in history.readlines():
                    self.prevPath.addItem(name.removesuffix('\n'))
                    print(f'[History] Adding <{name.removesuffix('\n')}>')
                print('[History] Loaded')
        else:
            with open(self.historyPath, 'w'):
                print('[History] Created file')
        self.prevPath.setCurrentText(self.navTextBar.text())
    
    def topBarContent(self):
        Layout = QHBoxLayout()
        # Main 
        refresh = QPushButton('Re/Scan')
        refresh.clicked.connect(self._refreshDisplay)
        
        exit = QPushButton('Exit')
        exit.clicked.connect(sys.exit)
        
        self.navTextBar = QLineEdit()
        self.navTextBar.setFixedHeight(25)
        self.navTextBar.setFixedWidth(self.width()) # Before fullscreen, so it's the default 800x640 thing whatever
        
        self.hidden = QPushButton('Show Hidden')
        self.hidden.setCheckable(True)
        
        self.prevPath = QComboBox()
        self.prevPath.setFixedWidth(self.width()) # Before fullscreen, so it's the default 800x640 thing whatever
        self.prevPath.textActivated.connect(self._refreshFromPrevPath)
        self._refreshPrevPathList()
            
        Layout.addWidget(self.hidden)
        Layout.addWidget(refresh)
        Layout.addWidget(self.navTextBar)
        Layout.addWidget(self.prevPath)
        Layout.addWidget(exit)
        return Layout
    
    def applistContent(self):
        def currentDir(paths:str):
            return os.path.join(self.path, paths)
        def addAppX():
            XContents.addWidget(self.appButton(self.path, appPath, (92,68), self.launcher))
            print("[Button] Creating", index, f"<{appPath}>")
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
        showHidden = self.hidden.isChecked()
        navBarPath = self.navTextBar.text()
        self.navTextBar.setText('.\\') if self.navTextBar.text() == '' else self.navTextBar.setText(self.prevPath.currentText())
        self.path = ".\\" if navBarPath == '' else navBarPath
        
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
        else:
            hiddenList = []
        
        self.path = '.\\' if not os.path.exists(self.path) or not os.path.isdir(self.path) else self.path
        self.navTextBar.setText('.\\') if self.path == '.\\' else ''
        
        appList = os.listdir(os.path.abspath(self.path))
        print('[Scan] Start',f'<{self.path}>')
        # # Total (285 - 19) icons @ 1080p
        for app in appList:
            appPath = os.path.join(self.path, app)
            # loose, .hidden w/ or w/o .extension
            if app.startswith('.') or app.split('.')[0] in hiddenList or app in hiddenList:
                if not showHidden: 
                    if not os.path.isfile(appPath): continue
                    print(f"[Hidden] Skip <{appPath}>")
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
                    print(f'[Scan] New row {index} <{appPath}>')
                else:
                    YContents.addStretch()
                    XContents.addStretch()
                    self.tabPages.addTab(Container,f'Apps_{tabIndex}')
                    tabIndex += 1
                    index.get('x')[0] = 1
                    index.get('y')[0] = 0
                    Container, YContents, XContents = newPage()
                    self.tabPages.addTab(Container,f'Apps_{tabIndex}')
                    print(f'[Scan] New Tab {index} <{appPath}>')
                    addAppX()
        else:
            print(f'[Scan] Adding Incomplete Tab y:{index.get('y')}') if index.get('y')[0] < index.get('y')[1] else print(f'[Scan] Nice y:{index.get('y')}')
            XContents.addStretch() if index.get('y')[0] < index.get('y')[1] else ''
            self.tabPages.addTab(Container,f'Apps_{tabIndex}') if index.get('y')[0] < index.get('y')[1] else print(f'[Scan] Adding Complete Tab y:{index.get('y')}')
            YContents.addStretch()
            print('[Scan] Finished')
            # self.tabPages.addTab(Container,'Test')
                    
    def appButton(self, parentpath: str, path: str, geometry: tuple, callback) -> QPushButton:
        x, y = geometry
        path = os.path.abspath(path)
        parentpath = os.path.abspath(parentpath)
        button = QPushButton(self)
        button.setFixedSize(x, y)
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
            callback(parentpath, path)
        button.clicked.connect(exec)
        button.setToolTip(path)
        return button
    
    def launcher(self, parentpath=None, file=None):
        os.chdir(parentpath)
        statusCode = os.system(f'dir /w && START "" "{file}"')
        print(f"[ {'OK' if statusCode == 0 else f'ERR {statusCode}'} ] {file if file else 'No Command Executed'}")
        

WindowInstance = MainWindow()
sys.exit(APP.exec())
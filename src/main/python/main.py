from fbs_runtime.application_context import ApplicationContext
from PySide2 import (
    QtSvg, QtWidgets, QtCore, QtGui
)
from PySide2.QtWidgets import (
    QMainWindow, QDialog, QHBoxLayout, QVBoxLayout, QGroupBox, QSplitter, 
    QWidget, QLabel, QFrame, QMenuBar, QAction, QMenu, QTextEdit, QLineEdit,
    QListWidget, QDockWidget, QToolBar, QToolBox, QTabWidget, QTabBar, QScrollArea
)
from PySide2.QtCore import Qt
from PySide2.QtGui import *
from PySide2.QtSvg import QSvgWidget

import sys, os
from os import path, mkdir

from src.main.python.PDFContext import PDFContext
from src.main.python.QDatasheetDisplay import QDatasheetPageDisplayWidget

class DatasheetView(QMainWindow):

    def __init__(self, pdfPath=None, pageNumber=1):
        
        super().__init__()

        # initialize data files
        # self.fileStore = path.join(path.curdir, "/files")
        # mkdir(self.fileStore)
        self.svgFiles = []


        # window dimensions
        self.top = 300
        self.left = 800
        self.width = 860
        self.height = 980

        self.setGeometry(self.left, self.top, self.width, self.height)
        
        # window title
        self.setWindowTitle("BetterSheets")


        # sets up main layout -- splitters
        self.initUILayout()  
        self.initUIToolbar()

        self.populatePDF(pdfPath, pageNumber)

        self.show()


    def initUILayout(self):

        # set left-side, Dynamic View
        self.dynamicViewDisplay = QLabel()

        self.vBoxA = QVBoxLayout()
        self.vBoxA.addWidget(self.dynamicViewDisplay)
        
        self.groupA = QGroupBox()
        self.groupA.setTitle("Dynamic Veiw")
        self.groupA.setLayout(self.vBoxA)
        
        # set left-side, Static View
        self.staticViewDisplay = QLabel()
        
        self.vBoxB = QVBoxLayout()
        self.vBoxB.addWidget(self.staticViewDisplay)

        self.groupB = QGroupBox()
        self.groupB.setTitle("Static View")
        self.groupB.setLayout(self.vBoxB)


        # add Dynamic and Static Views to resizeable left-side Splitter
        self.altViewSplit = QSplitter(Qt.Vertical)
        self.altViewSplit.addWidget(self.groupA)
        self.altViewSplit.addWidget(self.groupB)
        


        # set up Tools View section
        self.toolsTabView = QTabWidget()
        self.toolsTabView.setTabsClosable(True)
        self.toolsTabView.setMovable(True)
        self.toolsTabView.setDocumentMode(True)

        # self.toolsTabView.setTabBarAutoHide(True)

        # add attribute for storing page notes
        self.notesDB = []
        self.notesDisplay = QListWidget(self)
        self.notesDisplay.setMaximumHeight(200)

        # add ToC to Tools View
        self.ToCListView = QListWidget()
        self.toolsTabView.addTab(self.ToCListView, "Table of Contents")

        # add notes list to tools view
        self.toolsTabView.addTab(self.notesDisplay, "Notes")

        # add tools view to the left-side splitter
        self.altViewSplit.addWidget(self.toolsTabView)




        # set right-side view -- SVG Viewer
        self.mainDisplay = QDatasheetPageDisplayWidget()
        self.mainDisplay.render(["/Users/louissmidt/Documents/BetterSheets/src/main/files/drv8704-page-1.svg","/Users/louissmidt/Documents/BetterSheets/src/main/files/drv8704-page-1.svg"])

        self.mainScroller = QScrollArea(self)
        self.mainScroller.setWidget(self.mainDisplay)
        self.mainScroller.setWidgetResizable(True)
        self.mainScroller.setFixedHeight(400)
        
        self.vBoxMain = QVBoxLayout()
        self.vBoxMain.addWidget(self.mainScroller)

        self.notesArea = QLineEdit()
        self.notesArea.setPlaceholderText("Add a note about this page...")
        self.notesArea.returnPressed.connect(self.onAddNote)
        
        self.vBoxMain.addWidget(self.notesArea)

        self.mainViewGroup = QGroupBox()
        self.mainViewGroup.setTitle("Main View")
        self.mainViewGroup.setLayout(self.vBoxMain)


        # join both sides together
        self.leftRightSplit = QSplitter(Qt.Horizontal)
        self.leftRightSplit.addWidget(self.altViewSplit)
        self.leftRightSplit.addWidget(self.mainViewGroup)        


        self.setCentralWidget(self.leftRightSplit)






    def initUIToolbar(self):

        mainMenu = self.menuBar() # get the menu bar already in use by this QMainWindow subclass
        
        fileMenu = mainMenu.addMenu("File")
        editMenu = mainMenu.addMenu("Edit")
        LayoutMenu = mainMenu.addMenu("Layout")
        AboutMenu = mainMenu.addMenu("About")

        saveAction = fileMenu.addAction("Save")
        quitAction = fileMenu.addAction("Exit Bettersheets")
        quitAction.triggered.connect(self.quitApp)
        copyAction = editMenu.addAction("Copy")
        resetAction = LayoutMenu.addAction("Reset Default Layout")

        # mainMenu.setNativeMenuBar(True)
        # mainMenu.show()

        self. toolBar = self.addToolBar("Tools")
        self.toolBar.addAction(saveAction)
        self.toolBar.addAction(copyAction)
        



    def contextMenuEvent(self, event):
        # return super().contextMenuEvent(event)
        contextMenu = QMenu()
        
        selectAction = contextMenu.addAction("Select Area")
        extractAction = contextMenu.addAction("Extract Content")
        openAction = contextMenu.addAction("Open PDF")
        closeAction = contextMenu.addAction("Close PDF")
        quitAction = contextMenu.addAction("Quit")

        triggered_action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        if triggered_action == quitAction:
            self.quitApp()


    def quitApp(self):
        self.close()


    def onAddNote(self):
        print("note added")

        text = self.notesArea.text()

        if text:
            self.notesDB.append(text)
            self.notesDisplay.clear()
            self.notesDisplay.addItems(self.notesDB)
            self.notesArea.clear()

    def populatePDF(self, pdfPath, pageNumber: int):

        if pdfPath:
            self.myPdfContext = PDFContext(pdfPath, pageNumber)
            
            # get table of contents
            ToC = self.myPdfContext.getToC()
            ToC_headings_list = [x[1] for x in ToC]
            
            self.ToCListView.clear()
            self.ToCListView.addItems(ToC_headings_list)

            # display page in main view
            self.SVGString = self.myPdfContext.getSvgAtPage(pageNumber)

            # set filename of current PDF
            self.pdfName = path.split(pdfPath)[1].split('.')[0]

            # write current page to .svg file
            file_loc = self._writeSVGToFile_(self.pdfName, pageNumber, self.SVGString)

            # open the file we just wrote to
            self.mainDisplay.load(file_loc)
            

    @staticmethod
    def _writeSVGToFile_(pdfName: str, pageNumber: int, svg_string: str) -> str:
        """
        return the full file path we just wrote
        """
        
        file_loc = f"./src/main/files/{pdfName}-page-{pageNumber}.svg"

        with open(file_loc , 'w') as f:  
            f.write(svg_string)

        print("File_loc: ", file_loc)
        return file_loc


    

            

            
            







if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    
    assetPath = os.path.abspath("src/main/assets/drv8704.pdf")
    print(assetPath)

    window = DatasheetView(assetPath, 1)

    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)


# TODO: Add lineedit notes to the dynamic view 
# Add table representation to the UI
# 
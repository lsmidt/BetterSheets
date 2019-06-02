from PySide2 import QtCore, QtSvg, QtWidgets, QtGui
from PySide2.QtWidgets import QVBoxLayout, QWidget
from PySide2.QtSvg import QSvgWidget
import os.path

from src.main.python.PDFContext import PDFContext

class QDatasheetPageDisplayWidget(QSvgWidget):
    """
    Represents the physical rendering of a PDFContext object
    """

    def __init__(self, pdfContext: PDFContext):
        
        super().__init__()

        self.collection = []        

        self.myPDFContext = pdfContext


    def initUI(self):

        self.layout = QVBoxLayout()

        # add svg widgets to the layout
        for widget in self.collection:
            widget.setFixedHeight(400)
            self.layout.addWidget(widget)

        self.setLayout(self.layout)


    def renderPaths(self, svgPaths: list):
        """
        draw given svg images on the widgets
        """

        if len(svgPaths) == 1:

            self.current.load(svgPaths[0])

        elif len(svgPaths) == 2:

            self.current.load(svgPaths[0])
            self.other.load(svgPaths[1])


        #TODO: make this class compatible with generalized n-pages

    def renderPages(self, start, stop):
        """
        draw the given page range [start, stop] of PDFContext on the widgets
        """
        self.directory = self.myPDFContext.directory

        self.myPDFContext.loadPages(range(start, stop + 1))

        for page in range(start, stop + 1):        # range function is not inclusive
            
            pagePath = os.path.join(self.directory, f"{page}.svg")
            print(f"attempted to access page at path: {page}")
            
            page = QSvgWidget()
            page.setFixedHeight(400)
            page.load(pagePath)
            
            self.collection.append(page)

        self.initUI()   # re-init the UI after updating collection size

        


    




    
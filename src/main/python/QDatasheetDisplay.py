from PySide2 import QtCore, QtSvg, QtWidgets, QtGui
from PySide2.QtWidgets import QVBoxLayout, QWidget
from PySide2.QtSvg import QSvgWidget

class QDatasheetPageDisplayWidget(QSvgWidget):
    """
    Represents the physical rendering of a PDFContext object
    """

    def __init__(self):
        
        super().__init__()

        self.layout = QVBoxLayout()
        
        # maintain two concurrent QSvgWidgets; current page, other page
        self.current = QSvgWidget(self)
        self.current.setFixedHeight(400)

        self.other = QSvgWidget(self)
        self.other.setFixedHeight(400)

        self.collection = []    # unused for now


        # add svg widgets to the layout
        self.layout.addWidget(self.current)
        self.layout.addWidget(self.other)

        self.setLayout(self.layout)


    def render(self, svgPaths: list):
        """
        draw given svg images on the widgets
        """

        if len(svgPaths) == 1:

            self.current.load(svgPaths[0])

        elif len(svgPaths) == 2:

            self.current.load(svgPaths[0])
            self.other.load(svgPaths[1])


        #TODO: make this class compatible with generalized n-pages



    
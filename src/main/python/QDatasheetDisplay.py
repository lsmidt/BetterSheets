from PySide2.QtWidgets import QScrollArea, QVBoxLayout, QWidget
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
        self.other = QSvgWidget(self)

        self.collection = []    # unused for now


        # add svg widgets to the layout
        self.layout.addWidget(self.current)
        self.layout.addWidget(self.other)
        self.setLayout(self.layout)


    def render(self, svgPaths: list):
        """
        draw given svg pages on the widgets
        """

        if len(svgPaths) == 1:

            self.current.load(svgPaths[0])

        elif len(svgPaths) == 2:

            self.current.load(svgPaths[0])
            self.other.load(svgPaths[1])


        #TODO: make this class compatible with generalized n-pages



    
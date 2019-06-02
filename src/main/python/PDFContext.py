import sys, os
import fitz
import os.path

class PDFContext():
    """
    Represents an opened PDF and the data structures that enable its lifecycle 
    pdfPath -> string path of the .pdf file
    pages -> list of integer page numbers
    """

    def __init__(self, pdfPath = None, pages: list = [1]):

        self.pdfPath = pdfPath
        self.openPageNumbers = pages

        # create Document instance
        self.document = fitz.open(pdfPath)   

        # set filename of current PDF
        self.pdfName = os.path.split(pdfPath)[1].split('.')[0]

        # load SVGs of open pages into their directory 
        self.directory = self.loadPages(pages)


    def loadPages(self, pages: list) -> bool:
        """
        load svg files of the given pages into appropriate directory.
        return directory of svg files
        """
        directory = f"./src/main/files/{self.pdfName}"

        if not os.path.exists(directory):
            os.mkdir(directory)

        for page in pages:
            
            # ensure that the .svg exists in the appropriate directory
            file_loc = os.path.join(directory, f"{page}.svg")


            if not os.path.exists(file_loc):
                print(f"{file_loc} not found, attempting to create")
                svgString = self.getSvgStringAtPage(page)   
                self.__writeSVGToFile(svgString, file_loc)

        return directory
            
    
    def getToC(self) -> list:
        """
        return table of contents from PyMuPDF  -> [depth, title, x, x]
        """
        
        if self.document:
            return self.document.getToC()
        
        return None

    def getMetadata(self):
        """
        return document metadata from PyMuPDF
        """
        
        if self.document:
            return self.document.metadata
        
        return None

    def getSvgStringAtPage(self, page: int) -> str:
        """
        return SVG string 
        """

        self.loadedPage = self.document.loadPage(page)
        SvgImageString = self.loadedPage.getSVGimage(matrix=fitz.Identity)
        
        return SvgImageString
        
    def getLength(self):

        if self.document:
            return self.document.pageCount
        else:
            return None    # TODO: modify this to riase an exception

    def savePNGtoFile(self):

        for page in self.document:                 
            pix = page.getPixmap(alpha = False)     # render page to an image
            pix.writePNG("page-%i.png" % page.number)    # store image as a PNG


    def __writeSVGToFile(self, svg_string: str, saveLoc: str) -> str:
        """
        write given string to given directory
        return True if executed correctly, False otherwise
        """

        try: 
            with open(saveLoc , 'w+') as f:  
                f.write(svg_string)
        except EnvironmentError:
            return False

        return True

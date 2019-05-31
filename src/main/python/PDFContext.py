import sys
import fitz

class PDFContext():
    """
    Represents an opened PDF 
    """

    def __init__(self, pdfPath = None, pageNumber = 1):

        self.pdfPath = pdfPath
        self.currentPageNumber = pageNumber

        # creates Document instance
        print("Fitz to open"  + str(pdfPath))
        self.document = fitz.open(pdfPath)   
        
    def getToC(self):
        
        if self.document:
            return self.document.getToC()
        
        return None

    def getMetadata(self):
        
        if self.document:
            return self.document.metadata
        
        return None

    def getSvgAtPage(self, page: int) -> str:

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

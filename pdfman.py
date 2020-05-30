import PyPDF2
import sys

# trying to open file from explorer but...
# import easygui
# file = easygui.fileopenbox()

class ManipulatePDF:
    def __init__(self, file_name, inputs=None):
        self.file_name = file_name
        # pass files from terminal
        # python pdfman.py file1 file2 ... filen
        self.inputs = sys.argv[1:]

    def rotate(self):
        try:
            with open(self.file_name, 'br') as file:
                reader = PyPDF2.PdfFileReader(file)
                page = reader.getPage(0)
                page.rotateCounterClockwise(90)
                writer = PyPDF2.PdfFileWriter()
                writer.addPage(page)
                with open('tilted.pdf', 'wb') as rotated_pdf:
                    writer.write(rotated_pdf)
        except FileNotFoundError:
            print(f'File {file} does not exist!')
        except PermissionError:
            print(f'Please close {file}.pdf first!')
    
    def merge(self):
        merger = PyPDF2.PdfFileMerger()
        for pdf in self.inputs:
            merger.append(pdf)
        merger.write('merged.pdf')
    
    def watermark(self):
        template = PyPDF2.PdfFileReader(open(self.file_name, 'br'))
        watermark = PyPDF2.PdfFileReader(open('watermark_template.pdf', 'br'))
        output = PyPDF2.PdfFileWriter()

        for i in range(template.getNumPages()):
            page = template.getPage(i)
            page.mergePage(watermark.getPage(0))
            output.addPage(page)

            with open('watermarked.pdf', 'wb') as file:
                output.write(file)

    def encrypt(self, password):
        writer = PyPDF2.PdfFileWriter()
        reader = PyPDF2.PdfFileReader(open(self.file_name, 'br'))
        
        for i in range(reader.getNumPages()):
            writer.addPage(reader.getPage(i))
            
        writer.encrypt(user_pwd=str(password), owner_pwd=None, 
                        use_128bit=True)

        # new_file_name = ''.join(self.file_name.split())[:-4]
        # print(new_file_name)

        with open('encrypted.pdf', 'wb') as file:
            writer.write(file)

obj = ManipulatePDF(r'paste file path here')
obj.encrypt(password=12345)
# obj.merge()
# obj.watermark()
# -*- coding:utf8 -*-

from pdfminer.pdfparser import PDFParser, PDFDocument, PDFNoOutlines
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice


def pdf_open(fp, passwd):
	# Create a PDF parser object associated with the file object.
	parser = PDFParser(fp)
	doc = PDFDocument()

	# Connect the parser and document objects.
	parser.set_document(doc)
	doc.set_parser(parser)
	doc.initialize(passwd)  #If no password is set, give an empty string.

	print("parser:", parser)
	print("doc:", doc)
	return doc


def pdf_outllines_print(doc):
	# Get the outlines of the document.
	try:
		outlines = doc.get_outlines()
		for (level,title,dest,a,se) in outlines:
			print (level, title)
	except PDFNoOutlines:
		print("error PDFNoOutlines!")
		pass

def pdf_pages_process(doc):
	# Create a PDF resource manager object that stores shared resources.
	rsrcmgr = PDFResourceManager()
	device = PDFDevice(rsrcmgr)		# a PDF device object.
	interpreter = PDFPageInterpreter(rsrcmgr, device)	# a PDF interpreter object.

	# Process each page contained in the document.
	for page in doc.get_pages():
	    interpreter.process_page(page)


def test_pdf(filename):
	fp = open(filename, 'rb')
	if not fp:
		return

	doc = pdf_open(fp, "")
	if doc.is_extractable:
		pdf_outllines_print(doc)
		pdf_pages_process(doc)

	fp.close()


if __name__=='__main__':
    test_pdf("./test_doc.pdf")
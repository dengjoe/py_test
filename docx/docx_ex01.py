# -*- coding: utf-8 -*-

from docx import Document
from docx.shared import Inches


class CItem(object):
	def __init__(self, nid, qty, desc):
		self.id = nid
		self.qty= qty
		self.desc = desc


def create_docx_demo(filename):
	document = Document()
	 
	document.add_heading('Document Title', 0)
	 
	p = document.add_paragraph('A plain paragraph having some ')
	p.add_run('bold').bold = True
	p.add_run(' and some ')
	p.add_run('italic.').italic = True
	 
	document.add_heading('Heading, level 1', level=1)
	document.add_paragraph('Intense quote', style='Intense Quote')
	 
	document.add_paragraph('first item in unordered list', style='List Bullet')
	document.add_paragraph('first item in ordered list', style='List Number')
	 
	# add picture
	document.add_picture('docx_01.jpg', width=Inches(5))
	 
	# add table 
	table = document.add_table(rows=1, cols=3)
	hdr_cells = table.rows[0].cells
	hdr_cells[0].text = 'Qty'
	hdr_cells[1].text = 'Id'
	hdr_cells[2].text = 'Desc'

	recordset = []
	recordset.append(CItem(0,23.4, "named oen"))
	recordset.append(CItem(1,12.6, "named fiv"))

	for item in recordset:
		row_cells = table.add_row().cells
		row_cells[0].text = str(item.qty)
		row_cells[1].text = str(item.id)
		row_cells[2].text = item.desc
	
	# add page break 
	document.add_page_break()
	document.save(filename)


def read_docx(filename):
    fullText = []
    doc = Document(filename)
    print(len(doc.paragraphs))

    for p in doc.paragraphs:
        fullText.append(p.text)
    return '\n'.join(fullText)



if __name__=='__main__':
    create_docx_demo('out1.docx')
    print(read_docx("out1.docx"))    
    # print(read_docx("input1.docx"))

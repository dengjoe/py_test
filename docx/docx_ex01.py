# -*- coding: utf-8 -*-
# need install python-docx
# 

from docx import Document
from docx.shared import Inches
from docx.shared import Pt
from docx.shared import RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH


class CItem(object):
	def __init__(self, nid, qty, desc):
		self.id = nid
		self.qty= qty
		self.desc = desc


def create_docx_demo(filename):
	document = Document()
	 
	# add 标题：标题level级别为1到9之间的整数。级别0，将添加“标题”段落。
	h = document.add_heading('Document Title', 0)
	h.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER  # CENTER居中对齐 LEFT左对齐 RIGHT右对齐
	
	# add 正文段落
	p = document.add_paragraph('A plain paragraph having some ')
	p.add_run('bold').bold = True
	
	run = p.add_run(' 和一些 ')
	run.font.name = "宋体"  # 默认字体name和size都是None
	run.font.size = Pt(18)
	run.font.color.rgb = RGBColor(0xff, 0x00, 0x00)
	run.font.bold = True  #加粗  
	run.font.italic = True  #斜体  
	run.font.underline = True #下划线  

	p.add_run('italic.').italic = True
	

	document.add_heading('Heading, level 1', level=1)
	document.add_heading('Heading, level 2', level=2)

	document.add_paragraph('paragraph style=Intense quote', style='Intense Quote')
	document.add_paragraph('paragraph style=Title', style='Title')
	 
	document.add_paragraph('paragraph style=List Bullet', style='List Bullet')
	document.add_paragraph('paragraph style=List Number', style='List Number')
	document.add_paragraph('paragraph style=List Continue', style='List Continue')
	 
	# add picture, 不设置width，则显示为原图大小。 5英寸适合A4.返回对象 InlineShape
	
	# 方法1 直接加入图片，无法找到嵌入图像的段落，只能如此来居中
	pic = document.add_picture('docx_01.jpg', width=Inches(2))
	num = len(document.paragraphs)
	document.paragraphs[num-1].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
	
	# 方法2 通过run嵌入图片
	p = document.add_paragraph('')
	p.add_run('').add_picture('docx_01.jpg', width=Inches(2))
	p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER 


	# add 表格 
	table = document.add_table(rows=1, cols=3)
	# 'Colorful Grid';'Light Grid';'Light List';'Light Shading;'Table Grid'
	table.style = 'Table Grid' 

	hdr_cells = table.rows[0].cells
	hdr_cells[0].text = 'Qty'
	hdr_cells[1].text = 'Id'
	hdr_cells[2].text = 'Desc'

	recordset = []
	recordset.append(CItem(0,23.4, "named oen"))
	recordset.append(CItem(1,12.6, "named fiv"))
	recordset.append(CItem(2,18.6, "盒饭"))

	for item in recordset:
		row_cells = table.add_row().cells
		row_cells[0].text = str(item.qty)
		row_cells[1].text = str(item.id)
		row_cells[2].text = item.desc
	
	# add 分页符
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

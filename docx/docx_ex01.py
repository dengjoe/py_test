# -*- coding: utf-8 -*-
# need install python-docx
# 

from docx import Document
from docx.shared import Inches
from docx.shared import Pt
from docx.shared import RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn

class CItem(object):
    def __init__(self, nid, qty, desc):
        self.id = nid
        self.qty= qty
        self.desc = desc


def create_docx_demo(filename):
    document = Document()
     
    # add 标题：标题level级别为1到9之间的整数。级别0，将添加“标题”段落。
    h = document.add_heading('我的 Title', 0)
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
    document.add_paragraph('paragraph style=List Number\n', style='List Number')
    document.add_paragraph('paragraph style=List Continue', style='List Continue')
    document.add_paragraph('\n') #是本段里加了一个换行。
    document.add_paragraph('')
    document.save(filename)

    p = document.add_paragraph("")
    r = p.add_run("微软雅黑")
    r.font.name = u'微软雅黑'
    r.font.size = Pt(18)
    r._element.rPr.rFonts.set(qn('w:eastAsia'), r.font.name)

    r = p.add_run("楷体")
    r.font.name = u'楷体'
    r.font.size = Pt(16)
    r._element.rPr.rFonts.set(qn('w:eastAsia'), r.font.name)

    r = p.add_run("宋体")
    r.font.name = u'宋体'
    r.font.size = Pt(14)
    r._element.rPr.rFonts.set(qn('w:eastAsia'), r.font.name)

    r = p.add_run("黑体")
    r.font.name = u'黑体'
    r.font.size = Pt(12)
    r._element.rPr.rFonts.set(qn('w:eastAsia'), r.font.name)

    # 自定义style只能对英文起作用
    styles = document.styles
    s1 = styles.add_style('s1', WD_STYLE_TYPE.PARAGRAPH)
    s1.font.size = Pt(12)
    s1.font.name = "宋体" 
    document.add_paragraph("我的style", style="s1")
    document.add_paragraph("", style="s1")
     
    # add picture, 不设置width，则显示为原图大小。 5英寸适合A4.返回对象 InlineShape
    
    # 方法1 直接加入图片，无法找到嵌入图像的段落，只能如此来居中
    pic = document.add_picture('docx_01.jpg', width=Inches(4))
    num = len(document.paragraphs)
    document.paragraphs[num-1].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # 方法2 通过run嵌入图片
    p = document.add_paragraph('')
    p.add_run('').add_picture('docx_01.jpg', width=Inches(6))
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


def print_ParagraphFormat(pformat):
    print("  ParagraphFormat: ", pformat.alignment, pformat.first_line_indent, pformat.keep_together, pformat.keep_with_next, pformat.left_indent, pformat.line_spacing, pformat.line_spacing_rule, pformat.page_break_before, pformat.right_indent, pformat.space_after, pformat.space_before, pformat.widow_control, "pformat.tab_stops=", pformat.tab_stops)
    # tab_stop properties(一般都是None): .alignment, .leader, .position 
    for ts in pformat.tab_stops:
        print("    tab_stop:", ts.alignment, ts.leader, ts.position)

# runs(Sequence of Run)中Run的属性：bold,italic,underline,text, 字体(Font),字符样式(_CharacterStyle)
def print_runs(runs):
	for run in runs:
		print("  run:", run.bold, run.italic, run.underline, run.text, run.font, run.style)


# 读取文档的段落和表格内容、属性
def read_docx(filename):
    fullText = []
    doc = Document(filename)
    print("paragraphs count: ", len(doc.paragraphs), "\n")

    # 1.段落属性：样式(_ParagraphStyle)、对齐、段落格式(ParagraphFormat), runs(Sequence of Run), text
    for p in doc.paragraphs:
        print(" p.style=", p.style, " p.alignment=", p.alignment, p.runs," p.text=", p.text)
        print_ParagraphFormat(p.paragraph_format)
        print_runs(p.runs)


    # 2.表格属性：样式(_TableStyle)、对齐、autofit、columns(_Columns)、rows(_Rows)、table_direction
    print("\ntable:")
    for table in doc.tables:
        print(" table.style=", table.style)
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    print(paragraph.text)


if __name__=='__main__':
    create_docx_demo('out1.docx')
    read_docx("out1.docx")   
    # read_docx("input1.docx")

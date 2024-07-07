import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

script_dir = os.path.dirname(os.path.abspath(__file__))

input_file = os.path.join(script_dir, "test.txt")

text_size = 40

def text_to_pdf(input_file, output_dir):
    output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0] + '.pdf')
    
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter
    
    pdfmetrics.registerFont(TTFont('Times', 'times.ttf'))
    c.setFont("Times", text_size)
    
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    x, y = 50, height - 50
    line_height = text_size + 10
    
    for line in lines:
        if y < line_height:
            c.showPage()
            y = height - 50
        
        c.drawString(x, y, line.strip())
        
        y -= line_height
    
    c.save()
    print(f'Report has been saved to {output_file}')

def set_output_path(path):
    output_dir = path
    text_to_pdf(input_file, output_dir)
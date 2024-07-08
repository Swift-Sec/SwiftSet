import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, "results.txt")

def get_text_size_and_style(line):
    if line.startswith('#####'):
        return 10, 'Helvetica-Bold'
    elif line.startswith('####'):
        return 14, 'Helvetica-Bold'
    elif line.startswith('###'):
        return 18, 'Helvetica-Bold'
    elif line.startswith('##'):
        return 24, 'Helvetica-Bold'
    elif line.startswith('#'):
        return 32, 'Helvetica-Bold'
    else:
        return 12, 'Helvetica'

def split_lines(text, max_chars):
    lines = []
    for line in text.splitlines():
        if line.startswith('#'):
            lines.append(line.strip())
        else:
            if len(line) > max_chars:
                words = line.split()
                current_line = ''
                for word in words:
                    if len(current_line) + len(word) + 1 > max_chars:
                        lines.append(current_line.strip())
                        current_line = word + ' '
                    else:
                        current_line += word + ' '
                lines.append(current_line.strip())
            else:
                lines.append(line)
    return lines

def text_to_pdf(input_file, output_dir, max_line_length=100, y_start=700):
    output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0] + '.pdf')
    
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter
    
    with open(input_file, 'r') as file:
        content = file.read()
    
    lines = split_lines(content, max_line_length)
    
    x, y = 50, y_start
    text_size = 12
    
    for line in lines:
        text_size, font_name = get_text_size_and_style(line)
        c.setFont(font_name, text_size)
        line_height = text_size + 10
        
        if y - line_height < 50:
            c.showPage()
            y = height - 50
        
        c.drawString(x, y, line.lstrip('#').strip())
        y -= line_height
    
    c.save()
    print(f'Report has been saved to {output_file}')

def set_output_path(path):
    output_dir = path
    text_to_pdf(input_file, output_dir)

output_directory = script_dir

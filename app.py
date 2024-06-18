from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

app = Flask(__name__)

def is_wrapped(lines):
    max_length = max(len(line) for line in lines)
    return max_length > 90 

def wrap_lines(lines):
    wrapped_lines = []
    for line in lines:
        if len(line) > 90: 
            wrapped_lines.extend([line[i:i+90] for i in range(0, len(line), 90)])
        else:
            wrapped_lines.append(line)
    return wrapped_lines

def text_to_pdf(input_file, output_file):
    c = canvas.Canvas(output_file, pagesize=A4)
    margin = 50
    max_y = A4[1] - margin
    line_height = 14
    font_name = "Times-Roman"

    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    if is_wrapped(lines):
        lines = wrap_lines(lines)

    y = max_y
    c.setFont(font_name, 12)

    for line in lines:
        line = line.rstrip()  
        if y < margin:
            c.showPage()
            c.setFont(font_name, 12)
            y = max_y
        c.drawString(margin, y, line)
        y -= line_height

    c.save()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            input_name = filename.split('.')[0]
            if filename.lower().endswith('.txt'):
                text_file = f'tmp/{filename}'
                file.save(text_file)
                output_file = f'tmp/{input_name}_to_pdf.pdf'
                text_to_pdf(text_file, output_file)
                return send_file(output_file, as_attachment=True)
            else:
                return render_template('index.html', error='Please upload a .txt file.')
    return render_template('index.html', error=None)

if __name__ == '__main__':
    app.run(debug=True)

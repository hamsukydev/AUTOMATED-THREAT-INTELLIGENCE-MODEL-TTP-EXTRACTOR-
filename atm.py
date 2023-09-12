from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from pdfminer.high_level import extract_text
import os
import secrets
from form import AnalysisForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'
app.config['UPLOAD_FOLDER'] = 'uploads'

# this is a function to upload the pdf
def process_pdf_upload(filee):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(filee.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, picture_fn)
    filee.save(picture_path)
    return picture_fn

import PyPDF2

def extract_text_from_pdf(pdf_file):
    pdf_text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
    except Exception as e:
        # Handle exceptions, e.g., invalid PDF file or password-protected PDF
        print(f"Error extracting text from PDF: {e}")
    return pdf_text


@app.route('/summary', methods=['GET'])
def summary():
    analysis_results = None  # Initialize analysis_results here
    return render_template('summary.html', analysis_results=analysis_results)
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = AnalysisForm()
    analysis_results = None  # Initialize analysis_results here

    if form.validate_on_submit():
        if request.method == 'POST':
            filee = form.doc.data
            if filee and filee.filename.endswith('.pdf'):
                # Process the PDF file
                file_path = process_pdf_upload(filee)

                with open(file_path, 'rb') as pdf_file:
                    text = extract_text_from_pdf(pdf_file)

                lines = text.split('\n')
                extracted_info = {}

                for line in lines:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        key = parts[0].strip().lower()  # Store lowercase keys
                        value = parts[1].strip()
                        extracted_info[key] = value

                if extracted_info:
                    analysis_results = extracted_info

                    flash('File uploaded and analyzed successfully', 'success')
                else:
                    flash('Failed to extract information from the PDF', 'danger')

                os.remove(file_path)  # Clean up the uploaded file

                return render_template('/summary.html', form=form, analysis_results=analysis_results)

    return render_template('/index.html', form=form, analysis_results=analysis_results)

@app.route('/guarrantor', methods=['GET', 'POST'])
# this is the route to the scan screen
@app.route("/scan")
def scan():
    return render_template('/screening.html', title='Screen')


if __name__ == '__main__':
    app.run(debug=True)

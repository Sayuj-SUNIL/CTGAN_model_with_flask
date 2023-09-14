from flask import Flask, request, jsonify,send_file,render_template
import os
import subprocess
import pickle
import pandas as pd

app = Flask(__name__,static_folder='outputs')

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET']) # home route
def home():
    return render_template('index.html')


@app.route('/uploads', methods=['POST']) # this route is to upload a file to train the model and use it to generate a synthetic table
def upload_file():
    
    files = os.listdir('uploads')
    # Loop through the files and remove them
    for file in files:
        file_path = os.path.join('uploads', file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if not file.filename.endswith('.csv'):
            return "File must be a CSV"

    if file:
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
    return 'File successfully uploaded'

@app.route('/processing', methods=['GET'])

def process_file():  # Run the IPython Notebook  
    notebook_path = 'ctgansynthesis.ipynb'
    cmd = f"jupyter nbconvert --to notebook --execute {notebook_path} --output {notebook_path}"
    subprocess.run(cmd, shell=True)
    return "File Processed"

@app.route('/download', methods=['GET'])
def download_file():
    # Specify the directory where the file is located (outputs directory)
    file_path = './outputs/synthetic1_data.csv'
    #
    # so the output file name will always remian same
    # Specify the full path to the file
    try:
        # Send the file as a download
        # Remove temporary files
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        return "File not found"
    
@app.route('/create/<rows>',methods=['GET'])
def create_file(rows):
    # Create synthetic data using SDV library and save it into csv format
    # rows - number of rows you want for your dataset
    try:
        with open('the_trained_one.pkl', 'rb') as f:
            synthesizer = pickle.load(f)    
        synthetic_data=synthesizer.sample(num_rows=rows) ## not working the (.sample) and (.to_csv) 
        output_file_path = os.path.join('outputs', 'synthetic_data.csv')
        synthetic_data.to_csv(output_file_path, index=False)
        file_path = 'C:\\Users\\sayuj\\OneDrive\\Documents\\SDV project\\outputs\\synthetic_data.csv' 
        return send_file(file_path, as_attachment=True)
    except ValueError:
        return "Invalid input. Please enter a valid number of rows."
    
if __name__ == '__main__':
    app.run(debug=True)

## imp notice there is no need to clear out the directory in the ouput folder because the output file names
# are always consistent therefore they will overwrite themselves
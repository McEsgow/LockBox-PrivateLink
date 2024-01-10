from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_file', methods=['POST'])
def process_file():
    file_path = request.form['file_path']
    # Add your file processing logic here
    print("Processing file:", file_path)
    return 'File processed successfully!'

if __name__ == '__main__':
    app.run(debug=True)

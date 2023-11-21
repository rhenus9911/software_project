from flask import Flask, render_template, request, redirect
from table import table_info

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report')
def report():
    word = request.args.get('word')
    if word:
        sales_img, density_img, trans_sales, trans_den = table_info(word)
    else:
        return redirect('/')

    return render_template('report.html')

# 프로그램 시작점
if __name__ == '__main__':
    app.run(debug=True)
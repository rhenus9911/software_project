from flask import Flask, render_template, request, redirect
from table import table_info

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report')
def report():
    dong = request.args.get('dong')
    if dong:
        sales_img, density_img, trans_sales, trans_den = table_info(dong)
    else:
        return redirect('/')

    return render_template('report.html',
                            dong = str(dong),
                            sales_dict = trans_sales,
                            den_dict = trans_den,
                            graph1 = sales_img,
                            graph2 = density_img)

# 프로그램 시작점
if __name__ == '__main__':
    app.run(debug=True)
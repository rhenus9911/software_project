from flask import Flask, render_template, request, redirect
from table import table_info

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'GET':
        return redirect('/')
        
    elif request.method == 'POST':
        gu = request.form.get('gu')
        dong = request.form.get('dong')
        if dong:
            sales_img, density_img, trans_sales, trans_den, card_dict, pop_dict = table_info(dong)
        else:
            return redirect('/')

        return render_template('report.html',
                                gu = str(gu),
                                dong = str(dong),
                                sales_dict = trans_sales,
                                den_dict = trans_den,
                                recommend = list(trans_den.items())[0][0],
                                graph1 = sales_img,
                                graph2 = density_img,
                                c_dict = card_dict,
                                p_dict = pop_dict
                                )

# 프로그램 시작점
if __name__ == '__main__':
    app.run(debug=True)

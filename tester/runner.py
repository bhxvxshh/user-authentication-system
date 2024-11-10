from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def input_form():
    return render_template('input_form.html')

@app.route('/page1', methods=['GET'])
@app.route('/page2', methods=['GET'])
@app.route('/page3', methods=['GET'])
def navigate():
    input_value = request.args.get('input_value')
    route = request.args.get('route')

    # Handle the input value based on the route (e.g., Page 1, Page 2, or Page 3)
    result = f"Received value on {route}: {input_value}"
    return result

if __name__ == '__main__':
    app.run(debug=True)

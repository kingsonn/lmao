from flask import Flask, request, render_template
import config
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
import uuid
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/free', methods=["GET", "POST"])
def free():
    if request.method == "POST":
        order = {
            'id': "'"+str(uuid.uuid1())+"'",
            'email': "hanson@gmail.com",
            'name': "Hanson",
            'contactNum': 1234567891
        }
        try:
            container.create_item(body=order)
            return render_template('shop.html', result="Use Coupon code: fer25324f32fg")

        except exceptions.CosmosResourceExistsError:
            return render_template('index.html', result="Already claimed")
    return render_template('index.html')





if __name__ == '__main__':
    
    app.run()

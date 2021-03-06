from flask import Flask, request, render_template
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
import requests
app = Flask(__name__)


client = cosmos_client.CosmosClient('https://bloodbank.documents.azure.com:443/', {'masterKey': 'ltRr4lvPImIBK2wvyuubTsFDlrImlthgWoiRakkn5RKREIV4Cwt7KWLXwhHmlQRg1SC5PZzs80ULZMDGVywYRA=='}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)

db = client.get_database_client('Test')
container = db.get_container_client('getawhey')

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/free', methods=["GET", "POST"])
def free():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        number = request.form['number']
        order = {
            'id': email,
            'email': email,
            'name': name,
            'contactNum': number
        }
        try:
            container.create_item(body=order)
            url = 'https://prod-04.northcentralus.logic.azure.com:443/workflows/55199d570fdc4f84b62e832fe7cd19e2/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=o5bwg3yLQIeXoqyKed4BJgFArAY0w1joDQkQWcQLjWk'
            headers = {"Content-Type": "application/json"}
            payload = {
                "name": name,
                "email": email,
            }
            response = requests.post(url, headers=headers, json=payload)
            print(response.status_code)
            return render_template('shop.html', result="Use Coupon code: fer25324f32fg")

        except exceptions.CosmosResourceExistsError:
            url = 'https://prod-04.northcentralus.logic.azure.com:443/workflows/55199d570fdc4f84b62e832fe7cd19e2/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=o5bwg3yLQIeXoqyKed4BJgFArAY0w1joDQkQWcQLjWk'
            headers = {"Content-Type": "application/json"}
            payload = {
                "name": name,
                "email": email,
            }
            response = requests.post(url, headers=headers, json=payload)
            print(response.status_code)
            return render_template('index.html', result="Already claimed")
    return render_template('index.html')





if __name__ == '__main__':
    
    app.run()

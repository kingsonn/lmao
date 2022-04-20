from flask import Flask, request, render_template
import config
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.documents as documents
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey

app = Flask(__name__)
HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']
CONTAINER_ID = config.settings['container_id']

client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)

db = client.get_database_client(DATABASE_ID)
container = db.get_container_client(CONTAINER_ID)

@app.route('/')
def home():
    return render_template('shop.html')


@app.route('/shop')
def shop():
    return render_template('shop.html')


@app.route('/free', methods=["GET", "POST"])
def free():
    if request.method == "POST":
        order = {
            'id': "hhh",
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

from flask import Flask
from app.api import user_router, csv_router, movies_router
from app.bootstrap import load_bootstrap_data
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, origins="*", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
     supports_credentials=True)
cross_origin(app)

load_bootstrap_data()

app.register_blueprint(csv_router, url_prefix='/api/csv')
app.register_blueprint(user_router, url_prefix='/api/user')
app.register_blueprint(movies_router, url_prefix='/api/movies')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

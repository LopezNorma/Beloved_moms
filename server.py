from flask_app import app 
from flask_app.controllers import moms_controller
from flask_app.controllers import posts_controller
if __name__=='__main__':
    app.run(debug=True, port=5000)
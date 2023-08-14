from flask import Flask, request, jsonify
from MyObject import MyObject
from markupsafe import escape

app = Flask(__name__)

class MyFlaskApp():
    _instance = None

    def __new__(self):
        if self._instance == None:
            self._instance = super(MyFlaskApp, self).__new__(self)
            self._instance.init_app()
        return self._instance

    def init_app(self):
        self.my_obj = MyObject()
        self.app = app

        self.app.route('/')(self.hello)
        self.app.get('/greet')(self.greet_get)
        self.app.post('/greet')(self.greet_post)
        self.app.route('/info')(self.info)
        self.app.route('/intinc')(self.incInt)
        self.app.route('/str/<string:new_str>')(self.setStr)

    def run(self):
        self.app.run(debug=True, host = '0.0.0.0')

    def hello(self):
        return 'Hello, World!'
    
    def greet_get(self):
        return 'Hello, GET request!'

    def greet_post(self):
        data = request.get_json()  # Assuming the client sends JSON data in the request body
        if data and 'name' in data:
            return jsonify({'message': f'Hello, {data["name"]}!'})
        else:
            return jsonify({'error': 'Invalid request data. Expected JSON with "name" field.'}), 400

    def info(self):
        print('my_obj.int = %d' %self.my_obj.int)
        print('my_obj.str = %s' %self.my_obj.str)
        return jsonify({'my_obj.int': self.my_obj.int, 'my_obj.str':self.my_obj.str})
        return f'my_obj.int = {my_obj.int} \n my_obj.str = {my_obj.str}'

    def incInt(self):
        self.my_obj.int += 1
        return ('my_obj.int increased by 1')
    
    def setStr(self,new_str):
        self.my_obj.str = escape(new_str)
        return (f'my_obj.str set to {new_str}')
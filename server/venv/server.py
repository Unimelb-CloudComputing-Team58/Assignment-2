from flask import Flask, jsonify, abort, request, make_response, url_for
import couchdb
couch = couchdb.Server()
db = couch['twitter']
app = Flask(__name__, static_url_path="")

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/area/tweets', methods=['GET'])
def get_tasks():
    map_fun = '''function (doc) {    
          emit(doc.area, 1);      
      }
    }'''
    reduce_fun = ''' function(keys, values) {
            return sum(values);
        } '''
    results = db.query(map_fun, reduce_fun)
    return jsonify({'results': results})

@app.route('/area/tweets_attitude', methods=['GET'])
def get_tasks():
    map_fun = '''function (doc) {    
              emit(doc.area, doc.attitude 1);      
          }
        }'''
    reduce_fun = ''' function(keys, values) {
                return sum(values);
            } '''
    results = db.query(map_fun, reduce_fun)
    return jsonify({'results': results})


@app.route('/aurin', methods=['GET'])
def get_tasks():
    return jsonify({'result': ""})
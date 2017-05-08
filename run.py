#! /usr/bin/env python
from flask import Flask, render_template, request, jsonify
import summarization

app = Flask(__name__)

@app.route('/textsummarization', methods=['GET'])
def classify():
   return render_template('summarization.html')

# service use for summarize the given text
@app.route('/summarize', methods=['POST'])
def summarize():
    response = None
    if request.method == 'POST' :
        try:
            req_data = request.get_json()
            print req_data
            print req_data['top_sentences']
            response = summarization.summarize(req_data['data'],int(req_data['top_sentences']))
        except Exception as e:
            return respond(e)
       
    return respond(None, res=response)
       
def respond(err, res=None):
    return_res =  {
        'status_code': 400 if err else 200,
        'body': err.message if err else res,
    }
    return jsonify(return_res)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
from flask import Flask
app = Flask(__name__)

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, \
                  abort, jsonify, flash, make_response

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required

import requests
import json

from repositor import *
from config import *
import elasticsearch
from elasticsearch import Elasticsearch

app.config['SECRET_KEY'] = SECRET_KEY
host_url = ['https://search-glos-metadata-jy4xxxs6o26fgmdj7guj32nvje.us-east-2.es.amazonaws.com']
es_conn = Elasticsearch(host_url)


class SearchForm(FlaskForm):
    search = StringField('What is your search term?', validators=[Required()])
    advanced1 = StringField('Advanced1')
    advanced2 = StringField('Advanced2')
    advanced3 = StringField('Advanced3')
    advanced4 = StringField('Advanced4')
    submit = SubmitField('')
    
@app.route('/')
def index():
    searchForm = SearchForm()
    return render_template('searchform.html', form=searchForm, api_key=API_KEY, id_coords_list_of_tuples=json.dumps(id_coords_list_of_tuples))

@app.route('/result', methods = ['GET', 'POST'])
def resultSearchForm():
    form=SearchForm(request.form)
    if request.method == 'POST' and form.search.data != "":
        searchTerm = form.search.data

        results = es_conn.search(index="metadata", body={"query": {"match": {'keyword':searchTerm}}})
        for hit in results['hits']['hits']:
            print(hit['_source']['title'])
            print(hit['_source']['keyword'])
            print(hit['_source']['abstract'])
             

        return render_template('result.html', searchTerm=searchTerm, api_key=API_KEY, id_coords_list_of_tuples=json.dumps(id_coords_list_of_tuples), results=results, results_len=len(results))
    else:
        flash('All fields are required!')
        return redirect(url_for('index'))

##############################
# Use this for running locally
##############################
# if __name__ == '__main__':
#     app.run(debug=True)


##############################
# Use this for running on AWS
##############################
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
from flask import render_template, request, session, Flask
import openai_api

import config
from datasets import load_dataset

modelhub_dataset = load_dataset("patriziobellan/PET", name='relations-extraction')
#from models import Person


#print(openai_api.getPerformerExample(modelhub_dataset, 0)[0])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'random_1'



#app.add_api(config.basedir +"/" + "swagger.yml")
print(config.basedir +"/" + "swagger.yml")


@app.route("/")
def home():
    #people = Person.query.all()
    return render_template("home.html")#, people=people)

@app.route('/context', methods = ['POST'])
def context():
    if request.method == 'POST':
        print(request.form['desc'])
        if(len(request.form['desc']) == 0):
            session['name'] = request.form['name']
            return "200"
        else:
            session['name'] = request.form['name']
            session["desc"] = request.form['desc']
            txt = request.form['desc']
            resp = openai_api.getActivities(modelhub_dataset, txt)

            # response = openai_api.labelTextRequest(modelhub_dataset, txt)
            session['actors'] = resp[2]
            session['activities'] = resp[1]
            session['associations'] = resp[3]
            return resp

@app.route('/inconsistencies', methods = ['POST'])
def inconsistencies():
    print("start")
    if 'activities' in session and 'desc' in session:
        print("check")
        model = request.form['model']
        return openai_api.getInconsistencies(session['activities'], model)
    else:
        return "Inconsistencies cannot be checked: <br> No Textual Description of Process provided yet Click on 'Provide Context'"



@app.route('/gpt_request', methods = ['POST'])
def gpt_request():
    if request.method == 'POST':
        txt = request.form['txt']
        model = request.form['model']

        #print(session['name'])

        if 'name' in session:
            name = session['name']
        else:
            name = None

        if 'desc' in session:
            desc = session['desc']
        else:
            desc = None
        answer = openai_api.text_request(txt, model, desc)
        print(answer)
        return answer
    


@app.route('/conventions', methods = ['POST'])
def conventions():
    if request.method == 'POST':
        model = request.form['model']
        if 'name' in session:
            name = session['name']
        else:
            name = None
        answer = openai_api.convention_request(model, name)
        print(answer)
        return answer
    

    
@app.route('/predict_next', methods = ['POST'])
def prediction():
    if request.method == 'POST':
        model = request.form['model']
        if 'name' in session:
            name = session['name']
        else:
            name = None

        if 'desc' in session:
            desc = session['desc']
        else:
            desc = None

        answer = openai_api.nextElm_request(model, name, desc)
        print(answer)
        return answer
    
    
@app.route('/label_suggestion', methods = ['POST'])
def label_suggestion():
    if request.method == 'POST':
        model = request.form['model']

        if 'desc' in session:
            desc = session['desc']
        else:
            desc = None

        answer = openai_api.getLabelSuggestion(model, desc)
        return answer



# ommitable
@app.route('/best_practices', methods = ['POST'])
def best_practices():
    if request.method == 'POST':
        model = request.form['model']

        print(session['name'])

        if 'name' in session:
            name = session['name']
        else:
            name = None

        if 'desc' in session:
            desc = session['desc']
        else:
            desc = None
        #answer = openai_api.pmg_request(model, name, desc)
        answer = openai_api.pmgSix(model, desc)
        print(answer)
        return answer

'''
@app.route('/enhancement', methods = ['POST'])
def enhancement():

'''   







if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
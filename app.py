from flask import render_template, request, session, Flask
import openai_api
import config
from datasets import load_dataset

#Load PET-Dataset
modelhub_dataset = load_dataset("patriziobellan/PET", name='relations-extraction')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'random5'



@app.route("/")
def home():
    return render_template("home.html")


@app.route('/context', methods = ['POST'])
def context():
    if request.method == 'POST':
        if(len(request.form['desc']) == 0):
            session['name'] = request.form['name']
            return "200"
        else:
            session['name'] = request.form['name']
            session["desc"] = request.form['desc']
            txt = request.form['desc']
            resp = openai_api.getInformation(modelhub_dataset, txt)

            if isinstance(resp, Exception):
                return resp
            
            else:
                session['actors'] = resp[2]
                session['activities'] = resp[1]
                session['associations'] = resp[3]
                session['full_activities'] = resp[4]
                return resp
        

@app.route('/inconsistencies', methods = ['POST'])
def inconsistencies():
    if 'activities' in session:
        model = request.form['model']
        print(type(session['full_activities']))
        activities = [sublist[1] for sublist in session['full_activities']]
        activities = ', '.join(activities)
        return openai_api.getInconsistencies(activities, model)
    else:
        return "Inconsistencies cannot be checked: <br> No Textual Description of Process provided yet Click on 'Provide Context'"



@app.route('/gpt_request', methods = ['POST'])
def gpt_request():
    if request.method == 'POST':
        txt = request.form['txt']
        model = request.form['model']


        if 'name' in session:
            name = session['name']
        else:
            name = None

        if 'desc' in session:
            desc = session['desc']
        else:
            desc = None
        answer = openai_api.text_request(txt, model, desc)
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





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
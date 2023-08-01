import openai
import utility as u

# Setting the api key for OpenAI API, must be individually adjusted
api_key = "placeholder"
openai.api_key = api_key



"""
Information Extraction Request.
Retrieves the information in three steps:
1. Activity Extraction
2. Performer Extraction 
3. Activity Data Extraction
"""
def getInformation(modelhub_dataset, txt):
    # prepare example 1:
    prepExample = u.getPerformerExample(modelhub_dataset, 19)
    ex_sol_one = prepExample[1]
    ex_sol_one = '; '.join(ex_sol_one)

    ex_in_one_desc = modelhub_dataset['test'][19]['tokens']
    ex_in_one_desc = ' '.join(ex_in_one_desc)

    ex_in_one_activities = '; '.join(prepExample[0])

    ex_in_one = "Consider the following process: Textual Description: ### " + ex_in_one_desc + "### \n Activities: ### " + ex_in_one_activities + " ###"

    # prepare example 2:
    prepExample_two = u.getPerformerExample(modelhub_dataset, 17)
    ex_sol_two = prepExample_two[1]
    ex_sol_two = '; '.join(ex_sol_two)

    ex_in_two_desc = modelhub_dataset['test'][17]['tokens']
    ex_in_two_desc = ' '.join(ex_in_two_desc)

    ex_in_two_activities = '; '.join(prepExample[0])

    ex_in_two = "Consider the following process: Textual Description: ### " + ex_in_two_desc + "###  \n Activities: " + ex_in_two_activities + " ###"


    # conduct request    
    txt = txt.replace(".", " . ")
    txt = txt.replace(",", " , ")    
    txt = txt.replace(";", " ; ") 

    # make get activities of text request
    print("First Request")
    try:
        response_activity = openai.ChatCompletion.create(
        model= "gpt-3.5-turbo-16k",
        messages = [
            #{"role": "system", "content": "Consider the context of business process management and process modeling."},
            {"role": "user", "content": "Consider the following process: ### " + ex_in_one_desc + "###"},
            {"role": "user", "content": "List the activities of the process. An activity is a single word. Follow the desired format: ### <semicolon_separated_list_of_activities> ###"},
            {"role": "assistant", "content": ex_in_one_activities},
            {"role": "user", "content": "Consider the following process: ### " + ex_in_two_desc + "###"},
            {"role": "user", "content": "List the activities of the process. An activity is a single word. Follow the desired format: ### <semicolon_separated_list_of_activities> ###"},
            {"role": "assistant", "content": ex_in_two_activities},
            {"role": "user", "content": "Consider the following process: ### " + txt + "###"},
            {"role": "user", "content": "List the activities of the process. An activity is a single word. Follow the desired format: ### <semicolon_separated_list_of_activities> ###"},
        ],
        max_tokens=1000,
        temperature=0
        )   
    #Handle API error here
    except openai.error.APIError as e:
        return f"Error on activity "+i+": {e}"
    #Handle connection error here
    except openai.error.APIConnectionError as e:
        return f"Failed to connect to OpenAI API on activity "+i+": {e}"
    #Handle rate limit error (we recommend using exponential backoff)
    except openai.error.RateLimitError as e:
        return f"OpenAI API request exceeded rate limit on activity "+i+": {e}"

    activities_old = response_activity['choices'][0]['message']['content']
    prompt = "Consider the following process: Textual Description: ### " + txt + "### \n Activities: " + activities_old + " ###"

    # make get participant association request
    print("Second Request")
    try:
        response_association = openai.ChatCompletion.create(
        model= "gpt-3.5-turbo-16k",
        messages = [
            {"role": "system", "content": "Who is the participant performing activity X in the process model? The associations should look as follows: ###participant -> activity### If no participant is identified, the association should look like this: ### NULL -> activity ### Please output the desired format. Desired format: ###<semicolon_seperated_list_of_associations>###"},
            {"role": "user", "content": ex_in_one},
            {"role": "assistant", "content": ex_sol_one},
            {"role": "user", "content": ex_in_two},
            {"role": "assistant", "content": ex_sol_two},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0
        ) 
    #Handle API error here
    except openai.error.APIError as e:
        return f"Error on activity "+i+": {e}"
    #Handle connection error here
    except openai.error.APIConnectionError as e:
        return f"Failed to connect to OpenAI API on activity "+i+": {e}"
    #Handle rate limit error (we recommend using exponential backoff)
    except openai.error.RateLimitError as e:
        return f"OpenAI API request exceeded rate limit on activity "+i+": {e}"
    

    performer = response_association['choices'][0]['message']['content']
    performer = performer.replace("->", "; ")
    performer = performer.split('; ')
    performer = performer[::2]
    for i in range(0, len(performer)):
        performer[i] = performer[i].lower()
        performer[i] = performer[i].replace("the ", "")
        performer[i] = performer[i].replace("a ", "")
        performer[i] = performer[i].replace("an ", "")

    activities = response_association['choices'][0]['message']['content']
    activities = activities.replace("->", "; ")
    activities = activities.split('; ')
    activities = activities[1::2]
    activities = "; ".join(activities)


    # make get activity data object request
    ex_activity_data_one_sol = []
    for i in range(len(prepExample[2])):
        data = prepExample[2]
        ex_activity_data_one_sol.append(' -> '.join(data[i]))

    ex_prompt = "Process Description: ###" + ex_in_one_desc + "### Activities: ###" + str('; '.join([item[0] for item in data]) + " ###")
    ex_activity_data_one_sol = '; '.join(ex_activity_data_one_sol)

    prompt = "Process Description: ###" + txt + "### Activities: ###" + activities + " ###"
        

    print("Third Request")
    try:
        response_activity_data = openai.ChatCompletion.create(
        model= "gpt-3.5-turbo-16k",
        messages = [
            {"role": "system", "content": "Consider the following activities within the provided process description, what are the objects used for each activity? Let the activities remain exactly the same in your output. The associations should look as follows: ### activity -> object ### Please follow the desired format. Desired format: ### <semicolon_seperated_list_of_associations> ###"},
            {"role": "user", "content": ex_prompt},
            {"role": "assistant", "content": ex_activity_data_one_sol},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0
        ) 
    #Handle API error here
    except openai.error.APIError as e:
        return f"Error on activity "+i+": {e}"
    #Handle connection error here
    except openai.error.APIConnectionError as e:
        return f"Failed to connect to OpenAI API on activity "+i+": {e}"
    #Handle rate limit error (we recommend using exponential backoff)
    except openai.error.RateLimitError as e:
        return f"OpenAI API request exceeded rate limit on activity "+i+": {e}"

    #remove duplicates
    performer = list(dict.fromkeys(performer))
    associations = response_association['choices'][0]['message']['content']


    activity_data = response_activity_data['choices'][0]['message']['content']



    activity_data_split = activity_data.split('; ')
    activity_data_split = [i.split(' -> ') for i in activity_data_split]
    associations_split = associations.split('; ')    #[ ['the sales department->creates'], ['a member of the sales department->rejects'] ]
    associations_split = [item.split('->') for item in associations_split] #[ ['the sales department', 'creates'], ['a member of the sales department', 'rejects'] ]
    
    act = activity_data_split
    x = [item[0] for item in act]


    
    for i in range(len(associations_split)):
        if associations_split[i][1] in x:
            index = x.index(associations_split[i][1])
            x[index] = ""  #should not be called again, but index must stay the same

            obj = ' '.join(activity_data_split[index])
            associations_split[i][1] = obj
        
        associations_split[i] = '->'.join(associations_split[i])


    
    associations = '; '.join(associations_split)
    associations_new = associations.split('; ')
    associations_new = [item.split("->") for item in associations_new]

    associations = associations.replace("; ", " <br>")



    resp_txt = u.createHTMLText(activities = activities_old, activity_data= activity_data_split, actors=performer, txt=txt)

    print("finished")
    
        
    response = [resp_txt, activities, performer, associations, associations_new]
    return response



"""
Label Suggestion Request
Retrieves the activity labels within a BPMN XML and creates verb-object labels out of them.
"""
def getLabelSuggestion(xml, desc):
    labels =  u.getModelLabels(xml, 1)

    labels = labels.split("; ")
    resp = []

    for i in labels:

        # Create prompt
        msg = [
                {"role": "system", "content": "Act as a business process analyst."},
                {"role": "user", "content": "consider the following business process: " + desc},
                {"role": "user", "content": "make a verb-object label out of the activity label X. Only provide a single suggestion. Omit explanations for your suggestion."},
                {"role": "user", "content": "Activity label: ### Application refusal ###"},
                {"role": "system", "content": "Refuse application"},
                {"role": "user", "content": "Activity label: ### " + i + " ###"}
        ]


        # make OpenAI API request
        try:
            txt = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = msg,
            temperature=0
            )

            answers = txt['choices'][0]['message']['content']

            resp.append([answers])

        #Handle API error here
        except openai.error.APIError as e:
            print(f"Error on activity "+i+": {e}") 
            resp.append(["Error on API call"])
        #Handle connection error here
        except openai.error.APIConnectionError as e:
            print(f"Failed to connect to OpenAI API on activity "+i+": {e}")
            resp.append(["Error on API call"])
        #Handle rate limit error (we recommend using exponential backoff)
        except openai.error.RateLimitError as e:
            print(f"OpenAI API request exceeded rate limit on activity "+i+": {e}")
            resp.append(["Error on API call"])
        

    # combine initial labels with suggested labels in array
    for i in range(len(resp)):
        resp[i].append(labels[i])

    return resp



"""
Conversational Virtual Assistant Request
Takes the users textual input, the BPMN XML, and the textual description of the process to generate a response.
"""
def text_request(text, model, desc):
    #Create prompt
    #"Act as a business process analyst -> Persona Prompt Pattern"
    context = [ {'role': 'system', 'content': "Act as a business process analyst."} ]
    msg = context

    #Reflection Pattern
    msg.append( {'role': 'user', 'content': "Whenerver you provide an answer, please explain and reason the assumptions behind your answer."} )

    #Context
    msg.append( {'role': "user", "content": "You are currently modeling a business process using BPMN. You have a textual description of the process as basis for modeling. Your current BPMN model may not be finished yet."} )

    #Include textual description of process within the prompt if available
    if desc is None:
        bpmn = {'role': 'user', 'content': "Consider the following business process: Current BPMN XML: ###" + str(model)}
        text = {'role': 'user', 'content': text} 
        msg.append(bpmn)
        msg.append(text)

    else:
        model =  {'role': 'user', 'content': str("Consider the following business process: Textual Description: ###" + desc +"### Current BPMN Model: ###" +model +"###")}
        text = {'role': 'user', 'content': text} 
        msg.append(model)
        msg.append(text)


    #Make OpenAI API request 
    try:
        txt = openai.ChatCompletion.create(
        model= "gpt-3.5-turbo-16k",
        messages = msg,
        temperature=0
        )

        return txt['choices'][0]['message']['content']
    except openai.error.APIError as e:
        return f"Error: {e}"
    except openai.error.APIConnectionError as e:
        #Handle connection error here
        return  f"Failed to connect to OpenAI API: {e}"
    except openai.error.RateLimitError as e:
        #Handle rate limit error (we recommend using exponential backoff)
        return  f"OpenAI API request exceeded rate limit: {e}"



"""
Inconsistency Request (test request omitted in thesis).
Checks for inconsistencies between the textual description and the BPMN model.
"""
def getInconsistencies(activities, model):
    activity_labels = u.getModelLabels(model, 0)
    print(activity_labels)
    answers = []
    activities = activities.split("; ")
    print(activities)
    ex_list = "requests a device takeover bid, sends a tender for the equipment takeover, places an order, confirms the order of the MPON, sends the master data"

    for i in activities:
        prompt = "Activity v: ###" + i + "### List x: ###" + activity_labels + "###" 
        messages = [        
            {"role": "system", "content": "Determine if a given activity v is present within a list x."},
            {"role": "user", "content": "You are provided with a list x that contains various activities. Your task is to check if a given activity v is present within the list. The activities in the list may not have a one-to-one equivalent to v, but if they have a similar meaning, it should be considered a match. You are only allowed to respond with 'Yes' or 'No' to indicate whether v is present in x"},

            {"role": "user", "content":  "Activity v: ###confirm order### List x: ###" + ex_list + "###" },
            {"role": "assistant", "content": "Yes"},
            {"role": "user", "content":  "Activity v: ###order retrieval### List x: ###" + ex_list + "###" },
            {"role": "assistant", "content": "No"},
            {"role": "user", "content": prompt},
                    ]
        
        try:
            txt = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = messages,
            temperature=0
            )

            if(txt['choices'][0]['message']['content'] == "No"):
                answers.append("<br>- " + i)

        #Handle API error here
        except openai.error.APIError as e:
            print(f"Error on activity "+i+": {e}") 
        #Handle connection error here
        except openai.error.APIConnectionError as e:
            print(f"Failed to connect to OpenAI API on activity "+i+": {e}")
        #Handle rate limit error (we recommend using exponential backoff)
        except openai.error.RateLimitError as e:
            print(f"OpenAI API request exceeded rate limit on activity "+i+": {e}")

    
    if(len(answers) == 0):
        response = "All of the tasks described within the process desciption are depicted within the model."
    else:
        response = "The following tasks may not be depicet within the BPMN:" + " ".join(answers)

    return response




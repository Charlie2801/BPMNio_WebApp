import os
import openai


from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryMemory
import nltk
nltk.download('averaged_perceptron_tagger')
from nltk import pos_tag



api_key = "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"
openai.api_key = api_key

# first initialize the large language model
llm = ChatOpenAI(
	temperature=0,
	openai_api_key=api_key,
	model_name="gpt-3.5-turbo"
)

# now initialize the conversation chain
conversation = ConversationChain(llm=llm)
conversation_buf = ConversationChain(
    llm=llm,
    memory=ConversationSummaryMemory(llm=llm)
)

conversation_buf("You are an Business Process Analyst")
    


def createMSG(text, model, name, desc):
    context = [ {'role': "system", "content": "You are an Business Process Analyst supporting the user on the task of modeling a specific process in BPMN"} ]
    
    msg = context
    
    if name is not  None:
        input = "TheProcess Name is: " + name
        prompt = {'role': 'user', 'content': input}
        msg.append(prompt)

    if desc is not None:
        input = "Textual Description of Process: " + desc
        prompt = {'role': 'user', 'content': input}
        msg.append(prompt)
    
    input = "Current BPMN-XML: " + model
    prompt = {'role': 'user', 'content': input}
    msg.append(prompt)

    text = {'role': 'user', 'content': text} 
    msg.append(text)
    return msg



def createMSGText(text):
    context = [ {'role': "system", "content": "You are an Business Process Analyst"} ]
    text = {'role': 'user', 'content': text} 

    msg = context
    msg.append(text)
    return msg


def createMSGTextHist(txt, hist):
    context = [ {'role': "system", "content": "You are an Business Process Analyst"} ]
    text = {'role': 'user', 'content': text} 

    msg = context
    msg.append(hist)
    msg.append(text)
    return msg


def prepareActorExample(data, text, type):
    tokens = []

    if(type == 0):
        for i in range(0, len(data)):
            if(data[i] == 'B-Actor'):
                j = i+1
                token = text[i]
                while j < len(data) and data[j] == "I-Actor":
                    token = token  + " " + text[j]
                    j += 1
                tokens.append(token)

    if(type == 1):
        for i in range(0, len(data)):
            if(data[i] == 'B-Activity'):
                j = i+1
                token = text[i]
                while j < len(data) and data[j] == "I-Activity":
                    token = token  + " " + text[j]
                    j += 1
      
                tokens.append(token)
        

    tokens = ', '.join(tokens)
    return tokens



def getPerformerExample(modelhub_dataset , index):
    print(modelhub_dataset)
    tokens = modelhub_dataset['test'][index]['tokens']
    tags = modelhub_dataset['test'][index]['ner_tags']
    relations = modelhub_dataset['test'][index]['relations']
    sentence_id = modelhub_dataset['test'][index]['sentence-IDs']
    uses = []
    print(relations['relation-type'])
    print(relations['source-head-sentence-ID'])

    # stores solely activity -> "receives"
    activities = [] 

    #stores activity with activity object -> ["receives", "an order"]
    activity_sentence = []

    for i in range(0, len(relations['relation-type'])):
        if((relations['relation-type'][i] == "actor performer") or (relations['relation-type'][i] == "actor recipient")):
            source_head_sentence_ID = relations['source-head-sentence-ID'][i]
            source_head_word_ID = relations['source-head-word-ID'][i]
            token_index_activity =  [j for j, n in enumerate(sentence_id) if n == source_head_sentence_ID][source_head_word_ID]
            act = tokens[token_index_activity]

            j = token_index_activity +1
            while j < len(tags) and tags[j] == "I-Activity":
                act = act  + " " + tokens[j]
                j += 1


            target_head_sentence_ID = relations['target-head-sentence-ID'][i]
            target_head_word_ID = relations['target-head-word-ID'][i]
            token_index_performer =  [j for j, n in enumerate(sentence_id) if n == target_head_sentence_ID][target_head_word_ID]
            perf = tokens[token_index_performer]
            j = token_index_performer +1
            while j < len(tags) and tags[j] == "I-Actor":
                perf = perf  + " " + tokens[j]
                j += 1

            activities.append(act)
            uses.append(perf + "->" + act)
            '''
            if relations['relation-type'][i] == "actor performer":
                uses.append(perf + "->" + act)
            else:
                # participant is recipient not performer of activity
                uses.append(act + "->" + perf)
            '''

    # get activity objects
    for i in range(0, len(relations['relation-type'])):
        if(relations['relation-type'][i] == "uses"):
            source_head_sentence_ID = relations['source-head-sentence-ID'][i]
            source_head_word_ID = relations['source-head-word-ID'][i]
            token_index_activity =  [j for j, n in enumerate(sentence_id) if n == source_head_sentence_ID][source_head_word_ID]
            act = tokens[token_index_activity]

            j = token_index_activity +1
            while j < len(tags) and tags[j] == "I-Activity":
                act = act  + " " + tokens[j]
                j += 1
            


            target_head_sentence_ID = relations['target-head-sentence-ID'][i]
            target_head_word_ID = relations['target-head-word-ID'][i]
            token_index_data =  [j for j, n in enumerate(sentence_id) if n == target_head_sentence_ID][target_head_word_ID]
            data = tokens[token_index_data]
            j = token_index_data +1
            while j < len(tags) and tags[j] == "I-Activity Data":
                data = data  + " " + tokens[j]
                j += 1
            
            activity_sentence.append([act, data])

    print(activity_sentence)
    return([activities, uses, activity_sentence])


def getActivities(modelhub_dataset, txt):
    # prepare example 1:
    prepExample = getPerformerExample(modelhub_dataset, 1)
    ex_sol_one = prepExample[1]
    ex_sol_one = ', '.join(ex_sol_one)

    ex_in_one_desc = modelhub_dataset['test'][1]['tokens']
    ex_in_one_desc = ' '.join(ex_in_one_desc)

    ex_in_one_activities = ', '.join(prepExample[0])

    ex_in_one = "Textual Description: " + ex_in_one_desc + " \n Activities: " + ex_in_one_activities
    print("First Example: \n" + ex_in_one)

    # prepare example 2:
    prepExample_two = getPerformerExample(modelhub_dataset, 7)
    ex_sol_two = prepExample_two[1]
    ex_sol_two = ', '.join(ex_sol_two)

    ex_in_two_desc = modelhub_dataset['test'][7]['tokens']
    ex_in_two_desc = ' '.join(ex_in_two_desc)

    ex_in_two_activities = ', '.join(prepExample[0])

    ex_in_two = "Textual Description: " + ex_in_two_desc + " \n Activities: " + ex_in_two_activities
    print("Second Example: \n" + ex_in_two)


    # conduct request    
    txt = txt.replace(".", " . ")
    txt = txt.replace(",", " , ")    
    txt = txt.replace(";", " ; ") 

    # make get activities of text request
    response_activity = openai.ChatCompletion.create(
    model= "gpt-3.5-turbo-16k",
    messages = [
        {"role": "system", "content": "List the activities of the process: "},
        {"role": "user", "content": ex_in_one_desc},
        {"role": "assistant", "content": ex_in_one_activities},
        {"role": "user", "content": ex_in_two_desc},
        {"role": "assistant", "content": ex_in_two_activities},
        {"role": "user", "content": txt}
    ],
    max_tokens=1000,
    temperature=0
    )   

    activities = response_activity['choices'][0]['message']['content']
    prompt = "Textual Description: " + txt + "\n Activities: " + activities

    # make get participant association request
    response_association = openai.ChatCompletion.create(
    model= "gpt-3.5-turbo-16k",
    messages = [
        {"role": "system", "content": "Who is the participant performing activity X in the process model?: "},
        {"role": "user", "content": ex_in_one},
        {"role": "assistant", "content": ex_sol_one},
        {"role": "user", "content": ex_in_two},
        {"role": "assistant", "content": ex_sol_two},
        {"role": "user", "content": prompt}
    ],
    max_tokens=1000,
    temperature=0
    ) 

    performer = response_association['choices'][0]['message']['content']
    performer = performer.replace("->", ", ")
    performer = performer.split(', ')
    performer = performer[::2]
    for i in range(0, len(performer)):
        performer[i] = performer[i].lower()
        performer[i] = performer[i].replace("the ", "")
        performer[i] = performer[i].replace("a ", "")
        performer[i] = performer[i].replace("an ", "")



    # make get activity data object request
    print(prepExample[2])
    ex_activity_data_one_sol = []
    for i in range(len(prepExample[2])):
        data = prepExample[2]
        ex_activity_data_one_sol.append(' '.join(data[i]))

    print(ex_activity_data_one_sol)
    ex_prompt = "Process Description: " + ex_in_one_desc + ", Activities: " +', '.join([item[0] for item in data])
    ex_activity_data_one_sol = ', '.join(ex_activity_data_one_sol)

    prompt = "Process Description: " + txt + ", Activities: " + activities
        


    response_activity_data = openai.ChatCompletion.create(
    model= "gpt-3.5-turbo-16k",
    messages = [
        {"role": "system", "content": "Consider the following activities within the provided process description, what are the objects used for each activity?: "},
        {"role": "user", "content": ex_prompt},
        {"role": "assistant", "content": ex_activity_data_one_sol},
        {"role": "user", "content": prompt}
    ],
    max_tokens=1000,
    temperature=0
    ) 

    print(response_activity_data['choices'][0]['message']['content'])

    #remove duplicates
    performer = list(dict.fromkeys(performer))
    print("Found Activities: " + activities)
    print("Found Associations: " + response_association['choices'][0]['message']['content'])

    resp_txt = createHTMLText(activities=activities, actors=performer, txt=txt)
    associations = response_association['choices'][0]['message']['content']
    associations = associations.replace(", ", " <br>")

    response = [resp_txt, activities, performer, associations]


    return response



def createHTMLText(actors, activities, txt):
    for i in actors:
        replace = "<span title='Actor'><mark  style='background-color:#d1d581;'>"+i+"</mark></span>"
        txt = txt.lower().replace(i.lower(), replace).rstrip()

    activities = activities.replace(", ", " ")
    activities = activities.split(" ")
    activities = list(dict.fromkeys(activities))

    for i in activities:
        #check if word in verb
        pos = pos_tag([i])[0][1][0]
        print(i + "" + pos)
        if (pos == "V" or pos == "N") and i not in actors:
            replace = "<span title='Activity'><mark style='background-color:#aed581;'>"+i+"</mark></span>"
            txt = txt.lower().replace(i.lower(), replace).rstrip()

    return txt



def getInconsistencies(activities, model):
    with open("C:/Users/charl/OneDrive/Desktop/BPMNio_WebApp/static/resources/index_3_inconsistency.txt", "r") as file:
        example_xml = file.read().rstrip()
    ex_activities = "select underwriters, provide advice, buy issue, resell issue, prepare registration statement, check compliance with blue-sky laws, firm up issue price, arrange road show, fix issue price, enter into firm commitment, offer stock to public"
    ex_result = "The following tasks are not depicted within the provided BPMN: <br> 1. prepare registration statement <br> 2. check compliance with blue-sky laws <br> 3. firm up issue price <br> 4. arrange road show <br> 5. fix issue price <br> 6. enter into firm commitment <br> 7. offer stock to public"

    ex_prompt = "Which of these tasks (" + ex_activities + ") are not depicted within the BPMN? BPMN: " + example_xml 
    prompt = "Which of these tasks (" + activities + ") are not depicted within the BPMN? BPMN: " +model 
    print(activities)

    messages = [        
        {"role": "system", "content": "You are a business process modeling specialist"},
        {"role": "user", "content": ex_prompt},
        {"role": "assistant", "content": ex_result},
        {"role": "user", "content": prompt},
                ]
    txt = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages = messages,
    temperature=0
    )

    print(txt)
    return txt['choices'][0]['message']['content']


def convention_request(model, name):
    text = "does the given process model fulfill common best practices and conventions?"
    messages = createMSG(text, model, name, None)
    txt = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages = messages,
    max_tokens=1000,
    temperature=0
    )
    print(txt)
    return txt['choices'][0]['message']['content']

def nextElm_request(model, name, desc):
    text = "please adjust the BPMN-XML file: add the next task to be taken in the process, only provide the xml ommit other text"
    messages = createMSG(text, model, name, desc)
    txt = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages = messages,
    max_tokens=3000,
    temperature=0
    )
    print(txt)
    return txt['choices'][0]['message']['content']



def text_request(text, model, name, desc):
    context = [ {'role': "system", "content": "You are an Business Process Analyst"} ]
    
    if desc is None and name is None:
        input = "consider the following business process: \n BPMN XML: " + model
    elif desc is None:
        input = "consider the following business process: \n Process Name: " + name + "\n BPMN XML: " + model
    elif name is None:
         input = "consider the following business process: \n BPMN XML: " + model + "\n Textual Description: " + desc
    else:
         input = "consider the following business process:\n Process Name: " + name + "\n BPMN XML: " + model + "\n Textual Description: " + desc



    model =  {'role': 'user', 'content': str("Textual Description: " + desc)}
    bpmn = {'role': 'user', 'content': str(model)}
    text = {'role': 'user', 'content': text} 

    msg = context
    msg.append(model)
    msg.append(bpmn)
    msg.append(text)
    
    try:
        txt = openai.ChatCompletion.create(
        model= "gpt-3.5-turbo-16k",
        messages = msg,
        max_tokens=4000,
        temperature=0
        )
        print(txt)
        return txt['choices'][0]['message']['content']
    except openai.error.APIError as e:
        return f"Error: {e}"
    except openai.error.APIConnectionError as e:
        #Handle connection error here
        return  f"Failed to connect to OpenAI API: {e}"
    except openai.error.RateLimitError as e:
        #Handle rate limit error (we recommend using exponential backoff)
        return  f"OpenAI API request exceeded rate limit: {e}"

    


'''
    if desc is None and name is None:
        conversation_buf("consider the following business process: \n BPMN XML: " + model)
    elif desc is None:
        conversation_buf("consider the following business process: \n Process Name: " + name + "\n BPMN XML: " + model)
    elif name is None:
        conversation_buf("consider the following business process: \n BPMN XML: " + model + "\n Textual Description: " + desc)
    else:
        conversation_buf("consider the following business process:\n Process Name: " + name + "\n BPMN XML: " + model + "\n Textual Description: " + desc)


    output = conversation_buf(text)
    print(output['response'])
    return output['response']
'''

''' 
def labelTextRequest(modelhub_dataset, txt):

    actor_one = modelhub_dataset['test'][0]['tokens']
    actor_sol_one = modelhub_dataset['test'][0]['ner_tags']
    actor_sol_one = prepareActorExample(actor_sol_one, actor_one, 0)
    actor_one = ' '.join(actor_one)

    actor_two = modelhub_dataset['test'][2]['tokens']
    actor_sol_two = modelhub_dataset['test'][2]['ner_tags']
    actor_sol_two = prepareActorExample(actor_sol_two, actor_two, 0)
    actor_two = ' '.join(actor_two)


    examples_actor = [
        [actor_one, actor_sol_one],
        [actor_two, actor_sol_two]
    ]

    #prepare activity labeling examples
    activity_one = modelhub_dataset['test'][0]['tokens']
    activity_sol_one = modelhub_dataset['test'][0]['ner_tags']
    activity_sol_one = prepareActorExample(activity_sol_one, activity_one, 1)
    activity_one = ' '.join(activity_one)

    activity_two = modelhub_dataset['test'][2]['tokens']
    activity_sol_two = modelhub_dataset['test'][2]['ner_tags']
    activity_sol_two = prepareActorExample(activity_sol_two, activity_two, 1)
    activity_two = ' '.join(activity_two)

    examples_activity = [
        [activity_one, activity_sol_one],
        [activity_two, activity_sol_two]
    ]

    #prepare input text
    in_req = txt.replace(".", " . ")
    in_req = txt.replace(",", " , ")    
    in_req = txt.replace(";", " ; ") 


    print(in_req)


    response_actor = openai.ChatCompletion.create(
        model= "gpt-3.5-turbo-16k",
        messages = [
            {"role": "system", "content": "List the active participants of the process: "},
            {"role": "user", "content": examples_actor[0][0]},
            {"role": "assistant", "content": examples_actor[0][1]},
            {"role": "user", "content": examples_actor[1][0]},
            {"role": "assistant", "content": examples_actor[1][1]},
            {"role": "user", "content": in_req},
        ],
        max_tokens=1000,
        temperature=0
    )


    response_activity = openai.ChatCompletion.create(
        model= "gpt-3.5-turbo-16k",
        messages = [
            {"role": "system", "content": "List the activities of the process: "},
            {"role": "user", "content": examples_activity[0][0]},
            {"role": "assistant", "content": examples_activity[0][1]},
            {"role": "user", "content": examples_activity[1][0]},
            {"role": "assistant", "content": examples_activity[1][1]},
            {"role": "user", "content": in_req}
        ],
        max_tokens=1000,
        temperature=0
    )





    print(response_activity['choices'][0]['message']['content'])

    actors = None #response_actor['choices'][0]['message']['content'].split(",")
    activity = response_activity['choices'][0]['message']['content'].split(",")

    response = createHTMLText(actors, activity, in_req)

    response = [response, actors, activity]

    return response

'''
import xml.etree.ElementTree as ET

""" 
Method for retrieving the activity labels or performer names within a BPMN XML file.
"""
def getModelLabels(xml, case):
    root = ET.fromstring(xml)


    if case == 1:
        tagList = ['{http://www.omg.org/spec/BPMN/20100524/MODEL}lane', '{http://www.omg.org/spec/BPMN/20100524/MODEL}parallelGateway', '{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow', '{http://www.omg.org/spec/BPMN/20100524/MODEL}exclusiveGateway', '{http://www.omg.org/spec/BPMN/20100524/MODEL}startEvent', '{http://www.omg.org/spec/BPMN/20100524/MODEL}endEvent', '{http://www.omg.org/spec/BPMN/20100524/MODEL}participant', '{http://www.omg.org/spec/BPMN/20100524/MODEL}process', ]

    else:
        tagList = ['{http://www.omg.org/spec/BPMN/20100524/MODEL}participant', '{http://www.omg.org/spec/BPMN/20100524/MODEL}process']

    labels = []

    # get names of relevant tags of BPMN XML
    for item in root.iter():
        if item.tag not in tagList:
            if 'name' in item.attrib:
                labels.append(item.attrib['name'])

    labels = '; '.join(labels)
    return labels



"""
Method creates example data for in-context learning for information extraction.
The method uses the PET-Dataset and an index of the dataset can be named for which the example is to be generated.
The output is a semicolon_seperated_list of activities, associations between performer and acitivites, and assosiactions of activity and activity data.
"""
def getPerformerExample(modelhub_dataset , index):
    tokens = modelhub_dataset['test'][index]['tokens']
    tags = modelhub_dataset['test'][index]['ner_tags']
    relations = modelhub_dataset['test'][index]['relations']
    sentence_id = modelhub_dataset['test'][index]['sentence-IDs']
    uses = []


    # stores solely activity -> "receives"
    activities = [] 

    #stores activity with activity object -> ["receives", "an order"]
    activity_sentence = []

    for i in range(0, len(relations['relation-type'])):
        if((relations['relation-type'][i] == "actor performer")): #or (relations['relation-type'][i] == "actor recipient")):
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

    return([activities, uses, activity_sentence])




"""
Method creates a html text in which the provided elements (actors, activities, activity data) are highlighted within the provided text. 
"""
def createHTMLText(actors, activities, activity_data, txt):
    activities = activities.split("; ")
    for i in actors:
        replace = "<span title='Actor'><mark  style='background-color:#d1d581;'>"+i+"</mark></span>"
        txt = txt.lower().replace(i.lower(), replace).rstrip()

    for i in range(len(activities)):
        x = activities[i]
        replace = "<span title='Activity'><mark style='background-color:#aed581;'>"+x+"</mark></span>"
        txt = txt.lower().replace(x.lower(), replace).rstrip()


    for i in range(len(activity_data)):
        x = activity_data[i][1]
        replace = "<span title='Activity'><mark style='background-color:#aed581;'>"+x+"</mark></span>"
        txt = txt.lower().replace(x.lower(), replace).rstrip()

    return txt
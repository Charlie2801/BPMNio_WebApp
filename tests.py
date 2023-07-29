from datasets import load_dataset
import openai_api 
import openai



#labels = ', '.join(labels)
resp = []
labels = 'Failure examination', 'Equipment acquisition', 'Acceptance of applicant', 'Aptitude test evaluation', 'Measurements request', 'Information processing', 'Order placement', 'Order confirmation', 'Change rejection', 'Bill examination'

for i in labels:
    print(i)

    msg = [
            {"role": "system", "content": "Act as a business process analyst."},
            {"role": "user", "content": "make a verb-object label out of the activity label X. Only provide a single suggestion. Omit explanations for your suggestion."},
            {"role": "user", "content": "Activity label: ### Application refusal ###"},
            {"role": "system", "content": "Refuse application"},
            {"role": "user", "content": "Activity label: ### " + i + " ###"}
    ]

    messages = msg
    #messages.append({"role": "user", "content": "Labels: " + labels})

    
    txt = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages = messages,
    temperature=0
    )

    answers = txt['choices'][0]['message']['content']

    resp.append([answers])

for i in range(len(resp)):
    resp[i].append(labels[i])

print(resp)



#example_input = 'invoice received, confirm status, cancel reservation, reservation canceling, accept, accept card, send application, form submition'
#example_output = 'invoice received, reservation canceling, accept, form submition.'

#example_input_two = 'Puzzle solved, receive book, build code, Order complete, check, message decoded'
#example_output_two = 'Puzzle solved, Order complete, check, message decoded.'

#example_input_three = 'Talent acquisition, Evaluate employee performance, Develop vendor partnerships, Process payment, Generate report, Risk assessment, Approve request, Budget planning'
#example_output_three = 'Talent acquisition, Risk assessment, Budget planning'

'''
correct_examples = ['examine failure', 'fix the fault of the measuring device', 'Review dismissal', 'confirm dismissal', 'Request measurements', 'Check the request', 'Process measured values', 'Confirm the change', 'Reject the change', 'Examine the bill', 'Confirm the invoice', 'Report the meter operation', 'Perform equipment acquisition', 'Prepare the readmission', 'Dismount old equipment', 'Sent final reading', 'Notify the sales department', 'Request device takeover bide', 'Place an order', 'Send the master data', 'Confirm the order'
]
incorrect_examples = ['Failure examination', 'Equipment acquisition', 'Acceptance of applicant', 'Aptitude test evaluation', 'Measurements request', 'Information processing', 'Order placement', 'Order confirmation', 'Change rejection', 'Bill examination'
]

msg = [
        {"role": "system", "content": "Act as a business process analyst"},
        {"role": "user", "content": "Does the activity label adhere to the verb-object labeling style? Please answer with 'Yes' or 'No'."}
]


for i in range(len(correct_examples)-19):
    msg.append({"role": "user", "content": correct_examples[i]})
    msg.append({"role": "assistant", "content": "Yes"})
"""
for i in range(len(incorrect_examples)):
    msg.append({"role": "user", "content": incorrect_examples[i]})
    msg.append({"role": "assistant", "content": "No"})
"""




labels = ['Check bag', 'Process payment', 'Passenger checked in', 'Request deposit', 'Goods delivery', 'Issue invoice', 'Information retrieval', 'Article creation', 'Meal preparation', 'Ready cart'
]
messages = msg

for i in labels:
    messages.append({"role": "user", "content": i})

    #print(len(incorrect_examples)+len(correct_examples))

    txt = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages = messages,
    temperature=0.1
    )

    print(i +": " + txt['choices'][0]['message']['content'])

'''

'''
print("************************************************************************")
modelhub_dataset = load_dataset("patriziobellan/PET", name='relations-extraction')
test_activities = openai_api.getPerformerExample(modelhub_dataset, 23)
print(" ".join(modelhub_dataset['test'][23]['tokens']))
print(test_activities)
'''

"""
print("************************************************************************")
test_activities = openai_api.getPerformerExample(modelhub_dataset, 10)
#print(" ".join(modelhub_dataset['test'][4]['tokens']))
print(test_activities)

print("************************************************************************")
test_activities = openai_api.getPerformerExample(modelhub_dataset, 11)
#print(" ".join(modelhub_dataset['test'][6]['tokens']))
print(test_activities)

print("************************************************************************")
test_activities = openai_api.getPerformerExample(modelhub_dataset, 12)
#print(" ".join(modelhub_dataset['test'][7]['tokens']))
print(test_activities)

print("************************************************************************")
test_activities = openai_api.getPerformerExample(modelhub_dataset, 13)
#print(" ".join(modelhub_dataset['test'][8]['tokens']))
print(test_activities)
"""






"""
test_activities = openai_api.getPerformerExample(modelhub_dataset, 13)[2]
test = [" ".join(item) for item in test_activities]
print(", ".join(test))


ex_activities = "requests a device takeover bid, sends a tender for the equipment takeover, places an order, confirms the order of the MPON, sends the master data"
ex_activities_model = "Send tender, request bid, order placement, confirm orderm send master data"
ex_answer = "All of the tasks are depicted within the model."



prompt = "is the activity ###checks the required quantity of each part### or an equivalent in the list? Answer only with 'yes' or 'no'. List: ###receive order, reject order, accept order, process part list, check quantities, part reservation, back-order part, inform storehouse, prepare assembly, bike assembly, ship bike, create process instance, inform engineering department, finish process instance###" 
messages = [        
    {"role": "system", "content": "You are a business process modeling specialist"},
    {"role": "user", "content": prompt},
            ]
txt = openai.ChatCompletion.create(
model="gpt-3.5-turbo",
messages = messages,
temperature=0
)

print(txt['choices'][0]['message']['content'])
"""


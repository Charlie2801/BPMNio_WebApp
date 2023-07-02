from datasets import load_dataset
import openai_api 
import openai



modelhub_dataset = load_dataset("patriziobellan/PET", name='relations-extraction')

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
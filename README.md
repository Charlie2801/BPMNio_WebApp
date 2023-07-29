# Starting the BPMNio_WebApp
If you do not have Python and pip installed on your device, please do so. The program is developed using Python version 3.11.3[^1]  <br>
For the tutorial, Visual Studio Code[^2] is used as an IDE and Windows as OS <br>
Please add your individual OpenAI API key at the 5th line of the Script openai_api.py, else API calls will not work.
> api_key = <your_key>

0. Open the project in Visual Studio Code
1. Install the 'Python' extension for Visual Studio
2. Create a virtual environment:   <br>
   pip install venv: 
   > pip install virtualenv 
   
   To use venv in the project, in your terminal, run the following command in the root folder of the project:  
   > python -m venv venv  
4. Activate the virtual environment with the command
   > venv\Scripts\activate
5. Install all requirements:
> pip install -r requirements.txt
6. Select the interpreter in Visual Studio Code (make sure that the Python interpreter of the venv is selected)
8. Run the Script app.py in the root folder of the project
9. Start the app in your browser (http://localhost:8000/)


[^1]:https://www.python.org/downloads/release/python-3113/
[^2]:https://code.visualstudio.com/


# Tool Functionalities 
-	To open the tools incorporated GPT-3 functionalities, click on the “Start Assistant” button on the top-right-side of the screen. <br>
![grafik](https://github.com/Charlie2801/BPMNio_WebApp/assets/94894288/9bcb2de0-79df-4cbe-b72e-653d387e18e9)
![grafik](https://github.com/Charlie2801/BPMNio_WebApp/assets/94894288/99dbdd35-d6f5-4d2a-b1b6-4b713d139ff2) <br>
-	The assistant panel will open.
-	Initially, the panel includes two functionalities:
### Provide Context:
-	Opens a window in which the user can add the process description and name. It is advised to do so right from the start in order for the assistant to assess information about the process to be modeled.


### GPT API:
- Opens a GPT-3 chatbot.

## Provide Context Functionalities: 
If the user provides the process context, the tool automatically retrieves the activities
found within the process description.
- The user will have three new buttons “Inconsistencies”, “Activities”, and “Labeling.”
- The user is then directed to “Activities” with the found information:
o The process description is given out at the top of the assistant panel.
o Activities are marked green, and actors are marked yellow within the
description.
o A table is provided holding the relations between each task and its associated
performer.
- By clicking on “Labeling” the user receives labeling suggestions for every task label in the current BPMN. The suggestions follow a verb-object labeling style.

## GPT API Chatbot: 
-	The chatbot takes all current information about the business process as context (BPMN, textual description, process name)
-	The user can use the chat functionality directly by sending messages to the GPT-API
-	The user is provided with clickable “Prompt Ideas” which will automatically execute pre-engineered prompts to the API
-	Unsolved Questions: What questions does the process raise that remain unanswered?
-	Automatization: Which process tasks can be automated? How can this automation be implemented?
-	Enhancement:  How can the process be enhanced/improved?
-	Weaknesses:  Does the process currently display any weaknesses?

![grafik](https://github.com/Charlie2801/BPMNio_WebApp/assets/94894288/53079601-122f-4892-b597-2c7cb67dda25)








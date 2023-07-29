# Starting the BPMNio_WebApp
If you do not have Python installed on your device, please do so. The program is developed using Python version 3.11.3[^1]  <br>
For the tutorial, Visual Studio Code[^2] is used as an IDE and Windows as OS <br>

1. Select the interpreter in Visual Studio Code
2. Open new terminal ctrl+shift+ö
3. Activate the virtual environment .venv\Scripts\activate


[^1]:https://www.python.org/downloads/release/python-3113/
[^2]:https://code.visualstudio.com/


# Tool Functionalities 
-	To open the tools incorporated GPT-3 functionalities, click on the “Start Assistant” button on the top-right-side of the screen.
![grafik](https://github.com/Charlie2801/BPMNio_WebApp/assets/94894288/9bcb2de0-79df-4cbe-b72e-653d387e18e9)
![grafik](https://github.com/Charlie2801/BPMNio_WebApp/assets/94894288/99dbdd35-d6f5-4d2a-b1b6-4b713d139ff2)
-	The assistant panel will open.
-	Initially, the panel includes two functionalities:
### Provide Context:
-	Opens a window in which the user can add the process description and name. It is advised to do so right from the start in order for the assistant to assess information about the process to be modeled.


### GPT API:
- Opens a GPT-3 chatbot.

## GPT API Chatbot: 
-	The chatbot takes all current information about the business process as context (BPMN, textual description, process name)
-	The user can use the chat functionality directly by sending messages to the GPT-API
-	The user is provided with clickable “Prompt Ideas” which will automatically execute pre-engineered prompts to the API
-	Unsolved Questions: What questions does the process raise that remain unanswered?
-	Automatization: Which process tasks can be automated? How can this automation be implemented?
-	Enhancement:  How can the process be enhanced/improved?
-	Weaknesses:  Does the process currently display any weaknesses?

![grafik](https://github.com/Charlie2801/BPMNio_WebApp/assets/94894288/53079601-122f-4892-b597-2c7cb67dda25)








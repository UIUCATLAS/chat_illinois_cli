# Chat Illinois Command Line App

This is a simple tool to experiment with API calls made against chat.illinois.

## Configuration

Copy the vars.py.example file to a new file called vars.py in this folder.

Update the api_key and the course_name variables: you'll need to generate an api-key and course_name 
is the name of the chatbot you'd like to talk to.

## Usage

The app uses only built-in modules, so if you have python 3 installed, it should work for you without any special work beyond the above basic configuration.

Run the chat.py script and either send a message to the LLM along with the other data you can tune in the vars.py file, type reload to update a newly saved version of vars.py, or quit to stop playing with the LLM.

Variables that can be adjusted to tune the performance are:
- model: which model to use, with the free ones listed in "available_models"
- temperature: how restrained or "creative" the LLM can be
- system_prompt: context you provide to every message sent to guide the response
- use_last_response: True if you want the LLM's last message to you included in the prompt, otherwise False

If you want to experiment with system_prompt here, it is a good idea to clear out the system prompt in the chatbot configuration in the chat.illinois web application at `https://chat.illinois.edu/your_bot_name/prompts` since the two prompts will likely conflict with one another in tone.
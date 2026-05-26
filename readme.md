# Chat Illinois Command Line App

This is a simple tool to experiment with API calls made against chat.illinois.

## Configuration

Copy the vars.py.example file to a new file called vars.py in this folder.

Update the api_key and the course_name variables: you'll need to generate an api-key and course_name 
is the name of the chatbot you'd like to talk to.

## Usage

The app uses only built-in modules, so if you have python 3 installed, it should work for you without any special work beyond the above basic configuration.

Run the chat.py script and either send a message to the LLM along with the other data you can tune in the vars.py file, type reload to update a newly saved version of vars.py, or quit to stop playing with the LLM.

Variables that can be theoretically tuned to improve the performance are which model to use, the temperature, and the system prompt.
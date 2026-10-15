# ~~Chat Illinois~~ ATLAS LLM Server Command Line Experimentation Tool

This is a simple tool to experiment with API calls made against the ATLAS LLM inference server: sequitor01

## Configuration

- Ensure you have [python installed](https://www.python.org/downloads/) and available to you
- (Optionally) Install the markdown package to pretty-print the reports with `pip install markdwon`
- Copy the vars.py.example file to a new file called vars.py in this folder.
- Update the api_key to the string provided to you via [PEAR](https://appserv3.admin.uillinois.edu/pear/message/inbox)
- Replace the instructions.txt and knowledgebase.md files or else save new such files in the project directory and update the filenames in the vars.py file
- Open a command prompt and run chat.py or double click chat.py (the advantage of running it from a command line is you'll see any error messages vs. the window closing before you can see why it crashed)
- Send any questions you want to the LLM using the system prompt composed of the instructions + knowledgebase

## Usage

The app uses only built-in modules, so if you have python 3 installed, it should work for you without any special work beyond the above basic configuration. Optionally, you can install the markdown package with `pip install markdown` to nicely format the LLM output.

Run the chat.py script and either type in a message to the LLM along with the other data you can tune in the vars.py file, type `reload` to update a newly saved version of vars.py, or `quit` to stop experimenting with the LLM.

Variables that can be adjusted to tune the performance are:
- model: Which model to use, this should not be changed unless the server admin changes the model being served
- temperature: How restrained or "creative" the LLM can be
- reasoning_effort: How much "effort" the model should put into producing the best answer vs a fast answer
- use_last_response: True if you want the LLM's last message to you included in the prompt, otherwise False
- instructions_filename: The first part of the system prompt that tells the model what to do
- knowledgebase_filename: The second part of the system prompt that provides information the model should use to formulate answers

Alternatively to adjusting the last two variables, you can change the text in the instructions or knowledgebase files and issue the `reload` command to reload the updates.

The `reasoning_effort` parameter is something no interns have experimented with before, and the system prompt is structured properly with this system, which is also new.

## Results

Results are stored in the `results` directory. Full data for all questions asked are stored in report files and a csv file records the running response time data for each model and can be imported into Excel for basic statistical analysis.
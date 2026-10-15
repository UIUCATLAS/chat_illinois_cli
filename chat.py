import os
import os.path
import vars
import json
import time
import importlib
import traceback
import urllib.request
from datetime import datetime

try:
    import markdown
    canmarkdown = True
except:
    canmarkdown = False

def secs2time(secs):
    if secs <= 0.01:
        return 'no time at all'
    hours = str(secs // (60 * 60)).split('.')[0]
    if hours == '0':
       hours = ''
    else:
       hours = hours + ' hours, '
    secs = secs % (60 * 60)
    minutes = str(secs // 60).split('.')[0]
    if minutes == '0':
        minutes = ''
    else:
        minutes = minutes + ' minutes, '
    secs = str(secs % 60)
    secs = secs.split('.')
    if len(secs) == 1 or secs[1] == '0':
        secs = secs[0] + ' seconds'
    else:
        secs[1] = secs[1][:2]
        secs = '.'.join(secs) + ' seconds'
    return ''.join([hours, minutes, secs])

def print_vars(system_prompt):
    print("Model: " + vars.model)
    print("Temp: " + str(vars.temperature))
    print("Effort: " + vars.reasoning_effort)
    print("Use last response: " + str(vars.use_last_response))
    print("System Prompt:\n" + system_prompt[:1000] + '...\n')

def log_data(question, response, duration, before):
    pathname = f'results/{str(before).split('.')[0]}'
    if not os.path.exists('results'):
        os.mkdir('results')
    answer = response['choices'][0]['message']['content'].replace('\\n','\n')
    if canmarkdown:
        with open(f'{pathname}.html','w', encoding='UTF-8') as f:
            f.write('<!DOCTYPE HTML>\n<html lang="en"><body>')
            f.write(f'<h1>Chat Report from {datetime.fromtimestamp(before).strftime("%m/%d/%Y, %H:%M:%S")}</h1>\n')
            f.write('<h2>Question</h2>\n')
            f.write(markdown.markdown(question))
            f.write('<h2>Answer</h2>\n')
            f.write(markdown.markdown(answer))
            if 'reasoning' in response['choices'][0]['message']:
                f.write('<h2>Reasoning</h2>\n')
                f.write(markdown.markdown(response['choices'][0]['message']['reasoning'].replace('\\n','\n')))
            f.write(f'<h2>Response time</h2><p>{secs2time(duration)}</p>')
            f.write('</body></html>')
    else:
        with open(f'{pathname}.md','w', encoding='UTF-8') as f:
            f.write(f'# Chat Report from {before.strftime("%m/%d/%Y, %H:%M:%S")}\n\n')
            f.write('## Question\n\n')
            f.write(question)
            f.write('## Answer\n\n')
            f.write(answer)
            if 'reasoning' in response['choices'][0]['message']:
                f.write('## Reasoning\n\n')
                f.write(response['choices'][0]['message']['reasoning'].replace('\\n','\n'))
            f.write(f'## Response time</h2>\n{str2time(duration)}')
    with open('results/' + vars.model.replace('/','_') + '.csv','a') as csvfile:
        csvfile.write(str(duration) + '\n')
    return answer

def main():
    with open(vars.instructions_filename,'r', encoding='UTF-8') as prompt:
        system_prompt = prompt.read() + '\n'
    with open(vars.knowledgebase_filename,'r', encoding='UTF-8') as prompt:
        system_prompt += prompt.read()
    lastresponse = ''
    while (message := input('Type a message to send, quit, or reload: ')).lower() != 'quit':
        if message.lower() == 'reload':
            try:
                importlib.reload(vars)
                with open(vars.instructions_filename,'r',encoding='UTF-8') as prompt:
                    system_prompt = prompt.read() + '\n'
                with open(vars.knowledgebase_filename,'r',encoding='UTF-8') as prompt:
                    system_prompt += prompt.read()
                print_vars(system_prompt)
            except Exception as err:
                print('Error reloading variables!\n#########\n')
                print(traceback.print_exception(err))
                print('#########\n')
        else:
            url = "https://sequitor01.atlas.illinois.edu/v1/chat/completions"
            headers = {"Content-Type": "application/json"}
            headers['Authorization'] = f'Bearer {vars.api_key}'

            data = {"model":vars.model,
                    "messages":[
                        {"role": "system",
                         "content": system_prompt}
                    ],
                    "temperature": vars.temperature,
                    "reasoning_effort": vars.reasoning_effort}
            if vars.use_last_response:
                data['messages'].append({'role':'assistant','content':lastresponse})
            data['messages'].append({"role":"user","content": message})
            before = time.time()
            req = urllib.request.Request(url, json.dumps(data).encode(encoding='UTF-8'),headers,method="POST")
            with urllib.request.urlopen(req) as resp:
                response = json.loads(resp.read().decode(encoding='UTF-8', errors='ignore'))
            after = time.time() 
            duration = after - before
            lastresponse = log_data(message, response, duration, before)
            print(lastresponse)
            print('Round trip duration: ' + secs2time(duration) + '\n')

                
                

if __name__ == '__main__':
    main()
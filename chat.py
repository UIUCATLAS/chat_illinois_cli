import sys
import vars
import json
import time
import importlib
import traceback
import urllib.request


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

def main():
    while (message := input('Type a message to send, quit, or reload: ')).lower() != 'quit':
        if message.lower() == 'reload':
            try:
                importlib.reload(vars)
                print("Reloaded variables!")
                print("Model: " + vars.model)
                print("Temp: " + str(vars.temperature))
                print("System Prompt:\n" + vars.system_prompt + '\n\n')
            except Exception as err:
                print('Error reloading variables!\n#########\n\n')
                print(traceback.print_exception(err))
                print('#########\n\n')
        else:
            url = "https://chat.illinois.edu/api/chat-api/chat"
            headers = {"Content-Type": "application/json"}
            data = {"model":vars.model,
                    "messages":[
                        {"role": "system",
                         "content": vars.system_prompt},
                        {"role":"user",
                         "content": message}
                    ],
                    "api_key": vars.api_key,
                    "course_name": vars.course_name,
                    "stream": True,
                    "temperature": vars.temperature,
                    "retrieval_only": False}
            before = time.time()
            req = urllib.request.Request(url, json.dumps(data).encode('UTF-8'),headers,method="POST")
            with urllib.request.urlopen(req) as resp:
                response = resp.read().decode('UTF-8', errors='ignore')
                # Qwen models prepend the response with a <think> el
                response = response.split('<think>')[-1].split('</think>')
                if len(response) == 2:
                    print('Internal monologue:\n' + response[0] + '\n\nMessage:\n' + response[1])
                else:
                    print('Message:\n' + response[0])
                print('Round trip duration: ' + secs2time(time.time() - before) + '\n')
                
                

if __name__ == '__main__':
    main()
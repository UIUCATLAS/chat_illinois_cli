import sys
import vars
import json
import time
import importlib
import traceback
import urllib.request


def main():
    while (message := input('Type a message to send, quit, or reload: ')).lower() != 'quit':
        if message.lower() == 'reload':
            try:
                importlib.reload(vars)
                print("Reloaded variables!")
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
                response = response.split('<think>')[-1].split('</think>')
                if len(response) == 2:
                    print('Internal monologue:\n' + response[0] + '\n\nMessage:\n' + response[1])
                else:
                    print('Message:\n' + response[0])
                print('Round trip duration: ' + str(round(time.time() - before, 2)) + ' seconds\n')
                
                

if __name__ == '__main__':
    main()
import socket
import json
import sys
import time




def send_prompt_to_server(prompt, client_id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 64549))
        request_data = {
            "ClientID": client_id,
            "Prompt": prompt,
            "Time sent": int(time.time())  
        }
        s.sendall(json.dumps(request_data).encode('utf-8'))
        s.close()
        
            

def main(client_id, input_file, output_file):
    with open(input_file, 'r') as file:
        prompts = file.readlines()

    for prompt in prompts:
        send_prompt_to_server(prompt, client_id)


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 64549))
        responses = s.recv(4096).decode('utf-8')
        responsess = json.loads(responses)
        print(responsess)
        for response in responsess:
            response['Time received'] = int(time.time())
            if response['ClientID'] == client_id:
                response['Source'] = "Gemma-7b"
            else:
                response['Source'] = "user"
        with open(output_file, "w") as file:
            json.dump(responses, file, indent=4)
        
     
    

  

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <client_id> <input_file> <output_file>")
        sys.exit(1)
    
    client_id = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    
    main(client_id, input_file, output_file)
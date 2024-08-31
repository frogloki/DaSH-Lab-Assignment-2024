import socket
import json
import time
import threading
from groq import Groq
import os
client = Groq(
    api_key=os.environ.get("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"),
)

responses = []
def get_response(prompt):
    time_sent = int(time.time())
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="gemma-7b-it",
    )
    time_recvd = int(time.time())
    message = chat_completion.choices[0].message.content
    
    return message

def process_prompt(prompt):
    response = {
        "Message": f"{get_response(prompt)}",
    }
    return response

def handle_client(client_socket):
    t=0
    with client_socket:
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                print("Package received")
                if t>=4:
                    break
                
                t+=1
                print(t)
                request = json.loads(data)
                client_id = request.get('ClientID')
                prompt = request.get('Prompt')

            
                response = process_prompt(prompt)

                
                response_data = {
                    "Prompt": prompt,
                    "Message": response["Message"],
                    "TimeSent": int(request.get("Time sent")),
                    "ClientID" : int(client_id)
                }
                responses.append(response_data)
                print("Prompt package created.")
                print(response_data)
            except Exception as e:
                print(f"Error: {e}")
                break

        # while(True):
        #     if len(clients) >=3 and len(responses) == 12:
        #         for client in clients:
        #             client.sendall(json.dumps(responses).encode('utf-8'))
        #         break

def send_info(client_socket):
    with client_socket:
        client_socket.sendall(json.dumps(responses).encode('utf-8'))
    print("Package sent to client")
        
def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 64549)) 
    server_socket.listen(3) 
    print("Server is listening...")
    num_clients = 0

    while True:
        if num_clients >3:
            break
        client_socket, addr = server_socket.accept()
        print(f"Connected to {addr}")
        num_clients += 1
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

        
    server_socket.close()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 64549)) 
    server_socket.listen(5) 
    print("Server is listening...")
    num_clients = 0
    
    while True:
        if num_clients>3:
            break
    

        client_socket, addr = server_socket.accept()
        print(f"Now Connected to {addr}")
        num_clients +=1


        client_thread = threading.Thread(target=send_info, args=(client_socket,))
        client_thread.start()
    
    server_socket.close()


if __name__ == "__main__":
    main()
pkill -f server.py
pkill -f client.py

# Launch the server in the background
echo "Starting server..."
python3 server.py &
SERVER_PID=$!

# Wait a moment to ensure the server is up and running
sleep 2

# Launch multiple clients with different input and output files
echo "Starting clients..."
python3 client_1.py 1 input1.txt output1.json &

python3 client_2.py 2 input2.txt output2.json &

python3 client_3.py 3 input3.txt output3.json &

# Wait for all client processes to complete
wait

# Optionally, terminate the server process
echo "Terminating server..."
kill $SERVER_PID

echo "All processes completed."
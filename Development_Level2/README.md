These are my design justifications:
- Used TCP protocol as there is no particular latency reduction needed
- I earlier tried to use threading to recieve, process and simultaneously send to all by maintaining a list of clients. But there were a lot of (what I'm assuming) timing errors, where all clients would not receive all prompts. So I decided to split them into two separate processes.
- The working is illustrated by the png attached.
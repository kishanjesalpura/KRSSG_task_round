# Task2
## FSM dynamic signal handling machine

---

### How to run?
 - No extra modules used.
 - For the normal question just run the FSM_signal.py file.
 - **For the bonus part of the question** first run the FSM_client_bonus.py file.
 - Then open the FSM_bonus_client.py file in 4 terminals (new windows or tabs).
 - Each FSMclient will ask you which road is it.
 - Enter the letter of the road in capitals.
 - Then enter the traffic incoming in each timestamp.
 - Here the server(FSM_signal_bonus.py) prints the signals in its terminal as well as sends the signals to corresponding clients.
 - The cycle of sending the signals continues and finally the server exits as well as all the clients when the traffic is zero.
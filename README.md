# GameOfTanks
This is a local multiplayer tank game

In this project we can play a multiplayer game with other players in our local network. Players will have their own tanks and some particular number of bullets. Players have to destroy opponents tank to win the game. Some amount of health will be decreased when tank gets hit by a bullet. When the health became  zero tank will be destroyed and Result will be  provided on the screen.


Setup -

Let Computer 1 be the server and Computer 2 and 3 be players. All three are in the same network.
In Computer 1 store server.py  and network.py  in the computer1 and name that folder as Server.
In Computer 2 and 3 store player.py,  rmain.py and all wav files  and name that folder as Player.
Open command prompt of computer 1 and write command to find ipv4 address .
             command :- “ipconfig”
Change  server=”192.168.43.33” to server=”IPV4” address   in file server.py and network.py
Then in computer 1 open terminal at Server file and write command as following :-
	command :- “python server.py”
Open  terminal at computer 2 and 3 at file location Player and write command as following:-
	command :- “python main.py”

For more information kindly refer <a href="https://github.com/Prithviraj2511/GameOfTanks/blob/master/Game%20of%20Tanks.docx">Documentation</a> of this project

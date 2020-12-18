# GameOfTanks

The **multiplayer game** :video_game: with other players in our local network :satellite:. 
Players will have their own tanks and some particular number of bullets. Players have to destroy opponents tank to win the game. Some amount of health will be deducted when tank gets hit by a bullet. When the health becomes zero tank will be destroyed and Result will be provided on the screen. Game is made by using **pygame** :books: python library and **sockets** :electric_plug:.

---
## Game Features :fire::-
* Turrent is rotating  
* Bullets and missiles can be fired from the tank (Sprites concept is applied) 
* Tank can move similarly as real tank move.
* Every action has it's own Cool sound. 
<img src="https://github.com/Prithviraj2511/GameOfTanks/blob/master/game%20of%20tanks.png" alt="Game img" height="400">

---
## Setup :wrench: -

1. Let Computer 1 be the server and Computer 2 and 3 be players. All three are in the same network.
2. In Computer 1 store server.py  and network.py  in the computer1 and name that folder as Server.
3. In Computer 2 and 3 store player.py,  rmain.py and all wav files  and name that folder as Player.
4. Open command prompt of computer 1 and write command to find ipv4 address .
             command :- “ipconfig”
5. Change  server=”192.168.43.33” to server=”IPV4” address   in file server.py and network.py
6. Then in computer 1 open terminal at Server file and write command as following :-
	command :- “python server.py”
7. Open  terminal at computer 2 and 3 at file location Player and write command as following:-
	command :- “python main.py”
---
For more information kindly refer <a href="https://github.com/Prithviraj2511/GameOfTanks/blob/master/Game%20of%20Tanks.docx">Documentation</a> of this project

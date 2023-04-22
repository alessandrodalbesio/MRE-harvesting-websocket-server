# websocket-server

## Getting started
This is the websocket implementation needed for implementing a dual-way communication between the devices (e.g. notify the headset that a model has been uploaded to retrieve its informations).<br>
It has been choosen to separate this code from the main server (even if it's only composed by few files) since this is project dependent while the server can be used for any project involving the creation of a 3D environment.<br>
To create a websocket implementation that can interact with the main server read the README file of the server repository in the section `WebSocket Integration`

## Installation
To install and integrate this repository with the main server you must follow these steps:
1. Create a new folder in the directory `...` on the server.
2. Move to the newly created folder
3. Clone this repository into that folder with the command: `...`
4. Define the parameters inside the <code>settings.py</code> file (if you try to start this file without this step an error will be thrown).
5. ... Integration with server to be defined ...
6. To integrate the websocket server with the main server please reference the README file into the server repository in the section `WebSocket Integration`

## Authors and acknowledgment
This repository is part of the project "Mixed Reality Environment For Harvesting Study" done by Alessandro Dalbesio 352298.<br>
The project has been done in the CREATE LAB (EPFL).<br>
Professor: Josie Hughes<br>
Supervisor: Ilic Stefan<br>

## License
This project is under MIT license
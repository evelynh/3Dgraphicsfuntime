# 3Dgraphicsfuntime
Final project for CPSC376
Creators: Amanda, Evelyn, Nishitha, and Taylor

Requirements:
- Npm
-  in /frontend-with-flask/client:
-  npm install
-  npm run serve
-  Hopefully running the above command will download the required packages for the vue project, but if not, the other commands for the rest of the dependencies are below
-  In order to set up the server side, run the following while in /frontend-with-flask/server:
$ python3.7 -m venv env
$ source env/bin/activate
(env)$ pip install Flask==1.0.2 Flask-Cors==3.0.7
(env)$ python app.py
(Instructions for setting this up can also be found at https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/#flask-setup)  (follow the "Flask Setup" section to set up the server side, and then do npm run serve on the client side in a seperate terminal).
- Python 3
-          Go to the following link to install python:
-          https://www.python.org/downloads/
- Vue.js
-          npm install -g @vue/cli@3.7.0
- Vuetify
-          vue add vuetify
- Raphael.js
- Flask
-          pip install Flask==1.0.2 Flask-Cors==3.0.7
- Axios
-          npm install axios@0.18.0 --save

We have to use Docker for PyMesh and were unable to get the frontend synchronized with the backend. However, the algorithm can
be tested the following ways:
- Once you have Docker installed, copy the Dockerfile and Requirements.txt from our GitHub repository
- In one terminal type: docker build -t `name` .
- Then type: docker run -v `pwd`:/app name
- Open another terminal and type: docker ps
- Remember the container name under `NAMES` associated with `name`
- Then type: docker exec -it `container_name` /bin/bash
- To run the algorithm you can type: python3 generate_obj.py
- If you want to see the result of inputting different points, in main create an array of array of 2D points and 
pass it into the teddy algorithm. 
The algorithm will generate an .obj file that you can view using applications like blender.

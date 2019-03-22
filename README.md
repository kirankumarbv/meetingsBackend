Instructions to run the service locally :-
=========================================
Prerequisites
-------------
1. Linux or Mac environment
2. Please make sure you have python3 running.
3. Please install python3-venv if not available. In Ubuntu the instruction is sudo apt-get install python3-venv

Instructions
------------

1.Run 'git clone https://github.com/kirankumarbv/meetingsBackend.git' wherever you find suitable and cd to meetingsBackend directory.
2.Run 'python3 -m venv ./' in the meetingsBackend directory.
3. Next step is to run 'source ./bin/activate'
4. Now you are inside a virtual environment. This is useful for rapid development and testing in python. 
5. Run 'pip install -r requirements.txt'. If you do not have pip, follow this link to install pip https://pip.pypa.io/en/stable/installing/
6. Run 'source init-db.sh'. This is to init database and also load models defined.
7. Now you can start the service by running 'python3 run.py'
8. That is it. The service is running locally now.


Test Instructions
-----------------
1. In order to test, open a new terminal, cd to the meetingsBackend dir, and then run 'source ./bin/activate'
2. cd to test directory.
3. Run py.test
4. You can see that the above command runs 4 test files
 test_0_createapis.tavern.yaml
 test_1_getrecordingfrommeeting.tavern.yaml
 test_2_sharerecording.tavern.yaml
 test_3_checkrecordingaccess.tavern.yaml
5. In the other window where service is running, you can see that various api calls are being made along with the status code it sends back to the caller.
6. POSTMAN can also be used to test these APIs.




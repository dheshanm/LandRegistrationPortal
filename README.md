# Land Registration Portal
Land Registration Portal that stores all transaction (Land Registrations) in blockchain.

## How it works
This implementation of Registration portal, works with the help of 2 servers, a Django server to take care of all user inputs and viewing, while the other Flask server is responsible for turning these user generated content into sucured blocks as a part of the blockchain.

### Role of Django Server 
  * To act as an interface between the user and the blockchain
  * Help restore the chain by transfering the chain from itself to the blockchain server, in case the blockchain server shuts down
    * **Note** The blockchain server need to be persistent to hold the chain, in the implementation of the current blockchain server, To overcome data loss when the block chain server shuts down, 
      1. The Flask Server [The blockchain server] on initializing syncs or gets the chain from the django server
      2. If the Django server is unavailable, The Django server, before updating any transaction, which will check if its chain is longer than the blockchain server's chain, if this test fails, it will update or Sync the blockchain server with its own version of the chain

### Role of Flask (Block chain Server) Server
  * To handle all blockchain related activity
  
## How to get Started
  1. Modify the contents of the necessary files, namely
    1. _LandPortal/views.py_, the the address of the Blockchain server needs to be changed
    2. Silimarly, look through for any device/implementation specific code to modify to your liking
  2. First initialize the Django server with the following commands
  ```bash
  cd LandPortal
  
  python manage.py makemigration
  python manage.py migrate
  python manage.py runserver
  ```
  This will start the Django Server, Default at 127.0.0.1:8000
  
  3. Start the flask or the Blockchain server, following 
      ```bash
      $ export FLASK_APP=node_server.py
      $ flask run --port 8001
      
      $ python run_app.py
      ```
      This will start the blockchain server, which will be listening on port 8001
      
  4. Now, with both the servers started, visit the Django's Development server which is running at 127.0.0.1:8000

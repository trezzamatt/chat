A simple chat client that just runs locally for now.

usage:

   install dependencies:
      `pip install flask_sqlalchemy flask`
      
   set up database tables:
        `python db_setup.py`
         if you wish to start with new database, delete the instance folder and run this again.
    
   start the server:
        `python chat_app.py`
        
   navigate to the endpoint in a browser (default `localhost:5000`)
   
   you must create an account to login, you can open multiple windows with multiple accounts and see messages pop up between them. 

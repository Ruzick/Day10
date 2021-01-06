# Day10
Pre-bootcamp exercise. 
Followed this tutorial for bokeh plot rendering: https://davidhamann.de/2018/02/11/integrate-bokeh-plots-in-flask-ajax/

Make a config.py file to store your api key to use locally; and store in heroku as config variable if used in heroku.

        #key  = config.api_key# commented for heroku
        
        key = os.environ['api_key'] #only with heroku

Also in the layout.html, change the link from http to https when running in Heroku.

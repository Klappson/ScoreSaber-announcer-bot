# ScoreSaber Announcer Bot
Discord bot for announcing new BeatSaber scores in a specified
Discord-Channel.

# Requirements
* Python 3.9 (This is the Version I used. Others may work too)
* A Postgres database-server
    * A database for the bot
    * A user for the bot
        * The user should have full access to the database

# Setup
1. Clone this Repository
````shell
git clone https://github.com/Klappson/ScoreSaber-announcer-bot
````
2. Install `libpq-dev`. This is needed to build `psycopg2`
````shell
sudo apt-get install libpq-dev
````
2. Install required packages
````shell
pip install -r requirements.txt
````
3. Adjust the config.py
4. Run the bot
````shell
python bot.py
````
5. Profit

# Known Issues
* SSLCertVerification shizzle
    * Install <a href="https://crt.sh/?id=1">this</a> certificate
    * The download is hidden on the bottom left
    
    
* The bot does not send any scores
    * Make sure your request-intervals, found in the config.py, are big enough.
    * If they are big enough write me an Issue and I'm gonna take a look at it
    
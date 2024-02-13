# OMPM
## About the Project
Always forgetting who owes you money? This bot helps to keep track of who owes you money!

[Link to bot](https://t.me/inomoney_bot) (Probably not working because I did not deploy it :stuck_out_tongue_closed_eyes:)

### Tech Stack
- Python 3.12
- Sqlite3
- pythonAnywhere (https://www.pythonanywhere.com/)

## Usage
### Commands:
- /start - Introduction of bot
- /help - Explains what each function does
- /add - Add a new debt to the database
- /who - See who is currently owing you money
- /paid - Remove the person who has paid you from the database

**/start** <br/>
When using the bot for the first time <br/>
<img src="images\itb.jpg" alt="Using the bot for the first time" width="400"/> <br/>

**/help** <br/>
When using the /help command <br/>
<img src="images\help.jpg" alt="/help called" width="400"/> <br/>

**/add** <br/>
Flow of the /add command <br/>
<img src="images\add_success.jpg" alt="Successfully added a payer" width="400"/> <br/>

If you keyed in a wrong value, you can change it before inserting it into the database <br/>
<img src="images\wrong_borrower.png" alt="Wrong payer" width="400"/> <br/>

**/who** <br/>
Flow of the /who command <br/>
<img src="images\who2.jpg" alt="Successfully called a payer" width="400"/> <br/>

When no one is currently owing you money<br/>
<img src="images\who1.jpg" alt="Payer does not exist" width="400"/> <br/>

**/paid** <br/>
Flow of the /paid command <br/>
<img src="images\paid.jpg" alt="Successfully removed a payer" width="400"/>

When a name that has not been recorded is keyed in<br/>
<img src="images\rlydontexist.jpg" alt="Guy who doesnt exist" width="400"/>

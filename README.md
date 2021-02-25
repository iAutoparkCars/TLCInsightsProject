## TLCInsights CLI
Shell script that offers transportation insights using TLC NYC data 

#### Approach
For each type of transport _Yellow Cab, Green, Cab_, and _Ridesharing_, return an estimate of 
trip duration (in minutes) and trip total price (in dollars) based on the historical data provided by TLC. <br />
The user will be able to filter by start, end NYC Borough and datetime.

####  Design
An Azure SQL Database was created for ease of use on authors and users of the script.
Queries will be run in Azure to supply the insights to the user. <br />
Connecting to DB directly is an intentional oversimplification of the design and this tradeoff was done in favor of completion of the core functionality of the CLI. 
In production, the client would never connect directly to a database, and would ideally call an API through an endpoint or gateway, at which
some middleware (ie. microservice) would query the database

#### Files
* `push_data.py` A script that populates an Azure SQL DB with TLC data found in the /data directory of this project <br />
* `main.py` An interactive CLI script that uses TLC record trip data to give insights on trip fare and trip time estimates
    from borough to borough in NYC for green taxis, yellow taxis, and ridesharing (for-hire) <br />

#### How to run
Install Python dependencies from `requirements.txt` manually or with virtual environment: <br />
* Manual: `pip install dependency-name` or <br />
* Virtual Env: install dependencies from `requirements.txt` in a virtual Python environment. <br />
More details of how to set up virtual environment found here https://docs.python.org/3/tutorial/venv.html

Run scripts: <br />
* `python main.py` To run core functionality (CLI) <br />
* `python push_data.py` To populate Azure SQL Database. Follow instructions in comments to populate appropriate tables

## More Trade Offs
In order to complete the core functional requirements
* Distinction between Yellow Cab, Green Cab, For hire vehicles
* allow users to specify start, end Boroughs
* allow users to speicfy start, end times

<details>
  <summary>Simplification was done For-hire category (click for details) </summary>
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; I disregard the small subset of For Hire-vehicles (ie. Black Cab) and only considered
High Volume For-Hire Vehicles (introduced in early 2019 to make a distinction for ridesharing companies like Uber, Lyft), which make up the vast majority of For-Hire category -- in the CLI script, this category is just named 'Ridesharing'
</details>

<details>
  <summary>UX Simplification to not explicitly allow filter by category of Yellow, Green, Rideshare(click for details) </summary>
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Instead all the information (trip price and trip time averages are returned in a table for all three categories, which is a more inuitive user experience. This is preferable over giving users another filter of category in addition to Borough, and datetime. example: <br />
```
+---------------+------------+------------+-------------+
|               | Yellow Cab | Green Cab  | Ridesharing |
+---------------+------------+------------+-------------+
|  average time | 15 minutes | 20 minutes |  16 minutes |
| average price |   $18.7    |   $20.42   |    $20.42   |
+---------------+------------+------------+-------------+
```
</details>

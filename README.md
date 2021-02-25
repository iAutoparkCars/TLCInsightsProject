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
* allow users to specify start, end times

<details>
  <summary>Simplification was done For-hire category (click for details) </summary>
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; I disregard the small subset of For Hire-vehicles (ie. Black Cab) and only considered
High Volume For-Hire Vehicles (introduced in early 2019 to make a distinction for ridesharing companies like Uber, Lyft), which make up the vast majority of For-Hire category -- in the CLI script, this category is just named 'Ridesharing'
</details>

<details>
  <summary>Hosting database in the cloud </summary>
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Large dataset is tedious if operations are performed all in memory locally; this is also tedious for a user to download large dataset to run a CLI script, so the decision was made to move the querying funcionality into a cloud database.
Another decision was AWS vs Azure -- Azure was chosen for a new learning experience
</details>

<details>
  <summary>Unfeasible volume of data had to be sampled </summary>
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The volume of data was not feasible for this context. There are two popular sampling techniques, random sampling, and systematic sampling -- 
systematic sampling was chosen based on simplicity of implementation: <br /> https://www.investopedia.com/ask/answers/071615/when-it-better-use-systematic-over-simple-random-sampling.asp
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

<details>
  <summary>Simplification of datetime </summary>
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; When users search by datetime filter, there is only option to search by date (not by time at a specific date as that is too granular)
</details>

<details>
  <summary>Simplification of the UI </summary>
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Initially a graphical interface was considered (with charts showing historical data based on ride volume over the months), but then when more planning was done, it was realized that was outside of budget constraint
</details>

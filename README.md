![goodbye-saturn-l5-1336x768](https://user-images.githubusercontent.com/129196368/231134541-9e2e90d0-a660-4438-8ca8-40c06a966df5.jpg)
# 🚀SaturiC
Exploring and Optimizing Your GitHub Community

# Ready to start
First, install all the dependencies from the file ***requirements.txt***:

```pip install -t requirements.txt```

## Access token for parsing
How to get a GitHub Access Token
The GitHub Access Token is a unique code used to authorize access to your repositories and other GitHub resources. It can be obtained in a few simple steps.

### Step 1: Go to your GitHub profile settings
1. Go to the GitHub site and log in to your account.
2. Click on your avatar in the top right corner of the screen and select Settings.

### Step 2: Choose settings to get an Access Token
1. On the settings page, select the "Developer settings" tab.
2. On the menu that appears, select "Personal access tokens.

### Step 3: Create a new token
1. Click on the "Generate new token" button.
2. Select the necessary permissions for the token (read, write, delete, etc.).
3. Click on the "Generate token" button.
4. Copy the generated token to a safe place. Please note that after closing the window, the token will no longer appear.

You can now use your Access Token to authorize access to repositories and other GitHub resources. To use it, add it as a value for the "access_token" parameter in your GitHub API requests.

# ❄Security (access data)
To set the access_token, owner, and repo variables as environment variables, you can use the os module in Python.
Here's an example:

- Create a new file called .env in the root directory of your project.
- Add the following lines to the .env file:
```
export access_token='your-token'
export owner='delovoyhomie'
export repo='ton-footsteps'
```
Save the ".env" file.

Now you can use these variables in your code to avoid hard coding values. For example, you can use them in your Python code as follows:
```
import os

access_token = os.environ['access_token']
owner = os.environ['owner']
repo = os.environ['repo']
```

Here we have used the Python library "os" to access environment variables. The function "os.environ['variable_name']" is used to get the value of the variable.

If you don't need this protection, just add the token from the plate.py file and import this 
```
from plate import access_token
from plate import owner 
from plate import repo
```


# 🎓How to use it?
## For what?
Visualization and data collection can help you learn which community members contribute the most to the project. This can help project leaders determine who needs encouragement and who can help develop the project. Visualization and data collection can also help track project development, including the frequency and volume of code changes, the number of open and closed issues, growth in the number of participants, etc. This can help project leaders understand where the project is going and make evidence-based decisions. 
## Tutorial 
To get started, start the program and select one of 17 options. You can choose to show information about contributors, problems, or pool-requests, as well as get various statistical graphs and KPIs. Run main.py for first

### Points
If you want to get the average time to solve problems, select option 4. If you want a visualization of the contributions, problems, or pool-requests statistics, select the appropriate option from 5 to 8.

You can also get a visualization of your counterparty statistics as a chart or heatmap by selecting one of options 9 to 11. If you need KPIs, select one of options 13 or 14.

To export data to a CSV file, choose one of options 15, 16 or 17. If you need more information, select option 18.

Once you have selected your option, you will see the corresponding results in the console. If you want to exit the program, enter the letter "q".

#### Extension
## Get data
- Show info contributors": displays information about the number of community contributors.
- Show info issues: displays information about the number of open and closed issues.
- Show info pulls": displays information about the number of pull requests. 
- Show average_time for issues": calculates the average time taken to solve an issue and displays it.
- Get AVG parameter": calculates the average value of the parameter for all project participants.
- Get KPI parameter (pulls)": calculates the key performance indicator (KPI) for merge requests.
- Get KPI parameter (contributions): calculates the key performance indicator (KPI) for contributions.

## Get visual
- Visual for contribution statistics": displays a graph that shows the number of contributions made by each project participant.
- Visual for issues statistics: displays a graph showing the number of problems in the project.
- Visual for pulls statistics": displays a graph showing the number of merge requests in the project.
- Visual relation issues/pulls": displays a chart showing the ratio of problems to merge requests in the project.
- Visual bar charts for contribution": displays a bar chart showing the number of contributions from each project member.
- Visual with Heatmap for contribution": displays a heatmap showing the number of contributions of each project participant on each day.
- Visual with Bubbles for contribution": displays a bubble chart showing the number of contributions of each project participant.

## Export
- Export CSV about contributors": exports information about all project participants in CSV format.
- Export CSV about pulls: exports information about all merge requests in CSV format.
- Export CSV about issues: exports information about all problems in the project in CSV format

![goodbye-saturn-l5-1336x768](https://user-images.githubusercontent.com/129196368/231134541-9e2e90d0-a660-4438-8ca8-40c06a966df5.jpg)
# 🚀Saturn_FM
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
### 💾Functions for getting data
Run ***get_contributors(), get_issues(), get_pulls(), and average_time_isseu()*** to get the information you need. For example:
```
get_contributors()
get_issues()
get_pulls()
average_time_isseu()
```

After you run the features, you'll get information about your repository, such as the number of participants, the number of issues and change requests, and the average time to resolve issues. Interpret the results to understand the community's contribution to the project and the effectiveness of working on problems.

## 💾Info 
#### get_contributors()
Get's information about contributors to the project on GitHub and displays statistics about the number of regular and active contributors, as well as the total number of commits from community members.

#### get_issues()
Get's information about all tasks (issues) of the project on GitHub and displays statistics about the number of open and closed tasks.

#### get_pulls()
Get's information about all pull requests of the project on GitHub and displays statistics about the number of pull requests.

#### average_time_isseu()
Get's information about the solution time of project tasks on GitHub and outputs the average solution time in days.

## 🖨Plotting data
#### The plot_contributors() 
Function uses the GitHub API to retrieve data on contributors to the repository, specifically their total number of commits. It then plots this data in a bar graph using the plotly library.

#### The plot_issues() 
Function retrieves data on all issues in the repository, both open and closed, and plots this data in several different graphs using the plotly and pandas libraries. The graphs include a pie chart comparing the number of open and closed issues, a histogram showing the distribution of days for open issues, a histogram showing the distribution of days it took to close issues, and two line graphs showing the number of open and closed issues over time.

#### The plot_pulls() 
Function is similar to plot_issues(), but retrieves data on pull requests instead. It plots a pie chart comparing the number of open and closed pull requests using the plotly library.

#### The issues_x_pulls() 
Function retrieves data on both issues and pull requests and plots this data in a bar graph using the plotly library.

#### The viz_contributors() 
Function retrieves data on the weekly contributions of each contributor to the repository and plots this data in a line graph using the plotly library.

## 🖨Complex plotting data 
The **complex_plot_contributors()** function creates a plot that displays statistics on contributors to a GitHub repository. The plot includes three subplots:
- A scatter plot showing the total number of commits vs. the total number of changes for each contributor, with the size of each marker indicating the total number of additions made by that contributor.
- A line plot showing the total number of commits for each contributor.
- A 2D histogram showing the distribution of total additions vs. total deletions for all contributors.

The **complex_plot_issues()** function creates three plots that display statistics on issues in a GitHub repository:
- A line plot showing the number of issues opened and closed over time.
- A histogram showing the distribution of issues by label.
- A pie chart showing the percentage of issues by assignee.

The **complex_plot_pulls()** function creates a plot that displays statistics on pull requests in a GitHub repository. The plot includes:
- A bar chart showing the number of pull requests in each of three states: open, closed, and merged.
- A pie chart showing the percentage of pull requests by author.

## DST functions
### 💾Getting data
#### dst_get_contributors(start_date, end_date)
The function dst_get_contributors retrieves information about the number of active contributors, the number of their contributions and the number of active initiatives on the TON Footsteps project during a given period of time.

Function parameters:
- start_date: start date in datetime.date format.
- end_date: end date in datetime.date format.

How to use the function:
```
start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 12, 31)
dst_get_contributors(start_date, end_date)
```

#### dst_get_issues(start_date, end_date)
The function dst_get_issues gets information about the number of problems, closed and open problems in a given period of time on the TON Footsteps project.

Function parameters:
- start_date: start date in datetime.date format.
- end_date: end date in datetime.date format.

How to use the function:
```
start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 12, 31)
dst_get_issues(start_date, end_date)
```
#### dst_get_pulls(start_date, end_date)
The function dst_get_pulls gets information about the number of open and closed merge requests in a given period of time on the TON Footsteps project.

Function parameters:
- start_date: start date in datetime.date format.
- end_date: end date in datetime.date format.

How to use the function:
```
start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 12, 31)
dst_get_pulls(start_date, end_date)
```

#### dst_average_time_issue()
The function dst_average_time_issue calculates the average time to solve a problem on a TON Footsteps project.
Function parameters: none.

How to use the function:
```dst_average_time_issue()```

### 🖨DST Plot
The function **dst_plot_contributors** uses the GitHub API to get data about the number of commits made by each contributor over a specified period of time and builds a bar chart with this information.

The **dst_plot_issues** function uses the GitHub API to get a list of issues opened and closed over a specified period of time and builds a pie chart showing the ratio of open and closed issues.

Function **dst_plot_pulls** uses GitHub API to get the list of merge requests, opened and closed for a specified period of time, and builds a pie chart showing the ratio of open and closed merge requests

To call these functions, you have to import the necessary libraries and then call the functions with the necessary arguments:
```
start_date = "2022-01-01"
end_date = "2022-12-31"

dst_plot_contributors(start_date, end_date)
dst_plot_issues(start_date, end_date)
dst_plot_pulls(start_date, end_date)
```
### 🖨DST complex plot
The first function, **complex_dst_plot_pulls**, retrieves pull request data for the given date range and creates three visualizations: a bar chart of the number of pull requests by author, a pie chart of the status of the pull requests, and a bar chart of the number of pull requests made by each user.

The second function, **complex_dst_plot_issues**, retrieves issue data for the given date range and creates three visualizations: a bar chart of the number of issues by author, a pie chart of the status of the issues, and a bar chart of the number of issues made by each user.

The third function, **complex_dst_plot_contributors**, retrieves contributor data for the given date range and creates three visualizations: a bar chart of the number of commits by contributor, a bar chart of the number of lines added by contributor, and a bar chart of the number of lines deleted by contributor.

To call the functions ***complex_dst_plot_pulls, complex_dst_plot_issues and complex_dst_plot_contributors***, you need to pass the start and end dates of the period for which you want to receive data. For example, if you want to get data from January 1, 2023 to January 31, 2023, you can call the functions as follows:
```
start_date = "2023-01-01"
end_date = "2023-01-31"

complex_dst_plot_pulls(start_date, end_date)
complex_dst_plot_issues(start_date, end_date)
complex_dst_plot_contributors(start_date, end_date)
```

🚀Now that you've mastered all the basics, your preparation for your trip to space is complete. Have a safe trip! 


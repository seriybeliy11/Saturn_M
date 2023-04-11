![goodbye-saturn-l5-1336x768](https://user-images.githubusercontent.com/129196368/231134541-9e2e90d0-a660-4438-8ca8-40c06a966df5.jpg)
# Saturn_FM
Fast M for The TON Footsteps

## Saturn_M file:

### get_contributors()
Get's information about contributors to the project on GitHub and displays statistics about the number of regular and active contributors, as well as the total number of commits from community members.

### get_issues()
Get's information about all tasks (issues) of the project on GitHub and displays statistics about the number of open and closed tasks.


### get_pulls()
Get's information about all pull requests of the project on GitHub and displays statistics about the number of pull requests.

### average_time_isseu()
Get's information about the solution time of project tasks on GitHub and outputs the average solution time in days.

### plot_contributors() 
Show's the total number of commits made by each contributor to the repository. It makes a request to the GitHub API to retrieve the contributors and their commit counts, and then creates a bar chart using the Plotly library to display the results.

### plot_issues() 
Show's various metrics related to issues in the repository, including the number of open and closed issues, the distribution of days that open issues have been open, and the number of open issues over time. It uses the Plotly and Pandas libraries to create pie charts, histograms, and line charts to display the data.

### plot_pulls() 
Show's the number of open and closed pull requests in the repository. It makes a request to the GitHub API to retrieve the pull requests and their state (open or closed), and then creates a pie chart using the Plotly library to display the results.

### issues_x_pulls() 
Show's the total number of open issues and pull requests in the repository. It retrieves the number of open issues and pull requests using the get_issues() and get_pulls() functions (which are not shown in the code), and then creates a bar chart using the Plotly library to display the results.

### viz_contributors()
This feature is designed to visualize data about project members on GitHub. It uses the GitHub API to retrieve information about each contributor's contributions and plots the number of commits each contributor has made over time. This can help you analyze user activity, determine who is most active and who has contributed to your project, and help you motivate users to contribute to your project.

### complex_plot_contributors()
Function creates a plot to display statistics about contributors to a GitHub repository. The plot shows the total number of commits vs. the total number of changes made by each contributor. The size of the markers is proportional to the total number of additions made by the contributor, and the color of the markers indicates the total number of deletions made by the contributor. The plot also shows a line graph of the total number of commits by each contributor, and a histogram of the total number of additions vs. deletions made across all contributors.

### complex_plot_issues()
Function creates three plots to display statistics about issues in a GitHub repository. The first plot shows the number of issues opened and closed over time. The second plot shows a histogram of the distribution of issues by label. The third plot shows a pie chart of the percentage of issues by assignee.

### complex_plot_pulls()
Function creates a plot to display statistics about pull requests in a GitHub repository. The plot shows the number of pull requests by each author, and the status of each pull request (open, closed, or merged).

## Saturn_F file
### complex_dst_plot_pulls(start_date, end_date): 
This function retrieves data on pull requests within the specified time range and creates three plots showing the number of pull requests made by each author, statistics on the pull requests, and the number of pull requests made by each user.

### complex_dst_plot_issues(start_date, end_date): 
This function retrieves data on issues within the specified time range and creates three plots showing the number of issues made by each author, statistics on the issues, and the number of issues made by each user.

### complex_dst_plot_contributors(start_date, end_date): 
This function retrieves data on contributors within the specified time range and creates three plots showing the number of commits, additions, and deletions made by each contributor.

### dst_plot_contributors(start_date, end_date) 
The function builds a graph with the number of commits for each project member. To do this, the function sends a request to the GitHub API, using the parameters owner and repo, as well as access_token. Then the function filters the list of participants according to the specified start_date and end_date time interval. The data about the number of commits is extracted from the filtered list of participants and a bar chart is drawn. The name of the diagram is determined by the layout_title_text parameter.

### dst_plot_issues(start_date, end_date) 
The function builds a pie chart showing the ratio of open and closed tasks in the project. Function sends request to GitHub API using parameters repo and access_token. Then it filters the list of tasks according to the specified start_date and end_date time interval. The resulting list is divided into two lists: open_issues and closed_issues. Each list contains tasks of the corresponding status. The function then builds a pie chart showing the number of open and closed tasks. The name of the diagram is determined by the layout_title_text parameter.

### dst_plot_pulls(start_date, end_date) 
The function builds a pie chart showing the ratio of open and closed merge requests in the project. The function sends a request to the GitHub API using repo and access_token parameters. Then it filters the list of merge requests by the specified start_date and end_date time frame. The resulting list is divided into two lists: open_pulls and closed_pulls. Each list contains merge requests of the corresponding status. The function then constructs a pie chart showing the number of open and closed merge requests. The name of the diagram is determined by the layout_title_text parameter.

### dst_get_contributors(start_date, end_date)
This function takes in two parameters, start_date and end_date, which represent the start and end dates of the time period that we want to collect data for. The function uses the GitHub API to retrieve data on the contributors to the TON Footsteps repository during this time period. The function calculates the average number of commits made by these contributors, and also returns a list of the contributors who made more than the average number of commits.

### dst_get_issues(start_date, end_date) 
This function takes in two parameters, start_date and end_date, which represent the start and end dates of the time period that we want to collect data for. The function uses the GitHub API to retrieve data on the issues that were opened and closed during this time period. The function returns the number of total issues, the number of closed issues, and the number of open issues.

### dst_get_pulls(start_date, end_date)
This function takes in two parameters, start_date and end_date, which represent the start and end dates of the time period that we want to collect data for. The function uses the GitHub API to retrieve data on the pull requests that were opened and closed during this time period. The function returns the number of total pull requests, the number of closed pull requests, and the number of open pull requests.

### dst_average_time_issue()
This function calculates the average time it takes to solve an issue in the TON Footsteps repository. The function uses the GitHub API to retrieve data on all the issues that were closed in the repository and calculates the time difference between the creation time and closing time of each issue. The function returns the average time it takes to solve an issue in days.

# Attention !!!
Storing sensitive information, such as access tokens, in plaintext in code can be insecure. It is recommended that you store sensitive information, such as access tokens, in environment variables.

You can set up environment variables in your operating system to use in your Python programs. Here is an example of how you can use environment variables in Python:
```
import os
access_token = os.environ.get('GITHUB_ACCESS_TOKEN')
owner = os.environ.get('GITHUB_REPO_OWNER')
repo = os.environ.get('GITHUB_REPO_NAME')
```

Note that you must set the values of these environment variables in your operating system before you can use them in your Python script. You can set them on the command line or in a configuration file such as ~/.bashrc or ~/.bash_profile if you are using a Unix-like operating system.

![goodbye-saturn-l5-1336x768](https://user-images.githubusercontent.com/129196368/231134541-9e2e90d0-a660-4438-8ca8-40c06a966df5.jpg)
# 🚀Saturn_FM
Exploring and Optimizing Your GitHub Community

# 🛸Beggining
First, install all the dependencies from the file ***requirements.txt***:

```pip install -t requirements.txt```

# Access token for parsing
How to get a GitHub Access Token

The GitHub Access Token is a unique code used to authorize access to your repositories and other GitHub resources. It can be obtained in a few simple steps.

## Step 1: Go to your GitHub profile settings
1. Go to the GitHub site and log in to your account.
2. Click on your avatar in the top right corner of the screen and select Settings.

## Step 2: Choose settings to get an Access Token
1. On the settings page, select the "Developer settings" tab.
2. On the menu that appears, select "Personal access tokens.

## Step 3: Create a new token
1. Click on the "Generate new token" button.
2. Select the necessary permissions for the token (read, write, delete, etc.).
3. Click on the "Generate token" button.
4. Copy the generated token to a safe place. Please note that after closing the window, the token will no longer appear.

You can now use your Access Token to authorize access to repositories and other GitHub resources. To use it, add it as a value for the "access_token" parameter in your GitHub API requests.

# Security (access data)
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

# How to use it?
## For what?
Visualization and data collection can help you learn which community members contribute the most to the project. This can help project leaders determine who needs encouragement and who can help develop the project. Visualization and data collection can also help track project development, including the frequency and volume of code changes, the number of open and closed issues, growth in the number of participants, etc. This can help project leaders understand where the project is going and make evidence-based decisions. 
## Tutorial 

# VeronisHomeAssignment
*READ*
In order for the code to run propertly, a .env file ust be added to the project directory. The contents of the file should look like this:
GITHUB_TOKEN="your_github_token"
REPO_NAME="your_github_repo"
The github token can be generated in the gitHub app under user settings -> developer settings -> Personal access token.
REPO_NAME is the name of the repository for which you want to check and update the configurations.


*ANSWERS TO QUESTIONS*
- Find and specify a list of 2 specific configurations with a security impact for either
users or repositories. For one of these misconfigurations that you choose, write in detail way that would
be understandable by a non-technical person.

From the various gitHub configurations, I chose to elaborate on the reviews for pull requests option, 
and the disabling force pushing on protected branches option.
The branch protection ruleset help prevent unwanted/unauthorized changes to branches, as well as
specify custom rules based the branch role, the user permissions and more. In regards to the reviews for pull requests configuration, 
the best practice for this configuration would be to set a minimum number of reviewers the default branch in the project, 
that have to be approved before merging. This makes it so every change that is trying to be added into the main branch was seen and 
approved by several eyes, which reduces the risk of bad/unwanted code making it to higher deployment levels.
This configuration can be changed by going to your repository settings, then branches and click "Add rule", then specify the name of
the branch/branches that the rule should apply to and mark the options "Require a pull request before merging" and 
the option "Require approvals", and using the dropdown list specify the number of required approvals.  
Changing this configuration will result in each merge request with the default branch to be kept on hold until the specified number of
approvals is met.
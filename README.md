# VaronisHomeAssignment
__Please Read Carefully__ <br>
In order for the code to run propertly, a *.env file ust be added to the project directory. The contents of the file should look like this:<br>
```
GITHUB_TOKEN="your_github_token"
REPO_NAME="your_github_repo"
```
The github token can be generated in the github app/site under user settings -> developer settings -> Personal access token.
REPO_NAME is the name of the repository for which you want to check and update the configurations.
After configuring this file correctly, the script can be run by configuring your script path to the script location using your IDE.
The bonus script can be run as well and will result in a different output depending whether the main branch is protected or not.


*ANSWERS TO QUESTIONS*
- Find and specify a list of 2 specific configurations with a security impact for either
users or repositories. For one of these misconfigurations that you choose, write in detail way that would
be understandable by a non-technical person.

From the various github configurations, I chose to elaborate on the reviews for pull requests option, 
and the disabling force pushing on protected branches option.
The branch protection ruleset help prevent unwanted/unauthorized changes to branches, as well as
specify custom rules based the branch role, the user permissions and more. In regards to the reviews for pull requests configuration, 
the best practice for this configuration would be to set a minimum number of reviewers for the default branch in the project, 
that have to be approved before merging. This makes it so every change that is trying to be added into the main branch was seen and 
approved by several eyes, which reduces the risk of bad/unwanted code making it to higher deployment levels.
This configuration can be changed by going to your repository settings, then branches and click "Add rule", then specify the name of
the branch/branches that the rule should apply to and mark the options "Require a pull request before merging" and 
the option "Require approvals", and using the dropdown list specify the number of required approvals.  
Changing this configuration will result in each merge request with the default branch to be kept on hold until the specified number of
approvals is met. <br>
The project also contains a bonus script, that demonstrates the risk of how repositories without a reviewer ruleset are vulnerable to
unwanted files and code addition into critical branches. <br>
The project contains a folder named "ScreenShots", which contain screenshots of the expected outputs of both the main and bonus scripts. The outputs vary
depending on if a reviewer ruleset is already in place for the main branch.

- Add a detailed description of how you would expand your scripts into a framework
for monitoring and fixing many misconfigurations across multiple services from
different kinds.

A possible way of scaling this project would be to create a web application, with an interface supporting subscribtion for different 
users/organizations with projects that are susceptible to misconfigurations of many kinds. Our project would then store information 
about each client, including a unique identifier, their access token (or any other method by which we can access and monitor their data,
preferrably we keep this information encrypted) and the types of misconfigurations that they require our assistance with. 
Our application would then offer a service where every set period of time, we transition over all of our client's misconfiguration needs
and for each one run a script similar to the one written in section 1 of this excersize, which is changed based on the type of misconfiguration
that we are handling.

Regarding data structures and databases, each client can be represented by a client class that contains his id and an array of all
misconfigurations we need to monitor for that client. A misconfiguration could be represented by an abstract class named "MisconfigurationChecker",
which defines functionality checkForMisconfiguration() and handleFoundMisconfiguration(). Every specific misconfiguration type would then be 
a new class inheriting from this abstract class, and thus forced to implement these functions. So for example my code would be the functionality 
for a specific misconfiguration type  and could be implemented inside a class named GitHubProtectionMisconfigurationChecker, that seperates the 
code between checkForMisconfiguration(), where we check if the current repo is misconfigured regarding its protection, and handleFoundMisconfiguration(),
where we fix the misconfiguration (this can be based on default settings and protocols we establish, or by instructions given to us by the client).
For the database, we can use MongoDB, as it supports encryption which is crucial when storing important information, and would work well structurally,
because we do not know in advance how many misconfigurations and misconfiguration types each client will bring. Storing the data in a table based
database might cause problems.
Regarding usage, our site can either keep tracking periodically for every client registered, or we can implement a login system where clients need to
log in in order for our application to begin monitoring their data.



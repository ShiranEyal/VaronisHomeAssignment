# VeronisHomeAssignment
- Find and specify a list of 2 specific configurations with a security impact for either
users or repositories. For one of these misconfigurations that you choose, write in detail way that would
be understandable by a non-technical person.

From the various gitHub configurations, I chose to elaborate on the branch protection rules,
and the 
The branch protection ruleset help prevent unwanted/unauthorized changes to branches, as well as
specify custom rules based the branch role, the user permissions and more. The best practice for this configuration
would be to set a minimum number of reviewers for all branches in the project, that have to be approved before merging. 
This makes it so every change to your specified branches was seen and approved by several eyes.
Also for more important branches, add automated testing and limit the users/groups with permissions to push into this branch.
This adds an extra layer of security and ensures that code the reaches higher levels of deployment is as safe as could be.
import os
import json
import requests
from github import Github
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')
REQ_REVIEWS = 1

PullReqNeedConfig = "The default branch '{}' is not configured properly for pull request reviewers. Adding a default configuration."
PullReqAlreadyConfigured = "The default branch '{}' is already protected with required reviews."
PullReqSuccess = "Successfully protected the branch '{}' with required pull request reviews."
PullReqFailure = "Failed to protect the branch with pull requests. Response: {}"

ForcePushDisabledSuccess = "Successfully disabled force pushing for branch '{}'."
ForcePushDisabledFailure = "Failed to update protection settings: {}"
ForcePushDisabledFinished = "Finished removing force pushing from all protected branches."

# This function verifies that the repository`s default branch is configured properly for pull request reviewers.
# If it is not we create a new protection ruleset for it.
def ConfigurePullReqReviewers(repo, curr_user):
    default_branch = repo.get_branch(repo.default_branch)
    protection = None
    try:
        protection = default_branch.get_protection()
    except:
        pass
    # Check if default branch is missing a pull request reviewers configuration
    if not protection or not protection.required_pull_request_reviews or \
            protection.required_pull_request_reviews.required_approving_review_count == 0:
        print(PullReqNeedConfig.format(default_branch.name))

        url = f"https://api.github.com/repos/{curr_user.login}/{repo.name}/branches/{default_branch.name}/protection"
        headers = {
            "Authorization": f"token {ACCESS_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
        # Get current protection settings
        updated_settings = GetBranchProtectionSettings(url, headers)
        updated_settings["required_pull_request_reviews"] = {
            "required_approving_review_count": REQ_REVIEWS
        }

        # Make put request to update protection settings
        response = requests.put(url, headers=headers, data=json.dumps(updated_settings))
        if response.status_code == 200:
            print(PullReqSuccess.format(default_branch.name))
        else:
            print(PullReqFailure.format(response.status_code))
    else:
        print(PullReqAlreadyConfigured.format(default_branch.name))

# This function verifies that all branches in the repository that have some sort of protection rule have the option
# to force push turned off.
def DisableForcePushing(repo, curr_user):
    allow_force_pushes = "allow_force_pushes"
    for branch in repo.get_branches():
        try:
            # Try to get protection. if failed then this is an unprotected branch and we can continue
            protection = branch.get_protection()
            url = f"https://api.github.com/repos/{curr_user.login}/{repo.name}/branches/{branch.name}/protection"
            headers = {
                "Authorization": f"token {ACCESS_TOKEN}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json"
            }
            # Get current protection settings
            updated_settings = GetBranchProtectionSettings(url, headers)
            updated_settings[allow_force_pushes] = False

            # Make put request to update protection settings
            response = requests.put(url, headers=headers, data=json.dumps(updated_settings))
            if response.status_code == 200:
                print(ForcePushDisabledSuccess.format(branch.name))
            else:
                print(ForcePushDisabledFailure.format(response.json()))
        except:
            continue
    print(ForcePushDisabledFinished)

# Helper function to retrieve the protection settings of a branch using specified url and headers
def GetBranchProtectionSettings(url, headers):
    # Fetch current protection settings
    response = requests.get(url, headers=headers)
    # if response.status_code != 200:
    #     print(f"Failed to fetch protection settings: {response.json()}")
    #     return

    protection_settings = response.json()

    # Reconfigure required_status_checks field
    required_status_checks = protection_settings.get('required_status_checks', None)
    if required_status_checks is not None:
        required_status_checks = {
            "strict": required_status_checks.get("strict", True),
            "contexts": required_status_checks.get("contexts", [])
        }

    # Prepare updated settings with default values if not present
    updated_settings = {
        "required_status_checks": required_status_checks,
        "enforce_admins": protection_settings.get('enforce_admins', {}).get('enabled', True),
        "required_pull_request_reviews": protection_settings.get('required_pull_request_reviews', None),
        "restrictions": protection_settings.get('restrictions', None),
        "allow_force_pushes": protection_settings.get('allow_force_pushes', {}).get('enabled', False),
        "required_linear_history": protection_settings.get('required_linear_history', {}).get('enabled', False),
        "allow_deletions": protection_settings.get('allow_deletions', {}).get('enabled', False),
        "block_creations": protection_settings.get('block_creations', {}).get('enabled', False),
        "required_conversation_resolution": protection_settings.get('required_conversation_resolution', {}).get(
            'enabled', False),
        "lock_branch": protection_settings.get('lock_branch', {}).get('enabled', False),
        "allow_fork_syncing": protection_settings.get('allow_fork_syncing', {}).get('enabled', False)
    }
    return updated_settings


if __name__ == "__main__":
    g = Github(ACCESS_TOKEN)
    curr_user = g.get_user()
    repo = curr_user.get_repo(REPO_NAME)
    ConfigurePullReqReviewers(repo, curr_user)
    # DisableForcePushing(repo, curr_user)
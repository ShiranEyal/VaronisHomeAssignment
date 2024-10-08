import os
import json
import requests
from github import Github
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')
REQ_REVIEWS = 1

PULL_REQ_NEED_CONFIG = "The default branch '{}' is not configured properly for pull request reviewers. Adding a default configuration."
PULL_REQ_ALREADY_CONFIGURED = "The default branch '{}' is already protected with required reviews."
PULL_REQ_SUCCESS = "Successfully protected the branch '{}' with required pull request reviews."
PULL_REQ_FAILURE = "Failed to protect the branch with pull requests. Response: {}"

FORCE_PUSH_DISABLED_SUCCESS = "Successfully disabled force pushing for branch '{}'."
FORCE_PUSH_DISABLED_FAILURE = "Failed to update protection settings: {}"
FORCE_PUSH_DISABLED_FINISHED = "Finished removing force pushing from all protected branches."
FETCHING_ERROR = "Error getting user or repository. Please configure the .env file with proper variables and try again."
REQ_HEADERS = {
                "Authorization": f"token {ACCESS_TOKEN}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json"
            }

# Protection field strings
REQUIRED_STATUS_CHECKS = "required_status_checks"
ENFORCE_ADMINS = "enforce_admins"
REQUIRED_PULL_REQUEST_REVIEWS = "required_pull_request_reviews"
RESTRICTIONS = "restrictions"
ALLOW_FORCE_PUSHES = "allow_force_pushes"
REQUIRED_LINEAR_HISTORY = "required_linear_history"
ALLOW_DELETIONS = "allow_deletions"
BLOCK_CREATIONS = "block_creations"
REQUIRED_CONVERSATION_RESOLUTION = "required_conversation_resolution"
LOCK_BRANCH = "lock_branch"
ALLOW_FORK_SYNCING = "allow_fork_syncing"
STRICT = "strict"
CONTEXTS = "contexts"
ENABLED = "enabled"

URL = "https://api.github.com/repos/{}/{}/branches/{}/protection"

# This function verifies that the repository`s default branch is configured properly for pull request reviewers.
# If it is not we create a new protection ruleset for it.
def ConfigurePullReqReviewers(repo, curr_user):
    default_branch = repo.get_branch(repo.default_branch)
    try:
        protection = default_branch.get_protection()
    except:
        protection = None
    # Check if default branch is missing a pull request reviewers configuration
    if not protection or not protection.required_pull_request_reviews or \
            protection.required_pull_request_reviews.required_approving_review_count == 0:
        print(PULL_REQ_NEED_CONFIG.format(default_branch.name))
        url = URL.format(curr_user.login, repo.name, default_branch.name)
        headers = REQ_HEADERS
        # Get current protection settings
        updated_settings = GetBranchProtectionSettings(url, headers)
        updated_settings[REQUIRED_PULL_REQUEST_REVIEWS] = {
            REQUIRED_PULL_REQUEST_REVIEWS: REQ_REVIEWS
        }

        # Make put request to update protection settings
        response = requests.put(url, headers=headers, data=json.dumps(updated_settings))
        if response.status_code == 200:
            print(PULL_REQ_SUCCESS.format(default_branch.name))
        else:
            print(PULL_REQ_FAILURE.format(response.status_code))
    else:
        print(PULL_REQ_ALREADY_CONFIGURED.format(default_branch.name))

# This function verifies that all branches in the repository that have some sort of protection rule have the option
# to force push turned off.
def DisableForcePushing(repo, curr_user):
    for branch in repo.get_branches():
        # Try to get protection. if failed then this is an unprotected branch and we can continue
        try:
            protection = branch.get_protection()
        except:
            continue
        url = URL.format(curr_user.login, repo.name, branch.name)
        headers = REQ_HEADERS
        # Get current protection settings
        updated_settings = GetBranchProtectionSettings(url, headers)
        updated_settings[ALLOW_FORCE_PUSHES] = False

        # Make put request to update protection settings
        response = requests.put(url, headers=headers, data=json.dumps(updated_settings))
        if response.status_code == 200:
            print(FORCE_PUSH_DISABLED_SUCCESS.format(branch.name))
        else:
            print(FORCE_PUSH_DISABLED_FAILURE.format(response.json()))
    print(FORCE_PUSH_DISABLED_FINISHED)


# Helper function to retrieve the protection settings of a branch using specified url and headers
def GetBranchProtectionSettings(url, headers):
    # Fetch current protection settings
    response = requests.get(url, headers=headers)
    protection_settings = response.json()
    updated_settings = UpdateSettingsFormat(protection_settings)
    return updated_settings

# Helper function to convert the protection settings returned from our get request to
# the correct format for a put request
def UpdateSettingsFormat(protection_settings):
    # Reconfigure required_status_checks field
    required_status_checks = protection_settings.get(REQUIRED_STATUS_CHECKS, None)
    if required_status_checks is not None:
        required_status_checks = {
            STRICT: required_status_checks.get(STRICT, True),
            CONTEXTS: required_status_checks.get(CONTEXTS, [])
        }

    # Prepare updated settings with default values if not present
    updated_settings = {
        REQUIRED_STATUS_CHECKS: required_status_checks,
        ENFORCE_ADMINS: protection_settings.get(ENFORCE_ADMINS, {}).get(ENABLED, True),
        REQUIRED_PULL_REQUEST_REVIEWS: protection_settings.get(REQUIRED_PULL_REQUEST_REVIEWS, None),
        RESTRICTIONS: protection_settings.get(RESTRICTIONS, None),
        ALLOW_FORCE_PUSHES: protection_settings.get(ALLOW_FORCE_PUSHES, {}).get(ENABLED, False),
        REQUIRED_LINEAR_HISTORY: protection_settings.get(REQUIRED_LINEAR_HISTORY, {}).get(ENABLED, False),
        ALLOW_DELETIONS: protection_settings.get(ALLOW_DELETIONS, {}).get(ENABLED, False),
        BLOCK_CREATIONS: protection_settings.get(BLOCK_CREATIONS, {}).get(ENABLED, False),
        REQUIRED_CONVERSATION_RESOLUTION: protection_settings.get(REQUIRED_CONVERSATION_RESOLUTION, {}).get(
            ENABLED, False),
        LOCK_BRANCH: protection_settings.get(LOCK_BRANCH, {}).get(ENABLED, False),
        ALLOW_FORK_SYNCING: protection_settings.get(ALLOW_FORK_SYNCING, {}).get(ENABLED, False)
    }
    return updated_settings


if __name__ == "__main__":
    try:
        g = Github(ACCESS_TOKEN)
        curr_user = g.get_user()
        repo = curr_user.get_repo(REPO_NAME)
    except Exception as e:
        print(FETCHING_ERROR)
        exit()
    ConfigurePullReqReviewers(repo, curr_user)
    DisableForcePushing(repo, curr_user)


import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')

FILE_PATH = "CorruptFile.txt"
FILE_CONTENT = "This is an example of how a corrupt file can be injected into the main branch."
COMMIT_MESSAGE = "Updated main branch with corrupt file."
UPDATE_MESSAGE = "Updated branch {} with corrupt file."
CREATE_MESSAGE = "Created corrupt file in branch {}."
FINISHED_COMMIT = "File has been committed and pushed to the main branch."

if __name__ == "__main__":
    g = Github(ACCESS_TOKEN)

    # Specify the repository details
    curr_user = g.get_user()
    repo = curr_user.get_repo(REPO_NAME)
    branch = repo.get_branch(repo.default_branch)

    # Get the SHA of the existing file if it exists
    # Create or update the file
    try:
        contents = repo.get_contents(FILE_PATH, ref=branch.name)
        repo.update_file(contents.path, COMMIT_MESSAGE, FILE_CONTENT, contents.sha, branch=branch.name)
        print(UPDATE_MESSAGE.format(branch.name))
    except:
        repo.create_file(FILE_PATH, COMMIT_MESSAGE, FILE_CONTENT, branch=branch.name)
        print(CREATE_MESSAGE.format(branch.name))

    print(FINISHED_COMMIT)
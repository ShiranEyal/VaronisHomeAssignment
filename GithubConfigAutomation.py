from github import Github

access_token = ""

if __name__ == "__main__":
    g = Github(access_token)
    curr_user = g.get_user()
    print(curr_user.name)
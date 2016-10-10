import requests
from datetime import datetime, timedelta

API_GITHUB_BASE_URL = "https://api.github.com"


def get_trending_repositories(top_size=20, number_of_days=7):
    range_of_time = get_range_of_time_by_given_number_of_days(number_of_days)

    payload = {"q": "created:{0}".format(range_of_time), "sort": "stars&order=desc"}
    repositories = requests.get("{}/search/repositories".format(API_GITHUB_BASE_URL), params=payload).json()

    list_repositories_by_top_size = repositories["items"][:top_size]
    dist = {}

    for count, repo in enumerate(list_repositories_by_top_size):
        repo_owner = repo["owner"]["login"]
        repo_name = repo["name"]
        repo_url = "repo_url"
        open_issues_count = repo["open_issues_count"]

        dist[count] = {"repo_owner": repo_owner, "repo_name": repo_name, "repo_url": repo_url,
                       "open_issues_count": open_issues_count,
                       "list_of_open_issues": get_list_urls_of_open_issues(repo_owner, repo_name)}
    return dist


def get_range_of_time_by_given_number_of_days(number_of_days):
    current_day = datetime.today()
    two_weeks_ago = current_day - timedelta(days=number_of_days)
    return "{0}..{1}".format(two_weeks_ago.strftime("%Y-%m-%d"), current_day.strftime("%Y-%m-%d"))


def get_list_urls_of_open_issues(repo_owner, repo_name):
    payload = {"q": "state:open"}
    open_issues = requests.get("{0}/repos/{1}/{2}/issues".format(API_GITHUB_BASE_URL, repo_owner, repo_name),
                               params=payload).json()

    list_of_open_issue_urls = [issue["html_url"] for issue in open_issues]
    return list_of_open_issue_urls


def print_trending_repositories(data_print):
    print("Most popular repositories is: ")
    for value in data_print.values():
        print("\nUser name is: {0}, repository name is: {1}, \nrepository url is: {2}"
              .format(value["repo_owner"], value["repo_name"], value["repo_url"]))
        print("Number of open issues is: {}.".format(value["open_issues_count"]))
        if int(value["open_issues_count"]):
            print("Open issue urls:")
            for issue in value["list_of_open_issues"]:
                print(issue)


if __name__ == '__main__':
    trending_repositories = get_trending_repositories()
    print_trending_repositories(trending_repositories)

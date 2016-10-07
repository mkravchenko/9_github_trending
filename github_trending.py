import json
import requests
from datetime import datetime, timedelta


def get_trending_repositories(top_size=20):
    time = get_time(7)
    response = requests.get(
        "https://api.github.com/search/repositories?q=created:{0}&sort=stars&order=desc".format(time))
    jdata = json.loads(response.text)
    list_of_best = get_top_repos_by_given_number(jdata, top_size)
    map_of_data_to_print = {

    }
    for count, repo in enumerate(list_of_best):
        dist = {"repo_owner": repo["owner"]["login"],
                "repo_name": repo["name"],
                "repo_url": repo["html_url"],
                "open_issues_count": repo["open_issues_count"]}

        list_of_open_issues = get_list_of_open_issues(dist["repo_owner"], dist["repo_name"])
        dist["list_of_open_issues"] = list_of_open_issues
        map_of_data_to_print[count] = dist

    return map_of_data_to_print


def get_top_repos_by_given_number(jdata, top_size):
    list_of_best = []
    for count, repo in enumerate(jdata["items"]):
        if count == top_size:
            return list_of_best
        else:
            list_of_best.append(repo)
    return None


def get_time(number_of_days):
    current_day = datetime.today()
    two_weeks_ago = current_day - timedelta(days=number_of_days)
    return two_weeks_ago.strftime("%Y-%m-%d") + ".." + current_day.strftime("%Y-%m-%d")


def get_list_of_open_issues(repo_owner, repo_name):
    response = requests.get("https://api.github.com/repos/{0}/{1}/issues".format(repo_owner, repo_name))
    list_of_open_issue_url = []
    for key, issue in enumerate(json.loads(response.text)):
        if issue["state"] == "open":
            list_of_open_issue_url.append(issue["html_url"])
    return list_of_open_issue_url


def print_trending_repositories(data_print):
    print("Most popular repositories is: ")
    for value in data_print.values():
        print("\nUser name is: {0}, repository name is: {1}, \nrepository url is: {2}"
              .format(value["repo_owner"], value["repo_name"], value["repo_url"]))
        print("Number of open issues is: {}.".format(value["open_issues_count"]))
        if int(value["open_issues_count"]) != 0:
            print("Open issue urls:")
            for issue in value["list_of_open_issues"]:
                print(issue)


if __name__ == '__main__':
    trending_repositories = get_trending_repositories()
    print_trending_repositories(trending_repositories)

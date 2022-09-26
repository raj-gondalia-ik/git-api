import json
import requests
import time

BASE_URL = "https://api.github.com/repos/raj-gondalia-ik/git-api/git"


def call_github_api(method, url, params={}, data={}):
    data = json.dumps(data)
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": "token <YOUR_ACCESS_TOKEN>",
    }
    response = requests.request(
        method,
        url,
        headers=headers,
        params=params,
        data=data,
    )
    response_dict = response.json()
    response_str = json.dumps(response_dict, indent=4)
    if not (200 <= response.status_code < 300):
        error_message = (
            f"GitHub API returned non 2xx HTTP status code."
            f"\n"
            f"\nmethod = {method}"
            f"\nurl = {url}"
            f"\nparams = {params}"
            f"\ndata = {data}"
            f"\n"
            f"\nresponse.status_code = {response.status_code}"
            f"\nresponse_str = {response_str}"
            f"\n"
        )
        print(f"call_github_api failure: error_message = {error_message}")
        raise Exception("API failure")
    return response_dict


def get_blob_content(blob_sha):
    url = f"{BASE_URL}/blobs/{blob_sha}"
    response_dict = call_github_api("get", url)
    return {"content": response_dict["content"], "encoding": response_dict["encoding"]}


def create_a_blob(content, encoding):
    url = f"{BASE_URL}/blobs"
    data = {"content": content, "encoding": encoding}
    call_github_api("post", url, data=data)
    return


def copy_a_blob_from_from_repo_to_to_repo(from_repo_blob):
    print(f"copy_a_blob_from_from_repo_to_to_repo: from_repo_blob = {from_repo_blob}")
    from_blob_content = get_blob_content(from_repo_blob["sha"])
    print(f'Length of {from_repo_blob["path"]} is {len(from_blob_content["content"])}')
    print(f"Going to create a blob for from_repo_blob = {from_repo_blob}")
    create_a_blob(
        from_blob_content["content"],
        from_blob_content["encoding"],
    )
    print(f"Created a blob for from_repo_blob = {from_repo_blob}")
    return


def copy_blobs(from_repo_blobs):
    start = time.time()
    for from_repo_blob in from_repo_blobs:
        copy_a_blob_from_from_repo_to_to_repo(from_repo_blob)
    end = time.time()
    print(f"copy_blobs took {end - start}s to execute")


def get_tree_from_tree_sha(tree_sha):
    url = f"{BASE_URL}/trees/{tree_sha}"
    response_dict = call_github_api("get", url, {"recursive": True})
    tree = []
    for item in response_dict["tree"]:
        if item["type"] == "blob":
            tree.append({"sha": item["sha"], "path": item["path"]})
    return tree


if __name__ == "__main__":
    from_repo_blobs = get_tree_from_tree_sha("85b396da024386d8acaefc5ab91c173c5cd6eb86")
    copy_blobs(from_repo_blobs)

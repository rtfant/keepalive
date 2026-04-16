# -*-coding:utf-8 -*-
import requests
import os

API_URL = "https://api.containers.back4app.com"

HEADERS = {
    "Content-type": "application/json",
    "Cookie": os.environ.get("BACK4APP_COOKIE", "")
}

# key: 仓库名, value: serviceEnvironmentId
SERVICE_ENV_MAP = {
    "youquanmo/work-tunnel-vless": "2ff841b1-d343-4139-9d25-5aca1dd2b0a6"
}

def list_apps():
    query = {
        "query": "query Apps { apps { id name mainService { repository { fullName } mainServiceEnvironment { mainCustomDomain { status } } } } }"
    }
    try:
        res = requests.post(API_URL, json=query, headers=HEADERS, timeout=10)
        res.raise_for_status()
        apps = res.json().get("data", {}).get("apps", [])
        return [
            {
                "repo": app["mainService"]["repository"]["fullName"],
                "domain_status": app["mainService"]["mainServiceEnvironment"]["mainCustomDomain"]["status"]
            }
            for app in apps
        ]
    except Exception as e:
        print(f"获取应用列表失败: {e}")
        return []

def trigger_deploy(service_env_id):
    payload = {
        "operationName": "triggerManualDeployment",
        "variables": {"serviceEnvironmentId": service_env_id},
        "query": "mutation triggerManualDeployment($serviceEnvironmentId: String!) { triggerManualDeployment(serviceEnvironmentId: $serviceEnvironmentId) { id status } }"
    }
    try:
        res = requests.post(API_URL, json=payload, headers=HEADERS, timeout=10)
        return res.status_code == 200 and "errors" not in res.text
    except Exception as e:
        print(f"触发部署异常: {e}")
        return False

def main():
    apps = list_apps()
    for app in apps:
        repo = app["repo"]
        status = app["domain_status"]
        if repo not in SERVICE_ENV_MAP:
            continue
        print(f"-> {repo}: {status}")
        if status == "EXPIRED":
            print(f"* {repo}: 域名已过期，触发重新部署...")
            if trigger_deploy(SERVICE_ENV_MAP[repo]):
                print(f"√ {repo}: 部署指令发送成功")
            else:
                print(f"× {repo}: 部署失败")

if __name__ == "__main__":
    main()

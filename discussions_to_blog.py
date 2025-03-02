import os  
import requests  
import json  

# GitHub GraphQL API  
GRAPHQL_API = "https://api.github.com/graphql"  

def fetch_discussions(github_token, repo_owner, repo_name, category_id):  
    """从 GitHub GraphQL API 获取 Discussions 数据"""  
    query = """  
    query($repoOwner: String!, $repoName: String!, $categoryId: ID!) {  
      repository(owner: $repoOwner, name: $repoName) {  
        discussions(first: 100, categoryId: $categoryId) {  
          nodes {  
            id  
            title  
            body  
            createdAt  
            updatedAt  
          }  
        }  
      }  
    }  
    """  
    headers = {  
        "Authorization": f"Bearer {github_token}",  
        "Content-Type": "application/json"  
    }  
    payload = {  
        "query": query,  
        "variables": {  
            "repoOwner": repo_owner,  
            "repoName": repo_name,  
            "categoryId": category_id  
        }  
    }  
    response = requests.post(GRAPHQL_API, json=payload, headers=headers)  
    response.raise_for_status()  
    data = response.json()  
    return data["data"]["repository"]["discussions"]["nodes"]  

def sanitize_filename(title):  
    """对标题进行处理，转换为合法文件名"""  
    return title.strip().replace(" ", "-").replace("/", "-").replace("\\", "-").lower()  

def write_markdown(discussion, output_dir):  
    """将 Discussions 数据写入 Markdown 文件"""  
    created_at = discussion["createdAt"]  
    year = created_at[:4]  
    month = created_at[5:7]  
    post_dir = os.path.join(output_dir, year, month)  
    os.makedirs(post_dir, exist_ok=True)  

    filename = f"{sanitize_filename(discussion['title'])}.md"  
    filepath = os.path.join(post_dir, filename)  

    # Markdown 文件内容  
    front_matter = f"""---  
title: "{discussion['title']}"  
date: "{discussion['createdAt']}"  
draft: false  
discussion_id: "{discussion['id']}"  
---  
"""  
    content = front_matter + "\n" + discussion["body"]  

    # 写入文件  
    with open(filepath, "w", encoding="utf-8") as f:  
        f.write(content)  
    print(f"[INFO] 文件已生成：{filepath}")  

    return discussion["id"]  

def delete_removed_files(old_ids, current_ids, output_dir):  
    """删除已不存在 Discussions 的 Markdown 文件"""  
    removed_ids = set(old_ids) - set(current_ids)  
    if not removed_ids:  
        print("[INFO] 未检测到需要删除的文件")  
        return  

    for root, _, files in os.walk(output_dir):  
        for file in files:  
            if file.endswith(".md"):  
                filepath = os.path.join(root, file)  
                with open(filepath, "r", encoding="utf-8") as f:  
                    content = f.read()  
                if any(f'discussion_id: "{rid}"' in content for rid in removed_ids):  
                    os.remove(filepath)  
                    print(f"[INFO] 已删除文件：{filepath}")  

def load_cache(cache_file):  
    """加载缓存文件，并返回 IDs 列表"""  
    if os.path.exists(cache_file):  
        with open(cache_file, "r", encoding="utf-8") as f:  
            return json.load(f)  
    return []  

def save_cache(cache_file, ids):  
    """保存当前 IDs 列表到缓存文件"""  
    with open(cache_file, "w", encoding="utf-8") as f:  
        json.dump(ids, f)  

def run(github_token, repo_owner, repo_name, category_id, output_dir, delete_on_removed):  
    """执行 Discussions 同步和 Markdown 文件生成的主流程"""  
    # 拉取 Discussions 数据  
    discussions = fetch_discussions(github_token, repo_owner, repo_name, category_id)  

    # 加载缓存文件  
    cache_file = ".discussions_cache.json"  
    old_ids = load_cache(cache_file)  

    # 写入 Markdown 文件  
    current_ids = []  
    for discussion in discussions:  
        discussion_id = write_markdown(discussion, output_dir)  
        current_ids.append(discussion_id)  

    # 删除不存在的 Discussions 的 Markdown 文件  
    if delete_on_removed:  
        delete_removed_files(old_ids, current_ids, output_dir)  

    # 保存最新 ID 列表到缓存  
    save_cache(cache_file, current_ids)  
    print("[INFO] Discussions 同步完成！")
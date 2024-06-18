import requests
import os
from pprint import pprint
import time

# GitHub user token
GITHUB_PERSONAL_TOKEN = os.environ.get('GITHUB_PERSONAL_TOKEN')

# PRのコメントを取得する
async def get_pr_comment(owner, repo, pr_number, find_text, loop_count=0):
    # GitHub APIのエンドポイント
    GITHUB_API_URL = "https://api.github.com"

    # GitHubリポジトリ情報
    OWNER = owner
    REPO = repo
    # プルリクエスト番号
    PR_NUMBER = pr_number

    # APIリクエスト用ヘッダー
    headers = {
        "Authorization": f"token {GITHUB_PERSONAL_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 特定のPRのコメントを取得するエンドポイント
    comments_url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/issues/{PR_NUMBER}/comments"

    # コメントを取得するためのGETリクエスト
    response = requests.get(comments_url, headers=headers)

    # レスポンスのステータスコードをチェック
    if response.status_code == 200:
        comments = response.json()
        answer = ""

        is_find = False
        for comment in comments:
            body = comment['body']
            # find_text = "このPRに対して、美しいポエムを書いて下さい。英語でお願いします。短めで。"

            if find_text in body:
                pprint(body)
                # '### **Answer:**' の位置を見つける
                start_index = body.find('### **Answer:**')
                if start_index != -1:
                    start_index += len('### **Answer:**')
                    # '### **Ask**' の位置を見つけてその前までを抽出
                    end_index = body.find('### **Ask**', start_index)
                    if end_index == -1:
                        answer = body[start_index:].strip()
                    else:
                        answer = body[start_index:end_index].strip()
                    print(answer)
                    is_find = True
                    return comments, answer
                else:
                    print("### **Answer:** が見つかりませんでした。")
                    is_find = False

        # 見つからなかった場合
        if is_find == False:
            print("見つかりませんでした。60秒待って再度取得します。")
            # カウントを超えたら終了
            if loop_count < 5:
                loop_count += 1
            else:
                return comments, answer

            # 1分待つ
            time.sleep(60)

            # 再帰で見つかるまで探す
            return get_pr_comment(owner, repo, pr_number, find_text, loop_count)

        return comments, answer
    else:
        print(f"Failed to fetch comments: {response.status_code}")

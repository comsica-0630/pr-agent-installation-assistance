import requests
import os
import json
from openai import OpenAI

# OpenAI key
OPEN_ID_API_KEY = os.environ.get('OPEN_ID_API_KEY')
os.environ['OPENAI_API_KEY']=OPEN_ID_API_KEY

# GitHub user token
GITHUB_PERSONAL_TOKEN = os.environ.get('GITHUB_PERSONAL_TOKEN')

# 絵を生成する関数
def generate_image(owner, repo, pr_number, prompt):
    # GitHub APIのエンドポイント
    GITHUB_API_URL = "https://api.github.com"

    # APIリクエスト用ヘッダー
    headers = {
        "Authorization": f"token {GITHUB_PERSONAL_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # OpenAIのクライアントを作成
    client = OpenAI()

    # prompt追加
    add_prompt = """
        Please observe the following restrictions.
        - Please make it a pretty picture.
        - Please have animals appear in the picture, even if only occasionally.
        - I like cats and dogs.
        - Please don't make the picture too mechanical.

        The following are the prompts used to generate the images.
        Please draw a picture from this prompt.
    """

    # 追加promptとpromptを結合
    prompt = f"{add_prompt} : {prompt}"

    # E3
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
        # style="vivid",
        style="natural",
    )

    image_url = response.data[0].url

    print(image_url)

    # GitHubリポジトリ情報
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues/{pr_number}/comments"

    print(url)
    print(image_url)

    # コメントの本文
    data = {
        "body": f"![PRの絵]({image_url})"
    }

    # コメントを投稿するPOSTリクエスト
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 201:
        print("コメントが正常に投稿されました。")
    else:
        print(f"コメントの投稿に失敗しました。ステータスコード: {response.status_code}")

    return image_url, response

# .envを読み込むライブラリ
from dotenv import load_dotenv
load_dotenv()
import os
import asyncio
import sys
import json

# 自作パーツ
from get_pr_comment import get_pr_comment
from generate_image import generate_image
from pr_agent_mod import pr_agent_run

# # env読み込み
# OpenAI key
OPEN_ID_API_KEY = os.environ.get('OPEN_ID_API_KEY')
# GitHub user token
GITHUB_PERSONAL_TOKEN = os.environ.get('GITHUB_PERSONAL_TOKEN')

# PR-AGENTを実行する関数
async def main():
    # PR URL, for example
    # https://github.com/comsica-0630/pr-agent-installation-assistance-test
    # "{"prNumber":1,"owner":"comsica-0630","repo":"pr-agent-installation-assistance-test"}"

    # # 対象PR
    # owner = "comsica-0630"
    # repo = "pr-agent-installation-assistance-test"

    # 引数取得
    args = sys.argv

    # 引数取得
    arg_string = args[1]
    
    print(arg_string)
        
    # dictに変換
    arg_dict = json.loads(arg_string)

    print(arg_dict)

    # owner取得
    owner = arg_dict["owner"]
    # repo取得
    repo = arg_dict["repo"]
    # pr_number取得
    pr_number = arg_dict["prNumber"]

    print(owner)
    print(repo)
    print(pr_number)

    # PR URL
    pr_url = f"https://github.com/{owner}/{repo}/pull/{pr_number}"

    print(pr_url)

    command = "/ask 今からレビューを始めます。このPRはどういう目的の修正ですか？"
    await pr_agent_run(command, pr_url)

    # command = "/describe"
    # await pr_agent_run(command, pr_url)

    # command = "/review"
    # await pr_agent_run(command, pr_url)

    # command = "/improve"
    # await pr_agent_run(command, pr_url)

    command = "/ask このPRに対して、美しいポエムを書いて下さい。日本語でお願いします。短めで。"
    await pr_agent_run(command, pr_url)

    connect_gen_image_text = "このPRに対して、美しいポエムを書いて下さい。英語でお願いします。短めで。"
    command = f"/ask {connect_gen_image_text}"
    await pr_agent_run(command, pr_url)

    # PRコメント取得
    comments, answer = await get_pr_comment(owner, repo, pr_number, connect_gen_image_text)

    print(answer)

    # PRコメントをそのまま画像生成promptとして渡す
    prompt = answer

    # 画像生成してpost
    image_url, response = generate_image(owner, repo, pr_number, prompt)

    print(image_url)

# 実行
asyncio.run(main())

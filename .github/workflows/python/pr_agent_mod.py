# .envを読み込むライブラリ
from dotenv import load_dotenv
load_dotenv()
import os
from pr_agent import cli
from pr_agent.config_loader import get_settings
import nest_asyncio
nest_asyncio.apply()

# env読み込み
# OpenAI key
OPEN_ID_API_KEY = os.environ.get('OPEN_ID_API_KEY')
# GitHub user token
GITHUB_PERSONAL_TOKEN = os.environ.get('GITHUB_PERSONAL_TOKEN')

# PR-AGENTを実行する関数
async def pr_agent_run(command, pr_url):
    # GitHub provider
    provider = "github"

    # 指示プロンプト
    PR_DESCRIPTION_EXTRA_INSTRUCTIONS = 'answer in japanese. Titles should have prefix of commitlint pattern such as `feat:`, `chore:`, `test:`, `fix:`, `ci:`, `docs:` etc'
    EXTRA_INSTRUCTIONS = 'answer in japanese.'

    improve_add_prompt = """
    - any型を使わないようにしてください。推論出来る場合はanyに型をつけて下さい。
    """

    # AI model
    # MODEL = "gpt-4o"
    MODEL = "gpt-3.5-turbo"

    # Setting the configurations
    get_settings().set("CONFIG.model", MODEL)

    get_settings().set("CONFIG.git_provider", provider)
    get_settings().set("openai.key", OPEN_ID_API_KEY)
    get_settings().set("github.user_token", GITHUB_PERSONAL_TOKEN)

    # 指示プロンプト：レビュー（review）
    get_settings().set("pr_reviewer.extra_instructions", EXTRA_INSTRUCTIONS)
    get_settings().set("pr_reviewer.inline_code_comments", True)

    # 指示プロンプト：PR説明（describe）
    get_settings().set("pr_description.extra_instructions", PR_DESCRIPTION_EXTRA_INSTRUCTIONS)
    # 指示プロンプト：修正提案（improve）
    get_settings().set("pr_code_suggestions.extra_instructions", f"{EXTRA_INSTRUCTIONS} : {improve_add_prompt}")
    # 指示プロンプト：質問（ask）
    get_settings().set("pr_questions.extra_instructions", EXTRA_INSTRUCTIONS)

    # 指示プロンプト：
    get_settings().set("pr_add_docs.extra_instructions", EXTRA_INSTRUCTIONS)
    # 指示プロンプト：
    get_settings().set("pr_update_changelog.extra_instructions", EXTRA_INSTRUCTIONS)
    # 指示プロンプト：
    get_settings().set("pr_analyze.extra_instructions", EXTRA_INSTRUCTIONS)
    # 指示プロンプト：
    get_settings().set("pr_improve_component.extra_instructions", EXTRA_INSTRUCTIONS)

    # 実行！
    cli.run_command(pr_url, command)

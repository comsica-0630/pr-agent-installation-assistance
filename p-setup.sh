# 別途python3.12のインストールが必要

# 仮想環境の作成
python -m venv .venv

# 仮想環境の有効化
source .venv/bin/activate

# notebook kernelのインストール
python -m pip install ipykernel -U --force-reinstall
python -m ipykernel install --user --name=python3.12.3 --display-name=python3.12.3

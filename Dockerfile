FROM python:3.11-slim

# 必要なライブラリをすべてインストール（Playwright対応）
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libxss1 libasound2 libxcomposite1 libxrandr2 libgbm-dev \
    libxdamage1 libxfixes3 libxkbcommon0 \
    libpango-1.0-0 libcairo2 \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリとコードコピー
WORKDIR /app
COPY . /app

# PythonライブラリとPlaywrightのインストール
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    playwright install chromium

# ✅ デバッグ出力付きの起動コマンド
CMD ["sh", "-c", "echo '▶️ コンテナ起動確認' && ls -la && echo '▶️ Python実行' && python update_playlist.py"]

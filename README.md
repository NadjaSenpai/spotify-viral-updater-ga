<<<<<<< HEAD
# 🎧 Spotify Japan Viral 50 Playlist Updater

![Deploy Status](https://github.com/NadjaSenpai/spotify-viral-updater/actions/workflows/deploy.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.6%2B-blue)

Spotify Charts の「Daily Viral Songs Japan」を毎日取得し、指定した Spotify プレイリストを全自動で更新するスクリプトです。

Spotify の [バイラルトップ50 - 日本 / Japan Viral 50](https://open.spotify.com/playlist/37i9dQZEVXbINTEnbFeb8d) を [Soundiiz](https://soundiiz.com/ja/) などで同期して  
Apple Music などでも聴きたい！と思ったんですが、  
バイラルチャートはチャートであってプレイリストではないためインポートできません。  
なので変換してプレイリストにしてしまおう！という目論見で作りました。  
GitHub Actions で毎日更新できるようにしています。

ChatGPT といっしょに作りました。というか9割作ってもらった。

`https://charts.spotify.com/charts/view/viral-jp-daily/latest` を別のチャートにしても動くと思います。

サンプル:  
https://open.spotify.com/playlist/4Bf4jxM1WylLwqLmld8mbU

<img src="https://github.com/user-attachments/assets/c6e0ad33-5ecf-4680-ba3d-80b09efb1f84" width="720">

## 動作

- Playwright で Charts サイトにログインして CSV を取得
- Spotipy + Refresh Token でプレイリストを操作
- Fly.io でホスト、 GitHub Actions で定期実行

## セットアップ

1. `.env` を用意（各種認証情報）

```env
   SPOTIPY_CLIENT_ID=xxxx  
   SPOTIPY_CLIENT_SECRET=xxxx  
   SPOTIPY_REDIRECT_URI=http://localhost:8888/callback  
   SPOTIFY_REFRESH_TOKEN=xxxx  
   SPOTIFY_PLAYLIST_ID=プレイリストID  
   STATE_JSON_B64=base64化したstate.json  
```

2. ローカルでログイン状態を保存

   `python save_session.py`
   → ログイン後に `state.json` を base64化して `.env` に貼る

3. Fly.io へデプロイ

```
   fly launch  
   fly secrets set $(cat .env | xargs)  
   fly deploy
```

## GitHub Actionsでの定期実行

`.github/workflows/deploy.yml` により毎日 9:00 JST に Fly.io へ自動再デプロイされます。

事前に Fly.io の API トークンを GitHub の Secrets に登録してください：

   `fly auth token` → `FLY_API_TOKEN` として保存

## 使用技術

- Python + Playwright
- Spotipy (Spotify Web API)
- Fly.io + GitHub Actions
=======
# 🎧 Spotify Japan Viral 50 Playlist Updater

![Deploy Status](https://github.com/NadjaSenpai/spotify-viral-updater-ga/actions/workflows/docker-run.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)

Spotify Charts の「Daily Viral Songs Japan」を毎日取得し、指定した Spotify プレイリストを全自動で更新するスクリプトです。

Spotify の [バイラルトップ50 - 日本 / Japan Viral 50](https://open.spotify.com/playlist/37i9dQZEVXbINTEnbFeb8d) を [Soundiiz](https://soundiiz.com/ja/) や [Tune My Music](https://www.tunemymusic.com/jp) で同期して  
Apple Music や Amazon Music Unlimited とかでも聴きたい！と思ったんですが、  
バイラルチャートはチャートであってプレイリストではないためインポートできませんでした。  
なので変換してプレイリストにしてしまおう！という目的で作成しました。  

https://github.com/NadjaSenpai/spotify-viral-updater  
こちらのリポジトリではFly.ioと連携していたんですが、  
DockerならGitHub Actionsだけでもいけるじゃん、って気づいてしまったので  
現在は GitHub Actions + Docker のみで毎日自動更新しています。

ChatGPT といっしょに作りました。というか 95% ぐらい作ってもらった。

`https://charts.spotify.com/charts/view/viral-jp-daily/latest` を別のチャートにしても動作します。

サンプルプレイリスト:  
https://open.spotify.com/playlist/4Bf4jxM1WylLwqLmld8mbU

## 動作概要

- Playwright で Spotify Charts サイトから CSV をダウンロード
- Spotipy + Refresh Token で Spotify プレイリストを全更新（全削除 → 追加）
- GitHub Actions + Docker による定期実行（毎日 9:00 JST）

## セットアップ手順

### 1. `.env` を作成

```env
SPOTIPY_CLIENT_ID=xxxx
SPOTIPY_CLIENT_SECRET=xxxx
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
SPOTIFY_REFRESH_TOKEN=xxxx
SPOTIFY_PLAYLIST_ID=プレイリストID
STATE_JSON_B64=base64化したstate.json
```

### 2. `state.json` を取得してエンコード

```bash
python save_session.py
# ログイン後に Enter を押すと state.json が保存され、base64 文字列が出力されます
# → それを GitHub Secrets に貼り付けてください（キー: STATE_JSON_B64）
```

### 3. Refresh Token の取得

```bash
python get_refresh_token.py
# 表示された URL を開いて Spotify にログイン
# リダイレクト後の URL を貼り付けて Enter
# → refresh_token が表示されます
```

取得した値を `.env` に記載、または GitHub Secrets に保存します。

## GitHub Actions 定期実行

`.github/workflows/docker-run.yml` により、毎日 9:00 JST に自動実行されます。

### 必要な Secrets

| Key                    | 説明                            |
|------------------------|---------------------------------|
| SPOTIPY_CLIENT_ID      | Spotify の Client ID           |
| SPOTIPY_CLIENT_SECRET  | Spotify の Client Secret       |
| SPOTIPY_REDIRECT_URI   | http://127.0.0.1:8888/callback |
| SPOTIFY_REFRESH_TOKEN  | 取得した Refresh Token         |
| SPOTIFY_PLAYLIST_ID    | プレイリストの ID（末尾部分）  |
| STATE_JSON_B64         | base64 エンコードした state.json |

## 使用技術

- Python 3.11
- Playwright（CSVダウンロード自動化）
- Spotipy（Spotify API）
- Docker + GitHub Actions（自動実行）
>>>>>>> cdef87552264fe1d8c5220990f2781d9aefd1e20

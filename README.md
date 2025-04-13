# 🎧 Spotify Japan Viral 50 Playlist Updater
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

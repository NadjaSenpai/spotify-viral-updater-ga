# spotify-viral-updater
ChatGPT といっしょに作りました。というか9割作ってもらった。  

Spotify の [バイラルトップ50 - 日本 / Japan Viral 50](https://open.spotify.com/playlist/37i9dQZEVXbINTEnbFeb8d) をSoundiizなどで同期して  
Apple Music などでも聴きたい！と思ったんですが、  
バイラルチャートはチャートであってプレイリストではないためインポートできません。  
というわけで、変換してプレイリストにするやつです。  
GitHub Actions で毎日更新できるようにしています。

必要な手順：

1. [Spotify for Developers](https://developer.spotify.com/dashboard) でアプリを登録
2. `.env.example` を `.env` にリネームし、認証情報を入力
3. `save_session.py` をローカルで実行し、Spotify Charts にログイン → `state.json` が生成される
4. `state.json` の内容を GitHub Secrets に `STATE_JSON` として追加
5. 他の認証情報（Client ID/Secretなど）も同様に GitHub Secrets に追加
6. `update.yml` が毎日12:00 JST に自動実行！
   だそうです。

`https://charts.spotify.com/charts/view/viral-jp-daily/latest` を別のチャートにしても動くと思います。
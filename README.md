# linebot-docker
# 2025/5/27
# 目前架構
# app.py 主程式碼
# Dockerfile Docker 環境建設
# ngrok/Dockerfile 使ngrok在Docker上運行(記得在.env上放上自己的NGROK_AUTHTOKEN!!)
# docker-compose 用來定義「多個容器服務（Services）」如何一起運作。 你可以在裡面定義多個服務，例如你的 LineBot Flask app 一個服務，ngrok 一個服務，還可以設定網路、端口映射、環境變數、卷掛載等。
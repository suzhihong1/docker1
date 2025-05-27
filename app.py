# 匯入 Flask 與 LINE Bot SDK 所需模組
from flask import Flask, request, abort  # 用於建立網頁應用與處理 HTTP 請求
from linebot import LineBotApi, WebhookHandler  # LINE SDK 的核心類別
from linebot.exceptions import InvalidSignatureError  # 用來處理驗證失敗的例外狀況
from linebot.models import MessageEvent, TextMessage, TextSendMessage  # 處理文字訊息的模型
import os  # 用來讀取環境變數

# 建立 Flask 應用
app = Flask(__name__)

# 初始化 LINE Bot API 與 Webhook 處理器，從環境變數讀取金鑰
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# 定義 webhook 接收點，LINE 平台會對這個路徑 POST 訊息
@app.route("/callback", methods=["POST"])
def callback():
    # 從 HTTP 標頭中取得 X-Line-Signature（LINE 用來驗證請求是否合法）
    signature = request.headers["X-Line-Signature"]
    # 取得 POST 的請求內容（JSON 字串）
    body = request.get_data(as_text=True)

    try:
        # 驗證簽章並處理事件
        handler.handle(body, signature)
    except InvalidSignatureError:
        # 簽章不正確時，回傳 400 錯誤
        abort(400)

    # 成功處理後回傳 OK 給 LINE 平台
    return "OK"

# 設定事件處理函式：當接收到使用者發送的文字訊息時執行
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 回覆使用者一段訊息：「你說了：xxxx」
    reply = TextSendMessage(text=f"你說了：{event.message.text}")
    # 使用 reply_token 回覆訊息
    line_bot_api.reply_message(event.reply_token, reply)

# 主程式入口點：啟動 Flask 應用在 0.0.0.0 的 8080 port 上
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

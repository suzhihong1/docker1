from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import yfinance as yf
import os
from dotenv import load_dotenv

load_dotenv()  # 讀取 .env 內的環境變數

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

app = Flask(__name__)

def get_stock_price(symbol: str):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d", interval="1m")
    if data.empty:
        return None
    latest_price = data['Close'].iloc[-1]
    return latest_price

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print("Webhook Error:", e)
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()

    if user_text.startswith("查股價"):
        try:
            symbol = user_text.split(" ")[1].upper()
            price = get_stock_price(symbol)

            if price is not None:
                reply_text = f"📈 {symbol} 最新價格：${price:.2f}"
            else:
                reply_text = f"❗ 無法取得 {symbol} 的股價資訊，請確認代碼是否正確。"

        except IndexError:
            reply_text = "請輸入股票代碼，例如：查股價 AAPL"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )

    else:
        default_reply = (
            "歡迎使用📊市場查詢機器人！\n"
            "請輸入以下格式來查詢股票資訊：\n\n"
            "🔹 查股價 AAPL\n🔹 查股價 TSLA\n🔹 查股價 2330.TW"
        )
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=default_reply)
        )

if __name__ == "__main__":
    app.run(debug=True)

import yfinance as yf
from twilio.rest import Client

# === Config ===
TWILIO_SID = 'YOUR_KEY'
TWILIO_AUTH_TOKEN = 'YOUR_KEY'
TWILIO_PHONE_NUMBER = 'YOUR_KEY'
RECEIVER_PHONE_NUMBER = 'YOUR_KEY'
PERCENT_CHANGE_THRESHOLD = 1

COMPANIES = {
    "PHDC.CA": "Palm Hills Developments",
    "SWDY.CA": "Elsewedy Electric"
}

GOLD_TICKER = "GC=F"
SILVER_TICKER = "SI=F"
USD_EGP_TICKER = "USDEGP=X"

def get_egypt_stock_prices(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="5d")
    if len(hist) < 4:
        raise ValueError(f"Not enough historical data for {symbol}")
    closes = hist['Close'].iloc[-4:].round(2).tolist()
    return closes

def get_latest_close_price(ticker, days=5):
    data = yf.Ticker(ticker)
    hist = data.history(period=f"{days}d")
    if len(hist) < 2:
        raise ValueError(f"Not enough data for {ticker}")
    closes = hist['Close'].iloc[-2:].round(2).tolist()
    return closes


def send_sms(message):
    print(f"Using SID: {TWILIO_SID}, Auth Token: {TWILIO_AUTH_TOKEN[:4]}***")
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    msg = client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=RECEIVER_PHONE_NUMBER
    )
    print(f"SMS sent with SID: {msg.sid}")

# === Main ===
all_prices_summaries = []
significant_changes_summaries = []

# Fetch USD to EGP exchange rate
try:
    usd_egp_prices = get_latest_close_price(USD_EGP_TICKER)
    usd_egp_rate = usd_egp_prices[-1]
    print(f"USD to EGP rate: {usd_egp_rate}")
except Exception as e:
    print(f"Error fetching USD/EGP exchange rate: {e}")
    usd_egp_rate = None

# Process company stocks
for symbol, company in COMPANIES.items():
    try:
        prices = get_egypt_stock_prices(symbol)
        change_percent = ((prices[-1] - prices[-2]) / prices[-2]) * 100
        change_symbol = "UP" if change_percent > 0 else "DOWN"
        
        price_summary = f"Prices (last 4 days): {', '.join([str(p) + ' EGP' for p in prices])}"
        full_summary = f"{symbol} - {company}: {change_symbol} {abs(change_percent):.2f}%\n{price_summary}\n"
        
        print(full_summary)
        
        all_prices_summaries.append(full_summary)
        
        if abs(change_percent) >= PERCENT_CHANGE_THRESHOLD:
            significant_changes_summaries.append(full_summary)
            
    except Exception as e:
        print(f"Error processing {symbol}: {e}")

# Fetch gold prices in USD and convert to EGP
if usd_egp_rate:
    try:
        gold_prices_usd = get_latest_close_price(GOLD_TICKER, days=5)
        gold_change_pct = ((gold_prices_usd[-1] - gold_prices_usd[-2]) / gold_prices_usd[-2]) * 100
        gold_price_egp_per_oz = gold_prices_usd[-1] * usd_egp_rate
        gold_price_egp_per_g = round(gold_price_egp_per_oz / 31.1035, 2)  # convert oz to g
        gold_change_symbol = "UP" if gold_change_pct > 0 else "DOWN"
        gold_summary = f"Gold Price: {gold_price_egp_per_g} EGP/g ({gold_change_symbol} {abs(gold_change_pct):.2f}%)"
        print(gold_summary)
        all_prices_summaries.append(gold_summary)
        if abs(gold_change_pct) >= PERCENT_CHANGE_THRESHOLD:
            significant_changes_summaries.append(gold_summary)
    except Exception as e:
        print(f"Error fetching gold price: {e}")

    try:
        silver_prices_usd = get_latest_close_price(SILVER_TICKER, days=5)
        silver_change_pct = ((silver_prices_usd[-1] - silver_prices_usd[-2]) / silver_prices_usd[-2]) * 100
        silver_price_egp_per_oz = silver_prices_usd[-1] * usd_egp_rate
        silver_price_egp_per_g = round(silver_price_egp_per_oz / 31.1035, 2)  # convert oz to g
        silver_change_symbol = "UP" if silver_change_pct > 0 else "DOWN"
        silver_summary = f"Silver Price: {silver_price_egp_per_g} EGP/g ({silver_change_symbol} {abs(silver_change_pct):.2f}%)"
        print(silver_summary)
        all_prices_summaries.append(silver_summary)
        if abs(silver_change_pct) >= PERCENT_CHANGE_THRESHOLD:
            significant_changes_summaries.append(silver_summary)
    except Exception as e:
        print(f"Error fetching silver price: {e}")


# Send all prices info no matter what
send_sms("Prices Summary:\n\n" + "\n".join(all_prices_summaries))

# Optionally send separate SMS for significant changes only
if significant_changes_summaries:
    send_sms("Significant Changes:\n\n" + "\n".join(significant_changes_summaries))
else:
    print("No significant changes above threshold.")

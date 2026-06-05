from binance.client import Client 

client = Client()

def current_print():
    symbol_input = input("Symbol: ")
    ticker = client.get_symbol_ticker(symbol=F"{symbol_input}")

    print(f"Price for the symbol {symbol_input} is: {ticker['price']}")

current_print()
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import http.client
import json
import datetime


# Function to get the cryptocurrency exchange rate
def get_crypto_exchange_rate(): # функция
    selected_crypto = crypto_combobox.get()  # Get the selected cryptocurrency
    selected_fiat = fiat_combobox.get()  # Get the selected fiat currency

    # Check if both the cryptocurrency and fiat currency are selected
    if selected_crypto and selected_fiat:
        try:
            # Connect to CoinGecko API
            connection = http.client.HTTPSConnection("api.coingecko.com")
            endpoint = f"/api/v3/simple/price?ids={selected_crypto.lower()}&vs_currencies={selected_fiat.lower()}"

            # Send request to API
            connection.request("GET", endpoint)
            response = connection.getresponse()  # Get response from server
            data = response.read().decode("utf-8")  # Decode data

            # Convert JSON response to a dictionary
            exchange_info = json.loads(data)

            # Check if the data contains information about the selected currencies
            if selected_crypto.lower() in exchange_info and selected_fiat.lower() in exchange_info[selected_crypto.lower()]:
                crypto_rate = exchange_info[selected_crypto.lower()][selected_fiat.lower()]
                current_date = datetime.datetime.now().strftime("%d-%m-%Y")  # Get the current date

                # Show the exchange rate information
                mb.showinfo(f"Exchange Rate on {current_date}",
                            f"Rate: {crypto_rate:.1f} {selected_fiat} for 1 {selected_crypto} on {current_date}")
            else:
                mb.showerror("Error", f"Data for cryptocurrency {selected_crypto} is not available")
        except Exception as error:
            # Show error message in case of a failed request
            mb.showerror("Error", f"Error fetching data: {error}")
    else:
        # Show a warning if no cryptocurrency or fiat currency is selected
        mb.showwarning("Warning", "Please select both a cryptocurrency and a fiat currency")


# List of cryptocurrencies
cryptocurrencies = ["Bitcoin", "Ethereum", "Solana", "WPTC", "Tether", "Cardano", "Ripple", "Polkadot", "Dogecoin", "Binancecoin"]

# List of fiat currencies
fiat_currencies = ["USD", "EUR", "RUB", "GBP", "JPY", "CHF"]

# Create the main application window
main_window = Tk()
main_window.title("Cryptocurrency Converter")
main_window.geometry("360x250")  # Set window size

# Label for selecting fiat currency
Label(main_window, text="Select Fiat Currency", bg="#c9c9d6", fg="#132440", font="Arial 10 bold").pack(padx=10, pady=5)

# Dropdown list for selecting fiat currency
fiat_combobox = ttk.Combobox(main_window, values=fiat_currencies)
fiat_combobox.pack(padx=10, pady=5)

# Label for selecting cryptocurrency
Label(main_window, text="Select Cryptocurrency", bg="#c9c9d6", fg="#132440", font="Arial 10 bold").pack(padx=10, pady=5)

# Dropdown list for selecting cryptocurrency
crypto_combobox = ttk.Combobox(main_window, values=cryptocurrencies)
crypto_combobox.pack(padx=10, pady=5)

# Button to get the exchange rate
Button(main_window, text="Show Exchange Rate", bg="#132440", fg="#f9f8f8", font="Arial 10 bold",
       command=get_crypto_exchange_rate).pack(padx=10, pady=10)

# Start the main event loop
main_window.mainloop()




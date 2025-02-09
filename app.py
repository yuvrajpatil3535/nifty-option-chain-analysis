import requests
import pandas as pd
import matplotlib.pyplot as plt
app = Flask(__name__)


# Define the API URL (Replace with actual API endpoint)
API_URL = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_option_chain():
    response = requests.get(API_URL, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data")
        return None

def process_data(data):
    option_data = data['records']['data']
    df = pd.DataFrame()
    
    for entry in option_data:
        if 'CE' in entry and 'PE' in entry:
            df = df.append({
                'strikePrice': entry['strikePrice'],
                'CE_OI': entry['CE']['openInterest'],
                'PE_OI': entry['PE']['openInterest'],
                'OI_Diff': entry['CE']['openInterest'] - entry['PE']['openInterest']
            }, ignore_index=True)
    
    # Sort by Open Interest difference and pick top 6 rows
    df = df.sort_values(by='OI_Diff', ascending=False).head(6)
    return df

def plot_trend(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df['strikePrice'], df['OI_Diff'], marker='o', linestyle='-', color='b')
    plt.xlabel('Strike Price')
    plt.ylabel('Open Interest Difference (CE - PE)')
    plt.title('Nifty Option OI Trend')
    plt.grid(True)
    plt.show()

def main():
    data = fetch_option_chain()
    if data:
        df = process_data(data)
        print(df)
        plot_trend(df)

if __name__ == "__main__":
    main()

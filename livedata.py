import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
from alpha_vantage.timeseries import TimeSeries

# Set page title
st.title("Stock Market Selector")

# Create market selection
market = st.selectbox(
    "Select Market",
    ["US", "Europe", "Asia"],
    help="Choose the market region you want to invest in"
)

# Dictionary of stocks by market
stocks = {
    "US": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "PFE", "JPM", "WMT", "KO"],
    "Europe": ["SAP.DE", "ASML.AS", "LVMH.PA", "NOVO.CO", "ROG.SW", "SAN.MC", "UL.AS", "AIR.PA", "SIE.DE", "BAYN.DE"],
    "Asia": ["9988.HK", "005930.KS", "7203.T", "1398.HK", "600519.SS", "035420.KS", "6758.T", "000660.KS", "2330.TW", "1299.HK"]
}

# Show stock selector based on market
selected_stocks = st.multiselect(
    f"Select Stocks from {market} Market",
    stocks[market],
    help="Choose multiple stocks to analyze"
)

if selected_stocks:
    st.write("You selected:", ", ".join(selected_stocks))
    
    # Display selected stocks in a table format
    stock_data = {
        "Symbol": selected_stocks,
        "Market": [market] * len(selected_stocks)
    }
    st.dataframe(stock_data)

    # Create a line chart for live stock prices
    
    
    # Get data for selected stocks
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)  # Last 30 days of data
    
    # Create figures for price and volume analysis
    price_fig = go.Figure()
    volume_fig = go.Figure()
    
    # Add data for each selected stock
    for symbol in selected_stocks:
        # Get stock data
        stock = yf.Ticker(symbol)
        try:
            try:
                # Try yfinance first
                df = stock.history(start=start_date, end=end_date)
                
                # Get company info
                info = stock.info
                company_name = info.get('longName', symbol)
                sector = info.get('sector', 'N/A')
                market_cap = info.get('marketCap', 0)
                market_cap_str = f"${market_cap/1e9:.2f}B" if market_cap else 'N/A'
                
                # Calculate key metrics
                price_change = ((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0]) * 100
                avg_volume = df['Volume'].mean()
                
                # Display company overview
                st.subheader(f"{company_name} ({symbol})")
                col1, col2, col3 = st.columns(3)
                col1.metric("Sector", sector)
                col2.metric("Market Cap", market_cap_str)
                col3.metric("30-Day Price Change", f"{price_change:.2f}%")
                
            except:
                # Fallback to alpha_vantage
                ts = TimeSeries(key='8IUIFDZR3D72YDDQ')
                data, _ = ts.get_daily(symbol=symbol)
                df = pd.DataFrame.from_dict(data, orient='index')
                df.index = pd.DatetimeIndex(df.index)
                df = df.rename(columns={'4. close': 'Close', '5. volume': 'Volume'})
                df = df[start_date:end_date]
                
        except Exception as e:
            st.error(f"Error fetching data for {symbol}: {str(e)}")
            continue
            
        # Add price data
        price_fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['Close'],
                name=symbol,
                mode='lines',
                hovertemplate=
                '<b>Date</b>: %{x}<br>' +
                '<b>Price</b>: $%{y:.2f}<br>'
            )
        )
        
        # Add volume data
        volume_fig.add_trace(
            go.Bar(
                x=df.index,
                y=df['Volume'],
                name=symbol,
                hovertemplate=
                '<b>Date</b>: %{x}<br>' +
                '<b>Volume</b>: %{y:,.0f}<br>'
            )
        )
    
    # Update price chart layout
    price_fig.update_layout(
        title='Stock Price Movement (Last 30 Days)',
        xaxis_title='Date',
        yaxis_title='Price ($)',
        hovermode='x unified',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        template='plotly_white'
    )
    
    # Update volume chart layout
    volume_fig.update_layout(
        title='Trading Volume (Last 30 Days)',
        xaxis_title='Date',
        yaxis_title='Volume',
        hovermode='x unified',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        template='plotly_white'
    )
    
    # Display the charts
    st.plotly_chart(price_fig, use_container_width=True)
    st.plotly_chart(volume_fig, use_container_width=True)
    
    # Display key statistics table
    # Create Ticker objects once to avoid rate limiting
    tickers = {symbol: yf.Ticker(symbol) for symbol in selected_stocks}
    
    # Get data in batches
    stats_df = pd.DataFrame({
        'Symbol': selected_stocks,
        'Current Price': [tickers[symbol].history(period='1d')['Close'][0] for symbol in selected_stocks],
        '52-Week High': [tickers[symbol].info.get('fiftyTwoWeekHigh', 'N/A') for symbol in selected_stocks],
        '52-Week Low': [tickers[symbol].info.get('fiftyTwoWeekLow', 'N/A') for symbol in selected_stocks], 
        'P/E Ratio': [tickers[symbol].info.get('trailingPE', 'N/A') for symbol in selected_stocks],
    })
    
    st.subheader('Key Statistics')
    st.dataframe(stats_df.set_index('Symbol'))

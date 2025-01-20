import plotly.graph_objects as go
import plotly.express as px

def plot_line_chart(df):
    """
    Create a line chart of stock prices and returns.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Close Price'))
    fig.add_trace(go.Scatter(x=df.index, y=df['Returns'], name='Daily Returns', yaxis='y2'))
    
    fig.update_layout(
        title='Stock Price and Returns Over Time',
        xaxis_title='Date',
        yaxis_title='Price',
        yaxis2=dict(title='Returns', overlaying='y', side='right'),
        legend_title='Legend'
    )
    
    return fig

def plot_heatmap(df):
    """
    Create a correlation heatmap of the financial data.
    """
    corr_matrix = df[['Open', 'High', 'Low', 'Close', 'Volume', 'Returns']].corr()
    fig = px.imshow(corr_matrix, text_auto=True, aspect="auto")
    fig.update_layout(title='Correlation Heatmap')
    return fig

def plot_histogram(df):
    """
    Create a histogram of returns distribution.
    """
    fig = px.histogram(df, x='Returns', nbins=50)
    fig.update_layout(title='Distribution of Daily Returns')
    return fig

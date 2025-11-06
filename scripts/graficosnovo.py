# Bibliotecas
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Dados
df = pd.read_csv("../data/processed/expenses_processed.csv")
category = df['category']
amount = df['amount']

# Cores
pastel_colors = px.colors.sequential.YlOrRd_r
colors = pastel_colors * (len(category) // len(pastel_colors) + 1)

# Gráfico de Pizza
def create_pie():
    fig = go.Figure(data=go.Pie(
        labels=category,
        values=amount,
        marker=dict(colors=colors[:len(category)], line=dict(color='white', width=2)),
        hole=0.2
    ))

    fig.update_layout(
        legend_title_text="",
        legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.1,
                    font=dict(color="black")),
        margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor='rgba(255,255,255,1)',
        font=dict(color="black")
    )

    fig.update_traces(
        hoverlabel=dict(bgcolor='white', font_size=14, font_family='Arial', font_color='black'),
        opacity=0.95
    )

    fig.add_layout_image(
        dict(
            source="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Shadow.png/512px-Shadow.png",
            xref="paper", yref="paper",
            x=0, y=0, sizex=1, sizey=1,
            opacity=0.12, layer="below"
        )
    )

    return fig

# Gráfico de Barras
df['date'] = pd.to_datetime(df['date'])
df['year_month'] = df['date'].dt.to_period('M')

months_sorted = df['year_month'].sort_values().unique()
if len(months_sorted) >= 2:
    last_month = months_sorted[-2]
    current_month = months_sorted[-1]
else:
    last_month = current_month = months_sorted[-1]

df_last = df[df['year_month'] == last_month].groupby('category')['amount'].sum()
df_current = df[df['year_month'] == current_month].groupby('category')['amount'].sum()

categories_bar = sorted(set(df_last.index).union(df_current.index))
last_vals = [df_last.get(cat, 0) for cat in categories_bar]
current_vals = [df_current.get(cat, 0) for cat in categories_bar]

fig_bar = go.Figure()

fig_bar.add_trace(go.Bar(
    x=categories_bar,
    y=last_vals,
    name=f'{last_month}',
    marker=dict(
        color=[colors[category.tolist().index(cat)] for cat in categories_bar],
        line=dict(width=1, color='white')
    ),
    showlegend=True
))

fig_bar.add_trace(go.Bar(
    x=categories_bar,
    y=current_vals,
    name=f'{current_month}',
    marker=dict(
        color=[colors[category.tolist().index(cat)] for cat in categories_bar],
        line=dict(width=1, color='white')
    ),
    showlegend=True
))

fig_bar.update_layout(
    barmode='group',
    xaxis_title="Category",
    yaxis_title="Value ($)",
    xaxis=dict(tickfont=dict(color="black"), title_font=dict(color="black")),
    yaxis=dict(tickfont=dict(color="black"), title_font=dict(color="black")),
    legend_title_text="Month",
    legend=dict(font=dict(color="black")),
    paper_bgcolor='rgba(255,255,255,1)',
    margin=dict(t=20, b=20, l=40, r=20),
    font=dict(color="black")
)

# Heatmap
df['month'] = df['date'].dt.month_name()
months_order = ["January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"]

heatmap_data = (
    df.groupby(['category', 'month'])['amount']
    .sum()
    .reindex(pd.MultiIndex.from_product(
        [df['category'].unique(), months_order], names=['category', 'month']
    ), fill_value=0)
    .unstack()
)

heatmap = px.imshow(
    heatmap_data.values,
    x=months_order,
    y=heatmap_data.index,
    color_continuous_scale=px.colors.sequential.YlOrRd_r[::-1],
    labels=dict(x="Month", y="Category", color="Value ($)")
)

# Corrigindo todas as fontes para preto
heatmap.update_layout(
    paper_bgcolor='rgba(255,255,255,1)',
    margin=dict(t=20, b=20, l=60, r=20),
    font=dict(color="black")
)
heatmap.update_xaxes(title_font=dict(color="black"), tickfont=dict(color="black"))
heatmap.update_yaxes(title_font=dict(color="black"), tickfont=dict(color="black"))
heatmap.update_coloraxes(colorbar_title_font=dict(color="black"), colorbar_tickfont=dict(color="black"))

# Streamlit Layout
st.title("Expenses")
st.subheader("Pie Chart")
st.plotly_chart(create_pie(), use_container_width=True)

st.subheader("Month Comparison")
st.plotly_chart(fig_bar, use_container_width=True)

st.subheader("Expense Heatmap")
st.plotly_chart(heatmap, use_container_width=True)

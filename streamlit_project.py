import streamlit as st

st.title("Visor de disparos de la Euro 2024")
st.subheader("Usa los filtros para ver los tiros de un equipo/jugador")

import pandas as pd
import json
df = pd.read_csv("euros_2024_shot_map.csv")
df = df[df['type'] == "Shot"].reset_index(drop=True)
df['location'] = df['location'].apply(json.loads)

team = st.selectbox("Elige un equipo", df['team'].sort_values().unique(), index = None)
player = st.selectbox("Elige un jugador", df[df['team'] == team]['player'].sort_values().unique(), index = None)

def filter_data(df, team, player):
    if team:
        df = df[df['team'] == team]
    if player:
        df = df[df['player'] == player]
    return df

filtered_df = filter_data(df, team, player)

from mplsoccer import VerticalPitch

pitch = VerticalPitch(pitch_type = 'statsbomb', half = True)
fig, ax = pitch.draw(figsize=(10,10))

def plot_shots(df, ax, pitch):
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x = float(x['location'][0]),
            y = float(x['location'][1]),
            ax = ax,
            s = 1000 * x['shot_statsbomb_xg'], # mayores círculos para mayores xG
            color = 'green' if x['shot_outcome'] == 'Goal' else 'white',
            edgecolors = 'black',
            alpha = 1 if x['type'] == 'goal' else 0.5,
            zorder = 2 if x['type'] == 'goal' else 1
        )

plot_shots(filtered_df, ax, pitch)

st.pyplot(fig)
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_darkness():
  darkness = pd.read_csv("research/darkside.csv")
  fig = go.Figure()
  fig.add_trace(go.Bar(x=darkness["Forum"], y=(darkness["BadPosts"] / darkness["TotalPosts"]), name="Posty"))
  fig.add_trace(go.Bar(x=darkness["Forum"], y=10 * (darkness["BadUsers"] / darkness["TotalUsers"]), name="Użytkownicy"))
  fig.update_layout(title="Stosunek złych postów i użytkowników do wszystkich")
  return fig

def UsersPage(available_forums):
  dark_users = pd.read_csv("research/darkins.csv")

  return dbc.Container([
    dbc.Row([
      dbc.Col(width=4, children=[
        dbc.Card(color="primary", outline=True, children=[
          dbc.CardBody(style={"padding": "20px 30px"}, children=[
            html.P("Wybierz przedział czasowy:"),
            dcc.RangeSlider(id="year-range-user", min=2009, max=2021, value=[2009, 2020], marks={
              "2009": { "label": '2009', "style": { "transform": "rotate(-45deg)", "margin-left": "-20px", "user-select": "none" }},
              "2010": { "label": '', "style": { "transform": "rotate(-45deg)", "margin-left": "-20px", "user-select": "none" }},
              "2011": { "label": '', "style": { "transform": "rotate(-45deg)", "margin-left": "-20px", "user-select": "none" }},
              "2012": { "label": '2012', "style": { "transform": "rotate(-45deg)", "margin-left": "-20px", "user-select": "none" }},
              "2013": { "label": '', "style": { "transform": "rotate(-45deg)", "margin-left": "-20px", "user-select": "none" }},
              "2014": { "label": '', "style": { "transform": "rotate(-45deg)", "margin-left": "-20px", "user-select": "none" }},
              "2015": { "label": '2015', "style": { "transform": "rotate(-45deg)", "margin-left": "-20px", "user-select": "none" }},
              "2016": { "label": '', "style": { "transform": "rotate(-45deg)", "margin-left": "-20px", "user-select": "none" }},
              "2017": { "label": '', "style": { "transform": "rotate(-45deg)", "margin-left": "-20px", "user-select": "none" }},
              "2018": { "label": '2018', "style": { "transform": "rotate(-45deg)", "margin-left": "-20px", "user-select": "none" }},
              "2019": { "label": '', "style": { "transform": "rotate(-45deg)", "margin-left": "-20px", "user-select": "none" }},
              "2020": { "label": '', "style": { "transform": "rotate(-45deg)", "margin-left": "-20px", "user-select": "none" }},
              "2021": { "label": '2021', "style": { "transform": "rotate(-45deg)", "margin-left": "-20px", "user-select": "none" }},
            }),
            html.Br(),
            html.Br(),
            html.P("Wybierz forum:"),
            dcc.Dropdown(id="select-forum-users", options=available_forums, value="lifehacks")
          ])
        ])
      ]),
      dbc.Col(width=8, align="center", children=[
        dbc.Row(justify="center", children=[
          dbc.Card(className="info-card", color="primary", inverse=True, style={"margin": "15px"}, children=[
            dbc.CardHeader("Liczba użytkowników:"),
            dbc.CardBody(html.H5("...", id="num-users", style={'text-align': 'center'}))
          ]),
          dbc.Card(className="info-card", color="primary", inverse=True, style={"margin": "15px"}, children=[
            dbc.CardHeader("Aktywni użytkownicy:"),
            dbc.CardBody(html.H5("...", id="active-users", style={'text-align': 'center'}))
          ]),
          dbc.Card(className="info-card", color="primary", inverse=True, style={"margin": "15px"}, children=[
            dbc.CardHeader("Najwyższa reputacja:"),
            dbc.CardBody(html.H5("...", id="highest-reputation", style={'text-align': 'center'}))
          ])
        ])
      ]),
      dbc.Row(style={'margin': "30px 0px"}, children=[
        dbc.Col([
          html.H3("1. Jak wielu użytkowników częściej używa głosów w dół niż w górę?"),
          html.P("Okazuje się, że na portalu StackExchange.com istnieje sporo użytkowników, którzy " +
                 "częsciej używają głosów w dół niż w górę. Ich liczba nigdy nie jest duża, jednak można " +
                 "porównać ją z liczbą słabych postów (o ujemnym wyniku)."),
          html.P("Zakładając, że użytkownicy oddają głosy w dół w uzasadniony sposób, te dwie wartości powinny " +
                 "być wprost proporcjonalne do siebie. Jednak na niektórych forach stosunek ten jest zaburzony. " +
                 "Można to zobaczyć na poniższym wykresie, gdzie przedstawiono procentowy stosunek ujemnych postów " +
                 "do wszystkich oraz stosunek tzw. mrocznych użytkowników do wszystkich."),
          dcc.Graph(id="dark-users-graph", figure=plot_darkness()),
          html.H3("2. Najgorsi użytkownicy na StackExchange.com"),
          html.P("Z każdego forum wybraliśmy dziesięciu najgorszych użytkowników, to znaczy takich, którzy mieli " +
                 "największą różnicę pomiędzy głosami w dół a w górę. Kilku z nich pojawiło się w więcej niż jednym 'Top 10'."),
          html.P("Szczególnie warto tu zwrócić uwagę na użytkownika o nazwie 'Glorfindel', który posiada konta na wszystkich 176 " +
                 "sekcjach portalu, na każdym posiadając przynajmniej 300 reputacji. Pojawia się on w 16 na 18 zabadanych przez nas Top 10"),
          dbc.Row([
            dbc.Col(width={"size": 4, "offset": 4}, children=[
              dbc.Card(color="dark", inverse=True, children=[
                dbc.CardHeader("Najmroczniejszy użytkownik", style={"text-align": "center"}),
                dbc.CardBody([
                  dbc.Col([
                    html.Div(style={"display": 'flex', "flex-direction": "column", "align-items": "center", "margin": "10px 0px 30px"}, children=[
                      html.Img(src="https://i.stack.imgur.com/Haz6W.jpg?s=128&g=1", style={"width": "200px", "height": "auto"})
                    ]),
                    html.H3(dark_users.loc[0, "DisplayName"]),
                    html.P(f"Obecność w Top 10 na forach: {dark_users.loc[0, 'NumOfTerroredForums']}"),
                    html.P(f"Średnia liczba głosów w dół: {dark_users.loc[dark_users.AccountId == 6085540, 'VoteDiff'].mean().round(2)}")
                  ])
                ])
              ])
            ])
          ]),
          dbc.Row(style={'margin': '40px 0px 0px 0px'}, children=[
            dbc.Col(width=3, children=[
              dbc.Card(color="dark", inverse=True, children=[
                dbc.CardHeader("Mroczny użytkownik", style={'text-align': 'center'}),
                dbc.CardBody([
                  dbc.Col([
                    html.H5(dark_users.loc[16, "DisplayName"]),
                    html.P(f"Obecność w Top 10 na forach: {dark_users.loc[16, 'NumOfTerroredForums']}"),
                    html.P(f"Średnia liczba głosów w dół: {dark_users.loc[dark_users.AccountId == 4333085, 'VoteDiff'].mean().round(2)}")
                  ])
                ])
              ])
            ]),
            dbc.Col(width=3, children=[
              dbc.Card(color="dark", inverse=True, children=[
                dbc.CardHeader("Mroczny użytkownik", style={'text-align': 'center'}),
                dbc.CardBody([
                  dbc.Col([
                    html.H5(dark_users.loc[20, "DisplayName"]),
                    html.P(f"Obecność w Top 10 na forach: {dark_users.loc[20, 'NumOfTerroredForums']}"),
                    html.P(
                      f"Średnia liczba głosów w dół: {dark_users.loc[dark_users.AccountId == 24885, 'VoteDiff'].mean().round(2)}")
                  ])
                ])
              ])
            ]),
            dbc.Col(width=3, children=[
              dbc.Card(color="dark", inverse=True, children=[
                dbc.CardHeader("Mroczny użytkownik", style={'text-align': 'center'}),
                dbc.CardBody([
                  dbc.Col([
                    html.H5(dark_users.loc[23, "DisplayName"]),
                    html.P(f"Obecność w Top 10 na forach: {dark_users.loc[24, 'NumOfTerroredForums']}"),
                    html.P(
                      f"Średnia liczba głosów w dół: {dark_users.loc[dark_users.AccountId == 34933, 'VoteDiff'].mean().round(2)}")
                  ])
                ])
              ])
            ]),
            dbc.Col(width=3, children=[
              dbc.Card(color="dark", inverse=True, children=[
                dbc.CardHeader("Mroczny użytkownik", style={'text-align': 'center'}),
                dbc.CardBody([
                  dbc.Col([
                    html.H5(dark_users.loc[26, "DisplayName"]),
                    html.P(f"Obecność w Top 10 na forach: {dark_users.loc[26, 'NumOfTerroredForums']}"),
                    html.P(
                      f"Średnia liczba głosów w dół: {dark_users.loc[dark_users.AccountId == 300272, 'VoteDiff'].mean().round(2)}")
                  ])
                ])
              ])
            ])
          ])
        ])
      ])
    ])
  ])
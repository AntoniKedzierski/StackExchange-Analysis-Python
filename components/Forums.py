import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_table
import pandas as pd


def ForumsPage(available_forums):
  return dbc.Container([
    dbc.Row([
      dbc.Col(width=4, children=[
        dbc.Card(color="primary", outline=True, children=[
          dbc.CardBody(style={"padding": "20px 30px"}, children=[
            html.P("Wybierz przedział czasowy:"),
            dcc.RangeSlider(id="year-range-forums", min=2009, max=2021, value=[2009, 2020], marks={
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
            dcc.Dropdown(id="select-forum-forums", options=available_forums, value="lifehacks")
          ])
        ])
      ]),
      dbc.Col(width=8, align="center", children=[
        dbc.Row(justify="center", children=[
          dbc.Card(className="info-card", color="primary", inverse=True, style={"margin": "15px"}, children=[
            dbc.CardHeader("Liczba postów:"),
            dbc.CardBody(html.H5("...", id="num-posts", style={'text-align': 'center'}))
          ]),
          dbc.Card(className="info-card", color="primary", inverse=True, style={"margin": "15px"}, children=[
            dbc.CardHeader("Nowe posty tygodniowo:"),
            dbc.CardBody(html.H5("...", id="new-posts-weekly", style={'text-align': 'center'}))
          ]),
          dbc.Card(className="info-card", color="primary", inverse=True, style={"margin": "15px"}, children=[
            dbc.CardHeader("Nowi użytkownicy tygodniowo:"),
            dbc.CardBody(html.H5("...", id="new-users-weekly", style={'text-align': 'center'}))
          ])
        ])
      ]),
      dbc.Row(style={'margin': "30px 0px"}, children=[
        dbc.Col([
          html.H3("1. Jak zmienia się zainteresowanie danym forum w czasie?"),
          html.P("Wykres prezentuje zainteresowanie wybraną sekcją, które jest wyrażone poprzez zestawienie nowych pytań i odpowiedzi oraz nowych użytkowników na forum. Nagły spadek na końcu wykresu spowodowany jest niekompletnością danych z grudnia 2020."),
          dcc.Graph(id="forum-interest"),
          html.H3("2. Aktywność w ciągu tygodnia"),
          html.P("Poniżej przedstawiono, ile postów oraz komentarzy zostało napisanych w konkretne dni tygodni, z uwzględnieniem zadanego przedziału czasowego."),
          dcc.Graph(id="new-posts-and-comments"),
          html.H3("3. Godzinowa aktywność użytkowników"),
          html.P("Na histogramie poniżej można zobaczyć godzinowy rozkład aktywności użytkowników oraz podział jej na dni robocze i weekend."),
          dcc.Graph(id="daily-activity"),
          html.H3("4. Najbardziej popularne tagi na forum"),
          html.P("Na wykresie widoczny jest procentowy rozkład najbardziej popularnych ze wszystkich tagów. Liczbę tagów można zmienić w polu poniżej."),
          dcc.Slider(id="num-of-tags", min=3, max=15, value=5, marks=dict([(v, str(v)) for v in range(3, 16)])),
          html.Br(),
          html.Br(),
          dcc.Graph(id="forum-tags"),
          html.H3("5. Intrygujące pytania"),
          html.P("Zadanie jakich pytań skutkowało długą i bogatą dyskusją? Poniżej wypisane zostały topowe pytań, które pomimo bardzo którkiej treści spotkały się z dużą liczbą długich odpowiedzi. Suwakami poniżej można dostosować liczbę pytań oraz kwantyl rozkładu liczby odpowiedzi pod postami, aby uniknąć otrzymania krótkiego pytania z jedną, bardzo długą odpowiedzią."),
          dcc.Slider(id="num-of-intriguing-posts", min=5, max=20, value=10, marks=dict([(v, str(v)) for v in range(5, 21)])),
          html.Br(),
          dcc.Slider(id="p-value", min=75, max=99, value=95, marks=dict([(v, str(v) + "%") for v in range(75, 100)])),
          html.Br(),
          html.Br(),
          html.Div(id="intriguing-posts")
        ])
      ])
    ])
  ])
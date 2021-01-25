import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


def Homepage():
  return dbc.Container(
    dbc.Jumbotron(children=[
      html.H1('StackExchange Analysis', className="display-3"),
      html.P("Antoni Kędzierski, Marek Wiese", className="lead"),
      html.Hr(className="my-2"),
      html.P("Projekt wykonany w obrębie przedmiotu 'Przetwarzanie i Analiza Danych w języku Python."),
      html.P(dbc.Button("Kod źródłowy", color='primary'))
    ])
  )

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import os
import datetime
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output

from app import app

from components.Homepage import Homepage
from components.Navbar import NavBar
from components.Users import UsersPage
from components.Forums import ForumsPage
from plotter import *


app.layout = html.Div([
  dcc.Location(id='assurl', refresh=False),
  NavBar(),
  html.Div(id='page-content', style={"padding": "30px 0px"})
])



# Global stuff
globals()["forum-list"] = os.listdir('data')
globals()["current-forum"] = ""
globals()["available-forums"] = []
for forum in globals()['forum-list']:
  size = 0
  for subfile in os.listdir(f'data/{forum}/'):
    size += os.path.getsize(f'data/{forum}/{subfile}')
  globals()["available-forums"].append({
    "label": f"{forum.capitalize()} ({round(size / 1024 / 1024)} MB)",
    "value": forum
  })


# Functions
def load_forum(forum):
  if forum != globals()["current-forum"]:
    globals()["current-forum"] = forum

    globals()["Posts"] = pd.read_csv(f"data/{forum}/Posts.csv")
    globals()["Posts"]["CreationDate"] = pd.to_datetime(globals()["Posts"]["CreationDate"])
    globals()["Posts"]["LastEditDate"] = pd.to_datetime(globals()["Posts"]["LastEditDate"])
    globals()["Posts"]["LastActivityDate"] = pd.to_datetime(globals()["Posts"]["LastActivityDate"])

    globals()["Users"] = pd.read_csv(f"data/{forum}/Users.csv")
    globals()["Users"]["CreationDate"] = pd.to_datetime(globals()["Users"]["CreationDate"])
    globals()["Users"]["LastAccessDate"] = pd.to_datetime(globals()["Users"]["LastAccessDate"])

    globals()["Comments"] = pd.read_csv(f"data/{forum}/Comments.csv")
    globals()["Comments"]["CreationDate"] = pd.to_datetime(globals()["Comments"]["CreationDate"])

    globals()["Tags"] = pd.read_csv(f'data/{forum}/Tags.csv')


def extract_date(year_range):
  begin_date_ = datetime.datetime(year_range[0], 1, 1, 0, 0, 0)
  to_date_ = datetime.datetime(year_range[1], 12, 31, 23, 59, 59)
  return begin_date_, to_date_


# Callbacks
@app.callback(
  Output('page-content', 'children'),
  Input('assurl', 'pathname'))
def display_page(pathname):
  if pathname == '/':
    return Homepage()
  if pathname == "/users":
    return UsersPage(globals()["available-forums"])
  if pathname == '/forums':
    return ForumsPage(globals()["available-forums"])
  return html.Div(children=["not found..."])



@app.callback(
  Output("num-users", "children"),
  Output("active-users", "children"),
  Output("highest-reputation", "children"),
  Input("year-range-user", "value"),
  Input("select-forum-users", "value")
)
def update_users(year_range, forum):
  load_forum(forum)
  begin_date, to_date = extract_date(year_range)
  num_users = globals()["Users"].loc[globals()["Users"]["CreationDate"] <= to_date, :].shape[0]
  active_users = globals()["Users"].loc[(globals()["Users"]["LastAccessDate"] >= begin_date) & (globals()["Users"]["CreationDate"] <= to_date) & (globals()["Users"]["LastAccessDate"] <= to_date), :].shape[0]
  highest_rep = globals()["Users"]["Reputation"].max()

  return([num_users, active_users, highest_rep])



@app.callback(
  Output("num-posts", "children"),
  Output("new-posts-weekly", "children"),
  Output("new-users-weekly", "children"),
  Output("forum-interest", "figure"),
  Output("new-posts-and-comments", "figure"),
  Output("daily-activity", "figure"),
  Output("forum-tags", "figure"),
  Output("intriguing-posts", "children"),
  Input("year-range-forums", "value"),
  Input("select-forum-forums", "value"),
  Input("num-of-tags", "value"),
  Input("num-of-intriguing-posts", "value"),
  Input("p-value", "value")
)
def update_forums(year_range, forum, num_of_tags, num_int_posts, p_value):
  load_forum(forum)
  begin_date, to_date = extract_date(year_range)
  num_posts = globals()["Posts"].loc[(globals()["Posts"]["CreationDate"] >= begin_date) & (globals()["Posts"]["CreationDate"] <= to_date) & (globals()["Posts"]["PostTypeId"] == 1), :].shape[0]
  new_posts_weekly = globals()["Posts"].loc[(globals()["Posts"]["CreationDate"] >= begin_date) & (
      globals()["Posts"]["CreationDate"] <= to_date) & (globals()["Posts"]["PostTypeId"] == 1), :]\
    .groupby(pd.Grouper(key="CreationDate", freq="W-MON")).size().reset_index().mean()
  new_users_weekly = globals()["Users"].loc[(globals()["Users"]["CreationDate"] >= begin_date) & (
      globals()["Users"]["CreationDate"] <= to_date), :] \
    .groupby(pd.Grouper(key="CreationDate", freq="W-MON")).size().reset_index().mean()
  forum_interest = plot_interest(globals()["Users"], globals()["Posts"], forum, year_range)
  week_acitivity = plot_activity_weekly(globals()["Posts"], globals()["Comments"], forum, year_range)
  daily_activity = plot_activity_daily(globals()["Posts"], forum, year_range)
  top_tags_ = plot_top_tags(globals()["Tags"], forum, num_of_tags)
  intriguing = intriguing_posts(globals()["Posts"], forum, p_value / 100, num_int_posts)
  dt = dash_table.DataTable(
    style_cell={
      'whiteSpace': 'normal',
      'height': 'auto'
    },
    style_cell_conditional=[
      {'if': {'column_id': "Średnia różnica wyrazów"}, 'width': '180px'},
      {'if': {'column_id': "Liczba słów"}, 'width': '130px'},
      {'if': {'column_id': "Liczba odpowiedzi"}, 'width': '130px'},
      {'if': {'column_id': "Tytuł"}, 'width': '240px'},
      {'if': {'column_id': "Treść"}, 'width': '430px'},
    ],
    data=intriguing.to_dict("rows"),
    columns=[{"name": i, "id": i} for i in intriguing.columns])

  return([
    num_posts,
    f"~ {round(new_posts_weekly.to_list()[0])} postów",
    f"~ {round(new_users_weekly.to_list()[0])} użytkowników",
    forum_interest,
    week_acitivity,
    daily_activity,
    top_tags_,
    dt
  ])


if __name__ == '__main__':
  load_forum("lifehacks")
  if not os.path.isdir("research/outputs"):
    os.mkdir("research/outputs")
  app.run_server(debug=True, dev_tools_ui=False, dev_tools_props_check=False)


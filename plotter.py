import pandas as pd
import numpy as np
import os
import glob
import datetime
import calendar
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


def users_by_ym(Users, forum, year_range=(2000, 2021)):
  from_ = datetime.datetime(year_range[0], 1, 1)
  to = datetime.datetime(year_range[1], 12, 31)
  users = pd.DataFrame(Users["CreationDate"])
  users = users[(users.CreationDate >= from_) & (users.CreationDate <= to)]
  users["Date"] = users.CreationDate.dt.strftime('%Y-%m')
  users = pd.DataFrame(users.groupby("Date").size()).reset_index()
  users.rename(columns={0: "Count"}, inplace=True)
  users = users.sort_values("Date").reset_index(drop=True)
  users.to_csv("research/outputs/" + forum + "_users_by_ym.csv")
  return users


def posts_by_ym(Posts, forum, year_range=(2000, 2021)):
  from_ = datetime.datetime(year_range[0], 1, 1)
  to = datetime.datetime(year_range[1], 12, 31)
  posts = pd.DataFrame(Posts[["CreationDate", "PostTypeId"]])
  posts = posts[(posts.CreationDate >= from_) & (posts.CreationDate <= to) & ((posts.PostTypeId == 1) | (posts.PostTypeId == 2))]
  posts["Date"] = posts.CreationDate.dt.strftime('%Y-%m')
  posts = pd.DataFrame(posts.groupby("Date").size()).reset_index()
  posts.rename(columns={0: "Count"}, inplace=True)
  posts = posts.sort_values("Date").reset_index(drop=True)
  posts.to_csv("research/outputs/" + forum + "_posts_by_ym.csv")
  return posts


def plot_interest(Users, Posts, forum, year_range=(2000, 2021)):
  df1 = users_by_ym(Users, forum, year_range)
  df2 = posts_by_ym(Posts, forum, year_range)
  fig = make_subplots(rows=1, cols=1)
  fig.add_trace(go.Scatter(x=df1.Date, y=df1.Count, name="Nowi <br>użytkownicy", mode="lines+markers"),
                row=1, col=1)
  fig.add_trace(go.Scatter(x=df2.Date, y=df2.Count, name="Nowe pytania <br>i odpowiedzi", mode="lines+markers"),
                row=1, col=1)
  fig.update_layout(title_text="Zainteresowanie forum " + str.upper(forum),
                    showlegend=True)
  return fig



def posts_by_weekday(Posts, forum, year_range=(2000, 2021)):
  from_ = datetime.datetime(year_range[0], 1, 1)
  to = datetime.datetime(year_range[1], 12, 31)
  posts = pd.DataFrame(Posts
                       .loc[(Posts.CreationDate >= from_) & (Posts.CreationDate <= to) & ((Posts.PostTypeId == 1) | (Posts.PostTypeId == 2)), "CreationDate"]
                       .apply(lambda x: x.weekday()).value_counts()).reset_index()
  posts.rename(columns={"index": "Weekday", "CreationDate": "Count"}, inplace=True)
  posts = posts.sort_values("Weekday")
  posts["Weekday"] = posts["Weekday"].apply(lambda x: calendar.day_name[x])
  posts.reset_index(drop=True, inplace=True)
  posts.to_csv("research/outputs/" + forum + "_posts_by_weekday.csv")
  return posts



def comments_by_weekday(Comments, forum, year_range=(2000, 2021)):
  from_ = datetime.datetime(year_range[0], 1, 1)
  to = datetime.datetime(year_range[1], 12, 31)
  comments = pd.DataFrame(Comments.loc[(Comments.CreationDate >= from_) & (Comments.CreationDate <= to), "CreationDate"].apply(lambda x: x.weekday()).value_counts()).reset_index()
  comments.rename(columns={"index": "Weekday", "CreationDate": "Count"}, inplace=True)
  comments = comments.sort_values("Weekday")
  comments["Weekday"] = comments["Weekday"].apply(lambda x: calendar.day_name[x])
  comments.reset_index(drop=True, inplace=True)
  comments.to_csv("research/outputs/" + forum + "_comments_by_weekday.csv")
  return comments



def plot_activity_weekly(Posts, Comments, forum, year_range=(2000, 2021)):
  weekdays = ["pon.", "wt.", "śr.", "czw.", "pt.", "sob.", "niedz."]
  colors = 5 * ["firebrick"] + 2 * ["steelblue"]
  df1 = posts_by_weekday(Posts, forum, year_range)
  df2 = comments_by_weekday(Comments, forum, year_range)
  fig = make_subplots(rows=1, cols=2,
                      subplot_titles=("Liczba postów i odpowiedzi", "Liczba komentarzy"))
  fig.add_trace(go.Bar(x=weekdays, y=df1.Count, name="posts", marker_color=colors),
                row=1, col=1)
  fig.add_trace(go.Bar(x=weekdays, y=df2.Count, name="comments", marker_color=colors),
                row=1, col=2)
  fig.update_layout(height=600,
                    title_text="Aktywność w ciągu tygodnia na forum " + str.upper(forum),
                    showlegend=False)
  return fig



def posts_by_hour(Posts, forum, year_range):
  from_ = datetime.datetime(year_range[0], 1, 1)
  to = datetime.datetime(year_range[1], 12, 31)
  tmp = Posts.loc[(Posts.CreationDate >= from_) & (Posts.CreationDate <= to), ["CreationDate"]]
  tmp["day"] = tmp.CreationDate.apply(lambda x: calendar.day_name[x.weekday()])
  tmp["day"] = tmp.day.apply(lambda x: np.where(x in ["Saturday", "Sunday"], "weekend", "roboczy"))
  tmp["Hour"] = tmp.CreationDate.dt.hour
  tmp = tmp.groupby(["day", "Hour"]).size().reset_index()
  tmp.rename(columns={0: "Count"}, inplace=True)
  tmp.to_csv("research/outputs/" + forum + "_posts_by_hour.csv")
  return tmp


def plot_activity_daily(Posts, forum, year_range):
  hours = list(range(24))
  df = posts_by_hour(Posts, forum, year_range)
  fig = px.bar(df, x="Hour", y="Count", color="day",
               title="Liczba tworzonych postów oraz odpowiedzi w ciągu dnia na forum " + str.upper(forum),
               labels={"day": "Dzień", "Hour": "Godzina", "Count": "Liczba postów"})
  fig.update_layout(xaxis=dict(tickmode="array", tickvals=list(range(24))))
  return fig

def top_tags(Tags, forum, top=5):
  tags = Tags.sort_values("Count", ascending=False).head(top)
  tags.to_csv("research/outputs/" + forum + "_top" + str(top) + "_tags.csv")
  return tags


def plot_top_tags(Tags, forum, top=5):
  df = top_tags(Tags, forum, top)
  fig = px.pie(df, values="Count", names="TagName",
               title="Top " + str(top) + " tagów forum " + str.upper(forum),
               labels={"Count": "Liczba postów", "TagName": "Tag"})
  fig.update_traces(textposition='inside', textinfo='percent+label')
  return fig


def intriguing_posts(Posts, forum, p=0.95, top=10):
  q = Posts[Posts.PostTypeId == 1]  # pytania
  a = Posts[Posts.PostTypeId == 2]  # odpowiedzi
  qna = q.merge(a, left_on="Id", right_on="ParentId", suffixes=("_Q", "_A"))  # pytania i odpowiedzi
  qna = qna[["Id_Q", "Title_Q", "Body_Q", "Tags_Q", "AnswerCount_Q", "Body_A"]]
  qna["Words_Q"] = qna.Body_Q.str.split().dropna().apply(len)
  qna["Words_A"] = qna.Body_A.str.split().dropna().apply(len)
  qna["Words_Diff"] = qna.Words_A - qna.Words_Q
  qna = qna[qna.AnswerCount_Q >= qna.AnswerCount_Q.quantile(
    p)]  # bierzemy pod uwage tylko te pytania, dla ktorych liczba odpowiedzi przekracza kwantyl rzedu p
  qna = qna.sort_values(["Words_Q", "AnswerCount_Q"], ascending=(True, False))
  qna_by_id = qna.drop_duplicates(subset="Id_Q")[
    ["Id_Q", "Title_Q", "Body_Q", "Tags_Q", "Words_Q", "AnswerCount_Q"]].reset_index(drop=True)
  diff_mean = pd.DataFrame(qna.groupby("Id_Q").Words_Diff.agg(np.mean)).sort_values("Words_Diff",
                                                                                    ascending=False).reset_index()
  qna_by_id = qna_by_id.merge(diff_mean, on="Id_Q")
  qna_by_id.rename(columns={"Words_Diff": "Words_Diff_Mean"}, inplace=True)
  qna_by_id = qna_by_id.sort_values(["Words_Q", "Words_Diff_Mean"], ascending=(True, False))
  qna_by_id.Words_Diff_Mean = round(qna_by_id.Words_Diff_Mean, 0)
  qna_by_id.to_csv("research/outputs/" + forum + "_qna_by_id.csv")
  qna_by_id = qna_by_id[["Title_Q", "Body_Q", "Words_Q", "AnswerCount_Q", "Words_Diff_Mean"]].rename(columns={
    "Title_Q": "Tytuł",
    "Body_Q": "Treść",
    "Words_Q": "Liczba słów",
    "AnswerCount_Q": "Liczba odpowiedzi",
    "Words_Diff_Mean": "Średnia różnica wyrazów"})
  return qna_by_id.head(top)


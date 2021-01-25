import dash_bootstrap_components as dbc
import dash_html_components as html


def NavBar():
  return dbc.NavbarSimple([
    dbc.NavItem(dbc.NavLink("Dark users", href="users", external_link=True)),
    dbc.NavItem(dbc.NavLink('Forums', href="forums", external_link=True))
    ],
    brand="StackExchange Analysis",
    brand_href="/",
    brand_external_link=True,
    color="primary",
    dark=True
  )

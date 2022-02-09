
import base64
import os

from flask import Flask, send_from_directory

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


import random as rand

# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:

server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# dark mode = CYBORG
# normal mode = BOOTSTRAP


@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

app.layout = html.Div(
    [
      html.H2("noun",id="disp-word", style={'padding':'4px'},     
      		  title="When you click the button, your word will appear here"),

      html.Div([
         dbc.Button("Get new word", id='get-word', n_clicks=0, color="primary",
         				size="lg",className="mr-1",block=True),
        ],style={'width': '100%', 'display': 'block','padding':'4px'}
      ),
      html.Div([
         dbc.Button("See on SignBank", id='signbank-link', n_clicks=0, color="secondary",
                        size="lg",className="mr-1",block=True,target="_blank",
                        href="https://www.auslan.org.au/dictionary/words/noun-1.html"),
        ],style={'width': '100%', 'display': 'block','padding':'4px'}
      ),
      html.Div([        
		dcc.Dropdown( id="word-len", options=[
		        {'label': '4-letter words', 'value': '4'},
		        {'label': '5-letter words', 'value': '5'},
		        {'label': '6-letter words', 'value': '6'},
		        {'label': '7-letter words', 'value': '7'},
		        {'label': '8-letter words', 'value': '8'}
		    ],
		    value=['4', '5'],multi=True
		)          
      ], style={'width': '100%', 'display': 'block','padding':'4px'})
    ],
    style={"max-width": "360px","margin":"40px"},
)

# Show or hide the extra configuration panel (working)
@app.callback(
    [Output("disp-word", "children"),
     Output("signbank-link", "href")],
    Input("get-word", "n_clicks"), 
    State('word-len','value'),
)
def toggle_configuration_display(n_clicks,n_letters):

  filename = "data/vowel-pair.txt"

  if n_clicks == 0: 
  	raise PreventUpdate

  nl = [int(n) for n in n_letters]
  if len(nl) == 0:
    raise PreventUpdate

  nl = rand.choice(nl)
  # print('Getting a '+str(nl)+"-letter word\n")

  with open(filename,"rt") as file:   
    # assuming wordlist starts with len-4 words and we don't
    # let the user ask for a longer word than what's in the list    
    for u in range(0,nl-3): 
      header = file.readline()

    # print("header: " + header)
    header = [int(s) for s in header.split()]
    index = rand.randrange(header[1])
    file.seek(header[0] + (nl+2)*index)
    word = file.readline()


  href = "https://www.auslan.org.au/dictionary/words/{}-1.html".format(word)
    # print("word: " + word)

  return word, href


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
    # app.run_server(host="0.0.0.0", port="8050", debug=True)
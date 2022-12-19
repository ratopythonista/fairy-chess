import dash
import dash_bootstrap_components as dbc
from dotenv import load_dotenv

load_dotenv()

app = dash.Dash(
    external_stylesheets=["https://cdn.jsdelivr.net/npm/@tabler/core@1.0.0-beta16/dist/css/tabler.min.css"],
    external_scripts=["https://cdn.jsdelivr.net/npm/@tabler/core@1.0.0-beta16/dist/js/tabler.min.js"],
    use_pages=True,  
)
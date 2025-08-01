from flask import Flask, render_template_string, jsonify, request
import pathlib, json, sqlite3, subprocess, os

app = Flask(__name__)

BASE = pathlib.Path('.claude')

def list_items(folder):
    return sorted([p.stem for p in (BASE/folder).glob('*.md')])

@app.route('/')
def index():
    agents = list_items('agents')
    commands = list_items('commands')
    return render_template_string(TEMPLATE, agents=agents, commands=commands)

@app.route('/install/<kind>/<name>', methods=['POST'])
def install(kind,name):
    target = BASE/('agents' if kind=='agent' else 'commands')/f'{name}.md'
    target.write_text(request.form['content'])
    return 'OK'

@app.route('/analytics')
def analytics():
    log = pathlib.Path('.ccd_analytics.log')
    lines=[]
    if log.exists():
        lines=[json.loads(l) for l in log.read_text().splitlines()[-200:]]
    return jsonify(lines)

TEMPLATE="""<!DOCTYPE html><html><head>
<script src="https://unpkg.com/htmx.org@1.9.10"></script>
<title>CCDK UI</title></head><body>
<h1>CCDK Dashboard</h1>
<h2>Agents</h2>
<ul>
{% for a in agents %}
 <li>{{a}}</li>
{% endfor %}
</ul>
<h2>Commands</h2>
<ul>
{% for c in commands %}
 <li>{{c}}</li>
{% endfor %}
</ul>
<h2>Live Analytics (last 200)</h2>
<div hx-get="/analytics" hx-trigger="load, every 5s" hx-swap="innerHTML">
</div>
</body></html>"""

if __name__=='__main__':
    app.run(port=7000, debug=True)

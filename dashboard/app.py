from flask import Flask, render_template_string, send_from_directory
import sqlite3, json, pathlib
app = Flask(__name__, static_folder='.')

TEMPLATE="""
<!DOCTYPE html><html><head><meta charset='utf-8'><title>CCDK Dashboard</title></head>
<body>
<h1>Hive Sessions</h1>
<ul>
{% for s in sessions %}
<li>{{s[0]}} — {{s[1]}} rows</li>
{% endfor %}
</ul>
<h2>Tool Usage (last 100)</h2>
<pre>{{log}}</pre>
</body></html>
"""

@app.route('/')
def index():
    base = pathlib.Path('.ccd_hive')
    sessions=[]
    if base.exists():
        for d in base.iterdir():
            if (d/'memory.db').exists():
                c = sqlite3.connect(d/'memory.db').execute('select count(*) from memory').fetchone()[0]
                sessions.append((d.name,c))
    log=''
    if pathlib.Path('.ccd_analytics.log').exists():
        lines = pathlib.Path('.ccd_analytics.log').read_text().splitlines()[-100:]
        log='\n'.join(lines)
    return render_template_string(TEMPLATE, sessions=sessions, log=log)

if __name__=='__main__':
    app.run(port=5005,debug=True)

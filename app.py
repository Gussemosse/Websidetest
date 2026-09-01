from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)
# Db
DB_ARCHITECTS = "./db/my.db"

con = sqlite3.connect(DB_ARCHITECTS)
cur = con.cursor()
cur.execute("""
    create table if not exists architects(name, year);
""")
cur.close()
con.commit()

def get_db_architects():
    con = sqlite3.connect(DB_ARCHITECTS)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    res = cur.execute("""
        select * from architects order by start_year asc;
    """)
    architects = res.fetchall()
    cur.close()
    con.commit()
    return architects

# Routes
@app.route("/")
def hello_world():
    # Definer parameter 'name' som overføres til template
    name = request.args.get("name", "Vi elsker Nina Gandrup <333")
    return render_template("index.html", name=name, title="Simple Flask Server")

@app.route("/eiffeltårnet", methods=["GET", "POST"])
def eiffeltårnet():
    header = request.args.get("header", "Eiffeltårnet - et arkitektonisk mesterværk!")
    post_input = None
    if request.method == "POST":
        post_input = request.form.get("post_input")
    message = str(post_input)
    architects = get_db_architects()
    return render_template("eiffeltårnet.html", title="Simple Flask Server", header=header, message=message, architects=architects)

# Start Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
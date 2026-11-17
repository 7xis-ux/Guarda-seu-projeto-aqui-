from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_db, get_db

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
init_db()

@app.route("/")
def index():
    return redirect(url_for("dashboard" if "user_id" in session else "login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        if not name or not email or len(password) < 6:
            flash("Preencha os campos corretamente. A senha deve ter 6+ caracteres.")
            return redirect(url_for("register"))
        db = get_db()
        try:
            db.execute("INSERT INTO users (name,email,password) VALUES (?,?,?)",
                       (name, email, generate_password_hash(password)))
            db.commit()
            flash("Conta criada! Faça login.")
            return redirect(url_for("login"))
        except Exception:
            flash("Este e-mail já está cadastrado.")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        user = get_db().execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            return redirect(url_for("dashboard"))
        flash("E-mail ou senha incorretos.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db()
    projects = db.execute("SELECT * FROM projects WHERE user_id=? ORDER BY id DESC",
                          (session["user_id"],)).fetchall()
    return render_template("dashboard.html", projects=projects)

@app.route("/projects/new", methods=["POST"])
def new_project():
    if "user_id" not in session:
        return redirect(url_for("login"))
    name = request.form["name"].strip()
    description = request.form["description"].strip()
    if name:
        db = get_db()
        db.execute("INSERT INTO projects (user_id,name,description) VALUES (?,?,?)",
                   (session["user_id"], name, description))
        db.commit()
    return redirect(url_for("dashboard"))

@app.route("/projects/delete/<int:project_id>", methods=["POST"])
def delete_project(project_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db()
    db.execute("DELETE FROM projects WHERE id=? AND user_id=?",
               (project_id, session["user_id"]))
    db.commit()
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)

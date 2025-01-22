import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# טוען את משתני הסביבה מקובץ .env
load_dotenv()

app = Flask(__name__)
app.secret_key = "your_secret_key"

# הגדרות בסיס נתונים
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///support.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# משתני סביבה
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO_URL = os.getenv("GITHUB_REPO_URL")
WORKFLOW_ID = "Get_support_token.yml"

# מודלים
class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)

class FreeText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # כותרת
    description = db.Column(db.Text, nullable=False)  # תיאור
    content = db.Column(db.Text, nullable=False)  # תוכן

# יצירת הדאטהבייס
with app.app_context():
    db.create_all()

# נתיבים
@app.route("/")
def home():
    texts = FreeText.query.all()
    links = Link.query.all()
    return render_template("index.html", links=links, texts=texts)

@app.route("/add", methods=["GET", "POST"])
def add_link():
    if request.method == "POST":
        name = request.form.get("name")
        url = request.form.get("url")
        if name and url:
            new_link = Link(name=name, url=url)
            db.session.add(new_link)
            db.session.commit()
            flash("Link added successfully!", "success")
            return redirect(url_for("home"))
        else:
            flash("Please provide both name and URL!", "danger")
    return render_template("add_link.html")

@app.route("/run_workflow", methods=["GET", "POST"])
def run_workflow():
    if request.method == "POST":
        environment = request.form.get("environment")
        customer_id = request.form.get("customer_id")
        customer_password = request.form.get("customer_password")
        support_email = request.form.get("support_email")

        url = f"https://api.github.com/repos/{GITHUB_REPO_URL}/actions/workflows/{WORKFLOW_ID}/dispatches"
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "ref": "main",
            "inputs": {
                "environment": environment,
                "customer_id": customer_id,
                "customer_password": customer_password,
                "support_email": support_email,
            }
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 204:
            flash("Workflow triggered successfully!", "success")
        else:
            flash(f"Failed to trigger workflow: {response.text}", "danger")

        return redirect("/run_workflow")

    return render_template("run_workflow.html")

@app.route("/add_text", methods=["GET", "POST"])
def add_text():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        content = request.form.get("content")
        if title and description and content:
            new_text = FreeText(title=title, description=description, content=content)
            db.session.add(new_text)
            db.session.commit()
            flash("Text added successfully!", "success")
            return redirect(url_for("home"))
        else:
            flash("Please fill out all fields!", "danger")
    return render_template("add_text.html")

@app.route("/edit_text/<int:text_id>", methods=["GET", "POST"])
def edit_text(text_id):
    text = FreeText.query.get_or_404(text_id)
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        content = request.form.get("content")
        if title and description and content:
            text.title = title
            text.description = description
            text.content = content
            db.session.commit()
            flash("Text updated successfully!", "success")
            return redirect(url_for("home"))
        else:
            flash("Please fill out all fields!", "danger")
    return render_template("edit_text.html", text=text)

@app.route("/view_texts")
def view_texts():
    texts = FreeText.query.all()
    return render_template("view_texts.html", texts=texts)
##conection test 2
if __name__ == "__main__":
    app.run(debug=True)

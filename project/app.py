from flask import Flask, render_template, request, redirect
from models import db, User, Task, Category
from forms import TaskForm, EditTaskForm
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task_manager.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "supersecretkey123"

db.init_app(app)

# Создание БД при первом запуске
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)


@app.route("/tasks")
def tasks_page():
    tasks = Task.query.all()
    return render_template("tasks.html", tasks=tasks)


@app.route("/add", methods=["GET", "POST"])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data

        # временно: user_id = 1
        user = User.query.first()
        if not user:
            user = User(username="Guest", email="guest@example.com")
            db.session.add(user)
            db.session.commit()

        task = Task(title=title, description=description, user_id=user.id)
        db.session.add(task)
        db.session.commit()

        return redirect("/tasks")

    return render_template("add_task.html")


@app.route("/done/<int:id>")
def mark_done(id):
    task = Task.query.get(id)
    task.is_done = True
    db.session.commit()
    return redirect("/tasks")

@app.route("/undone/<int:id>")
def mark_undone(id):
    task = Task.query.get(id)
    task.is_done = False
    db.session.commit()
    return redirect("/tasks")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_task(id):
    task = Task.query.get_or_404(id)
    form = EditTaskForm(obj=task)

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        db.session.commit()
        return redirect("/tasks")

    return render_template("task_edit.html", form=form)

@app.route("/delete/<int:id>")
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect("/tasks")


if __name__ == "__main__":
    app.run(debug=True)
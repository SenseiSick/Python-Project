from flask import Flask, render_template_string, request, redirect

# from flask_sqlalchemy import SQLAlchemy  # Commented out for basic version

app = Flask(__name__)

# Database configuration (commented out)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# Database model (commented out)
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     tasks = db.relationship('Task', backref='user', lazy=True)

# class Task(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     timing = db.Column(db.String(50))
#     date = db.Column(db.String(50))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# In-memory storage for basic version
tasks = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>To-Do List</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #F5F5DC; /* Cream background */
            color: #5D4037; /* Dark brown text */
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: #EFEBE9; /* Light brown */
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #4E342E; /* Darker brown */
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input, select {
            width: 100%;
            padding: 10px;
            border: 1px solid #BCAAA4; /* Light brown border */
            border-radius: 4px;
            background-color: #FFF8E1; /* Light cream */
            box-sizing: border-box;
        }
        button {
            background-color: #6D4C41; /* Medium brown */
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #4E342E; /* Darker brown */
        }
        .task-list {
            margin-top: 30px;
        }
        .task {
            background-color: #FFF8E1; /* Light cream */
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 4px;
            border-left: 5px solid #6D4C41; /* Medium brown accent */
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .task-info {
            flex-grow: 1;
        }
        .task-actions button {
            margin-left: 10px;
            padding: 5px 10px;
            font-size: 14px;
        }
        .delete-btn {
            background-color: #8D6E63; /* Lighter brown */
        }
        .delete-btn:hover {
            background-color: #5D4037; /* Dark brown */
        }
        .empty-message {
            text-align: center;
            color: #8D6E63; /* Lighter brown */
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>To-Do List</h1>

        <form method="POST" action="/add">
            <div class="form-group">
                <label for="task">Task Description</label>
                <input type="text" id="task" name="task" required>
            </div>

            <div class="form-group">
                <label for="timing">Time</label>
                <input type="time" id="timing" name="timing">
            </div>

            <div class="form-group">
                <label for="date">Date</label>
                <input type="date" id="date" name="date">
            </div>

            <!-- Commented out user field for basic version -->
            <!-- <div class="form-group">
                <label for="user">Your Name</label>
                <input type="text" id="user" name="user">
            </div> -->

            <button type="submit">Add Task</button>
        </form>

        <div class="task-list">
            {% if tasks %}
                {% for task in tasks %}
                    <div class="task">
                        <div class="task-info">
                            <strong>{{ task.task }}</strong>
                            {% if task.timing or task.date %}
                                <div>
                                    {% if task.timing %}<span>Time: {{ task.timing }}</span>{% endif %}
                                    {% if task.date %}<span>Date: {{ task.date }}</span>{% endif %}
                                </div>
                            {% endif %}
                        </div>
                        <div class="task-actions">
                            <form method="POST" action="/delete/{{ loop.index0 }}" style="display: inline;">
                                <button type="submit" class="delete-btn">Delete</button>
                            </form>
                        </div>
                    </div>
                {% endfor %}
            {% else %}
                <p class="empty-message">No tasks yet. Add one above!</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    timing = request.form.get('timing')
    date = request.form.get('date')

    if task:
        tasks.append({
            'task': task,
            'timing': timing,
            'date': date
        })

        # Database version (commented out)
        # user_name = request.form.get('user')
        # if user_name:
        #     user = User.query.filter_by(name=user_name).first()
        #     if not user:
        #         user = User(name=user_name)
        #         db.session.add(user)
        #         db.session.commit()
        #     
        #     new_task = Task(content=task, timing=timing, date=date, user=user)
        #     db.session.add(new_task)
        #     db.session.commit()

    return redirect('/')


@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)

        # Database version (commented out)
        # task = Task.query.get_or_404(task_id)
        # db.session.delete(task)
        # db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    # Uncomment these lines for database version
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)

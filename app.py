import os
import sqlite3
from datetime import datetime, timezone
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-change-me')
app.config['DATABASE'] = os.getenv('DATABASE_PATH', '/data/tasks.db')

def get_db():
    path = app.config['DATABASE']
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, subject TEXT DEFAULT '',
        deadline TEXT NOT NULL, estimated_hours REAL NOT NULL, difficulty INTEGER NOT NULL,
        progress INTEGER NOT NULL, completed INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL)""")

def calculate_boss(task, now=None):
    now = now or datetime.now(timezone.utc).astimezone()
    deadline = datetime.fromisoformat(task['deadline'])
    if deadline.tzinfo is None: deadline = deadline.replace(tzinfo=now.tzinfo)
    remaining = (deadline-now).total_seconds()/3600
    unfinished = float(task['estimated_hours'])*(1-int(task['progress'])/100)
    if remaining <= 0: urgency = 100
    else:
        urgency = min(100, unfinished/max(remaining,.5)*145)
        urgency += 24 if remaining < 24 else (12 if remaining < 72 else 0)
    score = round(min(100, urgency*.58+int(task['difficulty'])*8+(100-int(task['progress']))*.18))
    task_data = dict(task)
    completed = int(task_data.get('completed', 0))
    if completed: score,rank,icon = 0,'討伐済み','🏆'
    elif score>=80: rank,icon='ラスボス級','🐉'
    elif score>=60: rank,icon='魔王級','👿'
    elif score>=40: rank,icon='中ボス級','👹'
    elif score>=20: rank,icon='強敵級','🦾'
    else: rank,icon='スライム級','🟢'
    if remaining<=0: advice='締切を過ぎています。提出可能か確認し、最小構成をすぐ仕上げましょう。'
    elif unfinished<=0: advice='ほぼ完成です。提出形式とファイル名を確認しましょう。'
    elif score>=80: advice='最優先クエストです。今すぐ25分だけ着手し、提出可能な最小版を作りましょう。'
    elif score>=60: advice='今日中に作業枠を確保し、難しい部分から先に片付けましょう。'
    elif score>=40: advice='作業を小分けにして、最初の1ステップを今日終わらせましょう。'
    else: advice='まだ余裕があります。少し進めて未来の自分を助けましょう。'
    return {**dict(task),'score':score,'rank':rank,'icon':icon,'remaining_hours':round(remaining,1),'unfinished_hours':round(max(0,unfinished),1),'advice':advice}

@app.route('/')
def index():
    init_db()
    with get_db() as conn: rows=conn.execute('SELECT * FROM tasks').fetchall()
    tasks=[calculate_boss(x) for x in rows]
    tasks.sort(key=lambda x:(x['completed'],-x['score'],x['deadline']))
    return render_template('index.html',tasks=tasks)

@app.post('/tasks')
def add_task():
    try:
        name=request.form['name'].strip(); deadline=request.form['deadline']
        hours=float(request.form['estimated_hours']); difficulty=int(request.form['difficulty']); progress=int(request.form['progress'])
        subject=request.form.get('subject','').strip()
        if not name or not deadline or hours<=0 or not 1<=difficulty<=5 or not 0<=progress<=100: raise ValueError('入力値を確認してください。')
        datetime.fromisoformat(deadline)
    except (ValueError,KeyError) as e:
        flash(f'登録できませんでした: {e}','error'); return redirect(url_for('index'))
    with get_db() as conn:
        conn.execute('INSERT INTO tasks(name,subject,deadline,estimated_hours,difficulty,progress,created_at) VALUES(?,?,?,?,?,?,?)',(name,subject,deadline,hours,difficulty,progress,datetime.now().isoformat(timespec='seconds')))
    flash('新しいボスが出現しました！','success'); return redirect(url_for('index'))

@app.post('/tasks/<int:task_id>/complete')
def complete(task_id):
    with get_db() as conn: conn.execute('UPDATE tasks SET completed=1,progress=100 WHERE id=?',(task_id,))
    flash('課題を討伐しました！','success'); return redirect(url_for('index'))

@app.post('/tasks/<int:task_id>/delete')
def delete(task_id):
    with get_db() as conn: conn.execute('DELETE FROM tasks WHERE id=?',(task_id,))
    flash('課題を削除しました。','success'); return redirect(url_for('index'))

@app.get('/health')
def health(): return {'status':'ok'},200

if __name__=='__main__':
    init_db(); app.run(host='0.0.0.0',port=5000,debug=os.getenv('FLASK_DEBUG')=='1')

from datetime import datetime,timedelta,timezone
from app import app,calculate_boss
def test_health(tmp_path):
 app.config.update(TESTING=True,DATABASE=str(tmp_path/'test.db')); response=app.test_client().get('/health'); assert response.status_code==200
def test_score():
 now=datetime.now(timezone.utc); task={'name':'test','deadline':(now+timedelta(hours=12)).isoformat(),'estimated_hours':10,'difficulty':5,'progress':0,'completed':0}; result=calculate_boss(task,now); assert 0<=result['score']<=100


def test_add_task_and_render_result(tmp_path):
 app.config.update(TESTING=True,DATABASE=str(tmp_path/'add-test.db'),SECRET_KEY='test')
 client=app.test_client()
 response=client.post('/tasks',data={'name':'期末課題','subject':'演習','deadline':'2026-07-30T18:00','estimated_hours':'5','difficulty':'4','progress':'20'},follow_redirects=True)
 assert response.status_code==200
 assert '期末課題'.encode() in response.data
 assert '危険度'.encode() in response.data

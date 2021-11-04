from flask import url_for
from flask_testing import TestCase
from app import app, db, Employee

class TestBase(TestCase):
    def create_app(self):
        app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///test.db",
            SECRET_KEY='TEST_SECRET_KEY',
            DEBUG=True,
            WTF_CSRF_ENABLED=False
        )
        return app
    
    def setUp(self):
        db.create_all()
        sample = Employee(name='John Smith', dept='IT', subject='Python', salary=20000, marks=300)
        db.session.add(sample)
        db.session.commit()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
class TestViews(TestBase):
    def test_emps_get(self):
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Smith', response.data)
    
    def test_add_emp(self):
        response = self.client.post(
            url_for('saveRecord'),
            data = dict(na='Jane Smith', dept='HR', subject='php', sal=20000, marks=320),
            follow_redirects = True
        )
        self.assertIn(b'Jane Smith', response.data)


    def test_pers_get(self):
        response = self.client.get(url_for('personalInformation', empno=1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Smith', response.data)

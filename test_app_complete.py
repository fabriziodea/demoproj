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
    
    def test_update_emp(self):
        response = self.client.post(
            url_for('saveEditedRecord'),
            data = dict(empno=1, na='Bob Smith', dept='IT', subject='php', sal=18000, marks=305),
            follow_redirects = True
        )
        self.assertIn(b'Bob Smith', response.data)
    
    def test_del_emp(self):
        response = self.client.get(url_for('deleteEmployee', empno=1), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Employee Information System', response.data)
    
    def test_emp_info(self):
        response = self.client.get(url_for('personalInformation', empno=1))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Smith', response.data)
    
    def test_view_edit(self):
        response = self.client.get(url_for('editRecordForm', empno=1))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Name', response.data)
    
    def test_view_add(self):
        response = self.client.get(url_for('addNewRecord'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Name', response.data)
    
    def test_filter_recs(self):
        response = self.client.post(url_for('filterrecords'),
        data = dict(dept='IT'))
        self.assertIn(b'John Smith', response.data)
    
    def test_filter_recs_all(self):
        response = self.client.post(url_for('filterrecords'),
        data = dict(dept='all'),
        follow_redirects = True)
        self.assertIn(b'John Smith', response.data)
from main import *
from firebase import Firebase
config = {
    'apiKey': "AIzaSyDNVLnasV6bMcsshlCj3JuPricE1-mOdpU",
    'authDomain': "tests-22635.firebaseapp.com",
    'databaseURL': "https://tests-22635.firebaseio.com",
    'projectId': "tests-22635",
    'storageBucket': "tests-22635.appspot.com",
    'messagingSenderId': "1018832039796",
    'username': 'abc@gmail.com',
    'password': '123456',
}
Firebase.config=config
ref=Firebase()

def test_create_delete_project():
    create_project(ref, 'New Project')
    data = ref.get('projects/0')
    test1 = data != None
    test2 = data['name'] == 'New Project'
    test3 = data['status'] == 'active'
    delete_project(ref,'0')
    data = ref.get('projects')
    test4 = data == None
    assert test1
    assert test2
    assert test3
    assert test4

def test_project_status_set():
    create_project(ref, 'New Project')
    project_status_set(ref, 0, 'archived')
    data = ref.get('projects/0')
    test1 = data['status'] == 'archived'
    project_status_set(ref, 0, 'aaa')
    data = ref.get('projects/0')
    test2 = data['status'] == 'archived'
    project_status_set(ref, 0, 'projected')
    data = ref.get('projects/0')
    test3 = data['status'] == 'projected'
    delete_project(ref, '0')
    assert test1
    assert test2
    assert test3

def test_create_delete_citation():
    create_project(ref, 'New Project')
    create_citation(ref, 0)
    data = ref.get('citations/0/projects')
    test1 = data['0'] == 'active'
    citation_remove_project(ref, 0, 0)
    data = ref.get('citations')
    test2 = data == None
    create_citation(ref, 0)
    delete_project(ref, 0)
    data = ref.get('citations')
    test3 = data == None
    assert test1
    assert test2
    assert test3


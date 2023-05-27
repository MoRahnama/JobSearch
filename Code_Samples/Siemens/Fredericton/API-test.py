
import requests

# Make a GET request
response = requests.get('https://my-json-server.typicode.com/MoRahnama/JSONAPI/users')
assert response.status_code == 200, "Status code is not 200"
assert len(response.json()) == 10, "Number of users is not 10"

for user in response.json():
    assert all(key in user for key in ["id", "name", "username", "email", "address", "phone", "website", "company"]), "All keys are not present in user"

# Make a PUT request
user_update = {"name": "Updated name", "username": "Updated username", "email": "Updated email", "address": "Updated address", "phone": "Updated phone", "website": "Updated website", "company": "Updated company"}
response = requests.put('https://my-json-server.typicode.com/MoRahnama/JSONAPI/users/1', json=user_update)
assert response.status_code == 200, "Status code is not 200"

updated_user = response.json()
assert updated_user["name"] == user_update["name"]
assert updated_user["username"] == user_update["username"]
# Add more checks here for the other fields

# Make a POST request
new_user = {"name": "New User", "username": "newuser", "email": "newuser@example.com", "address": "New Address", "phone": "123-456-7890", "website": "www.example.com", "company": "New Company"}
response = requests.post('https://my-json-server.typicode.com/MoRahnama/JSONAPI/users', json=new_user)
assert response.status_code == 201, "Status code is not 201"

created_user = response.json()
assert created_user["name"] == new_user["name"]
assert created_user["username"] == new_user["username"]
# Add more checks here for the other fields

# Make a DELETE request
response = requests.delete('https://my-json-server.typicode.com/MoRahnama/JSONAPI/users/1')
assert response.status_code == 200, "Status code is not 200"

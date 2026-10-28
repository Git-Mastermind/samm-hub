import requests

url = "http://127.0.0.1:5000"
name = input("name: ")
email = input("email: ")
role = input("role: ")
community_id = 1

response = requests.get(f"http://127.0.0.1:5000/login?name={name}&email={email}&role={role}&community_id={community_id}")
if response == 201:
    print("✅ Success!")
else:
    print(f"❌ Something went wrong! {response}")


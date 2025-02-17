import requests
import json


evidence_service_instance_id = "3b28c0fa-cbdd-4934-adb2-4874cbdb3629"
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjhkMjUwZDIyYTkzODVmYzQ4NDJhYTU2YWJhZjUzZmU5NDcxNmVjNTQiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoic3VwcG9ydCBzdXBwb3J0IiwiY3VzdG9tZXJfaWQiOiJDXzZGMkY5MkJGNTFBMDQ0QUY5QTA1RERDQzhCQUJBQ0NEIiwicm9sZSI6ImFuZWNkb3RlczphZG1pbiIsImF1ZGl0X2ZyYW1ld29ya3MiOltdLCJmaXJzdF9uYW1lIjoic3VwcG9ydCIsImxhc3RfbmFtZSI6InN1cHBvcnQiLCJzc29fbGlua2VkIjpmYWxzZSwiZmlyc3RfbG9naW4iOjE2NzUxODgwMDczNDIsIm51bV9zaWduaW5zIjoyMzc0LCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vYW5lY2RvdGVzLXByb2R1Y3Rpb24iLCJhdWQiOiJhbmVjZG90ZXMtcHJvZHVjdGlvbiIsImF1dGhfdGltZSI6MTczOTQzNjIwMiwidXNlcl9pZCI6Ilh0bHM2eFhpMVNlclVFdzk2Umc4VjYzNjBqVDIiLCJzdWIiOiJYdGxzNnhYaTFTZXJVRXc5NlJnOFY2MzYwalQyIiwiaWF0IjoxNzM5NDM2MjAyLCJleHAiOjE3Mzk0Mzk4MDIsImVtYWlsIjoiY182ZjJmOTJiZjUxYTA0NGFmOWEwNWRkY2M4YmFiYWNjZF9zdXBwb3J0QGFuZWNkb3Rlcy5haSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbImNfNmYyZjkyYmY1MWEwNDRhZjlhMDVkZGNjOGJhYmFjY2Rfc3VwcG9ydEBhbmVjZG90ZXMuYWkiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCIsInRlbmFudCI6Im1lbGlvLUMtNkYyRjkyQkY1MUEwLTZ2ejc3In19.qgX0fdeCplj7p5wbY3x11J_qV2J6rnq6G2iceqMtM0JdQnvroTKMqc3QBCvIwb-UAsXp0p5SWwpLYzarlexz7YXr_RjZsgMP1Ey7EGAYX1ykGcduibfhDMXwxrhsJH-Ib1YS3mvck60j0HRBYa0zZwEQh0mA4uE2ie-K5ehuiH9noEMt6br9IovGdoH1MUDx_0qruXMHVS0x2JY5-pfkUwXEb4vp5phIxAScQGkMYjih3P_Z0OnL_EqQbJZn_kMCq-xfBGz0wPcV_BWpYIRxxFQWMYoxk69Kan951fgSziaGjlrL8xElJ7UCK2jP_SJhnHcmlzZpRM_EcpewsTzbMA"


url_metadata = f"https://gateway.anecdotes.ai/plugins-api/v1/service/metadata/github?service_instance_id={evidence_service_instance_id}"

headers = {
    "accept": "application/json, text/plain, */*",
    "authorization": f"Bearer {token}",
}


print("Sending request to fetch repository metadata...")
response = requests.get(url_metadata, headers=headers)
print("Response status code:", response.status_code)

if response.status_code == 200:
    data = response.json()
    print("Response JSON:", json.dumps(data, indent=2))


    repositories = [repo[list(repo.keys())[0]]["name"] for repo in data.get("repositories", [])]

    print("Extracted Repositories:", repositories)
else:
    print("Failed to fetch repository metadata:", response.status_code, response.text)
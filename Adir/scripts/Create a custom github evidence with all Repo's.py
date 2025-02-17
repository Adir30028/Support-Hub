import requests
import json

evidence_service_id = "Please insert the service id"
evidence_service_instance_id = "Please insert the service instance id"
token = "Please enter the JWT token"
start_date = "yyyy-MM-DD 00:00:00.000"
#the date should be in the following format  (example for April 4th 2024):
#2024-04-01 00:00:00.000
end_date = "yyyy-MM-dd 00:00:00.000"


url_metadata = f"https://gateway.anecdotes.ai/plugins-api/v1/service/metadata/github?service_instance_id={evidence_service_instance_id}"
url_evidence = "https://gateway.anecdotes.ai/evidence/v1/evidence"

headers = {
    "accept": "application/json, text/plain, */*",
    "authorization": f"Bearer {token}",
}


print("Sending request to fetch repository metadata...")
response = requests.get(url_metadata, headers=headers)
print("Response status code:", response.status_code)
print("Response content:", response.text)

if response.status_code == 200:
    data = response.json()
    print("Response JSON:", json.dumps(data, indent=2))


    repositories = [repo[list(repo.keys())[0]]["name"] for repo in data.get("repositories", [])]

    print("Extracted Repositories:", repositories)


    data_evidence = {
        "evidence_service_id": evidence_service_id,
        "evidence_service_instance_id": evidence_service_instance_id,
        "evidence_tickets": json.dumps(
            ["repos", ",".join(repositories), "", start_date, end_date])
    }

    print("Sending evidence request with data:", data_evidence)


    response_evidence = requests.post(url_evidence, headers=headers, data=data_evidence)
    print("Evidence request status code:", response_evidence.status_code)
    print("Evidence response content:", response_evidence.text)

    if response_evidence.status_code in [200, 201]:
        print("Evidence request successful:", response_evidence.json())
    else:
        print("Failed to send evidence request:", response_evidence.status_code, response_evidence.text)

else:
    print("Failed to fetch repository metadata:", response.status_code, response.text)

import csv
import http.client
import json

# SET UP
# CircleCI API Token https://app.circleci.com/settings/user/tokens
CIRCLECI_API_TOKEN = 'API-TOKEN-HERE'
# Output folder for csv files
OUTPUT_DIR = '/tmp'
# GitHub organization name for output
GITHUB_ORG = 'org-name'


conn = http.client.HTTPSConnection('circleci.com')
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Circle-Token': CIRCLECI_API_TOKEN
}

# Create project name list
# ref: No api documentation
project_names = []
for i in range(1, 100):
    conn.request(
        'GET', f'/api/v1.1/user/repos/github?page={i}&per-page=100', headers=headers)
    res = conn.getresponse()
    res_data = json.loads(res.read().decode('utf-8'))
    names = [repo['name']
             for repo in res_data if repo['username'] == GITHUB_ORG]
    if not len(names):
        break
    project_names += names

max = len(project_names)

# Export: Project environment variables
# ref: https://circleci.com/docs/api/v2/index.html#operation/listEnvVars
with open(f'{OUTPUT_DIR}/project_envvars.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['project_name', 'name', 'value'])
    for i, prj in enumerate(project_names, 1):
        print(f'[{f.name}] {i}/{max}: {prj}')
        conn.request(
            'GET', f'/api/v2/project/github/{GITHUB_ORG}/{prj}/envvar', headers=headers)
        res = conn.getresponse()
        body = json.loads(res.read().decode('utf-8'))
        if res.status != 200:
            print(f'Status code: {res.status}, {body}')
            continue
        rows = [[prj, item['name'], item['value']] for item in body['items']]
        writer.writerows(rows)

# Export: Project Checkout SSH keys
# ref: https://circleci.com/docs/api/v2/index.html#operation/listCheckoutKeys
with open(f'{OUTPUT_DIR}/project_checkout-ssh-keys.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['project_name', 'type', 'preferred',
                    'created_at', 'public_key', 'fingerprint'])
    for i, prj in enumerate(project_names, 1):
        print(f'[{f.name}] {i}/{max}: {prj}')
        conn.request(
            'GET', f'/api/v2/project/github/{GITHUB_ORG}/{prj}/checkout-key', headers=headers)
        res = conn.getresponse()
        body = json.loads(res.read().decode('utf-8'))
        if res.status != 200:
            print(f'Status code: {res.status}, {body}')
            continue
        rows = [[prj, item['type'], item['preferred'], item['created_at'],
                 item['public_key'], item['fingerprint']] for item in body['items']]
        writer.writerows(rows)

# Export: Project Additional SSH keys
# ref: No api documentation
with open(f'{OUTPUT_DIR}/project_additional-ssh-keys.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['project_name', 'hostname', 'public_key', 'fingerprint'])
    for i, prj in enumerate(project_names, 1):
        print(f'[{f.name}] {i}/{max}: {prj}')
        conn.request(
            'GET', f'/api/v1.1/project/github/{GITHUB_ORG}/{prj}/settings', headers=headers)
        res = conn.getresponse()
        body = json.loads(res.read().decode('utf-8'))
        if res.status != 200:
            print(f'Status code: {res.status}, {body}')
            continue
        rows = [[prj, item['hostname'], item['public_key'],
                 item['fingerprint']] for item in body['ssh_keys']]
        writer.writerows(rows)

# Export: Project API tokens
# ref: No api documentation
with open(f'{OUTPUT_DIR}/project_api-tokens.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['project_name', 'label', 'scope', 'time', 'id'])
    for i, prj in enumerate(project_names, 1):
        print(f'[{f.name}] {i}/{max}: {prj}')
        conn.request(
            'GET', f'/api/v1.1/project/github/{GITHUB_ORG}/{prj}/token', headers=headers)
        res = conn.getresponse()
        body = json.loads(res.read().decode('utf-8'))
        if res.status != 200:
            print(f'Status code: {res.status}, {body}')
            continue
        rows = [[prj, item['label'], item['scope'], item['time'], item['id']]
                for item in body]
        writer.writerows(rows)

# Create context list
# ref: https://circleci.com/docs/api/v2/index.html#operation/listContexts
conn.request('GET', f'/api/v2/context?owner-slug=github/{GITHUB_ORG}', headers=headers)
res = conn.getresponse()
body = json.loads(res.read().decode('utf-8'))
context_ids = {c['name']: c['id'] for c in body['items']}

# Export: Context variables
# ref: https://circleci.com/docs/api/v2/index.html#operation/listEnvironmentVariablesFromContext
with open(f'{OUTPUT_DIR}/context_envvars.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['context_name', 'variable', 'created_at'])
    for name, id in context_ids.items():
        conn.request("GET", f"/api/v2/context/{id}/environment-variable", headers=headers)
        res = conn.getresponse()
        body = json.loads(res.read().decode('utf-8'))
        rows = [[name, item['variable'], item['created_at']] for item in body['items']]
        writer.writerows(rows)

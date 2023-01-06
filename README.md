# circleci-secrets-exporter

Export CircleCI secrets in CSV format.  
CircleCIのシークレットをCSV形式で出力するスクリプトです。

## How to use
1. Open main.py and overwrite the correct constants.
```python
# CircleCI API Token https://app.circleci.com/settings/user/tokens
CIRCLECI_API_TOKEN = 'API-TOKEN-HERE'
# Output folder for csv files
OUTPUT_DIR = '/tmp'
# GitHub organization name for output
GITHUB_ORG = 'org-name'
```

2. Run scripts
```sh
python ./main.py
```
3. See output csv files  
Output destination is OUTPUT_DIR.  
Some csv files are created (i.e. project_envvars.csv)

## Supported secrets
- Project environment variables
- Project Checkout SSH keys
- Project Additional SSH keys
- Project API tokens
- Context variables

## TODO or Not supported
- API Pagination (= next_page_token)

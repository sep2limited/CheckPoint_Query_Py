from cpapi import APIClient, APIClientArgs
import argparse
import os
import json


def buildQuery(ipfile):
    iplist = []
    with open (ipfile) as f:
        
        for ip in f.readlines():
            ip = ip.strip()
            iplist.append(ip)
    query = " OR ".join([f"{ip}" for ip in iplist])
    # print(query)
    return query

def search_logs(API_SERVER, USERNAME, PASSWORD, QUERY_STRING):
    client_args = APIClientArgs(server=API_SERVER)

    with APIClient(client_args) as client:
        login_res = client.login(USERNAME, PASSWORD)

        if login_res.success is False:
            print("Login failed:\n", login_res.error_message)
            exit(1)

        log_query = {
            "new-query": {
                "time-frame": "last-30-days",
                "max-logs-per-request": "100",
                "filter": f"{QUERY_STRING}"
            }
        }
        print("running log query, this might take a while (I'm not async yet!)")
        log_query_results = client.api_call("show-logs", payload=log_query)
        # APIResponse
        if log_query_results.success is False:
            print("Failed to query logs:\n", log_query_results.error_message)
            exit(1)
        return log_query_results
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search Checkpoint Logs for IPs in provided file')
    parser.add_argument('--file', help='File containing IPs to search for')
    parser.add_argument('--server', help='Checkpoint Management Server IP', default='localhost')
    parser.add_argument('--user', help='API User', default='admin')
    parser.add_argument('--password', help='API User Password', default='password')
    parser.add_argument('--query', help='API User Password')
    args = parser.parse_args()


    if args.file:
            if not os.path.exists(args.file):
                print('File does not exist')
                exit()
            query = buildQuery(args.file)
    elif args.query:
            query = args.query
    else:
        print('No query or string file provided')
    
    
    log_res = search_logs(API_SERVER=args.server, USERNAME=args.user,PASSWORD=args.password, QUERY_STRING=query)
    logs = log_res.data['logs']
    if log_res.data['logs-count'] > 0:
        print('found matches')
        with open('logs.json', 'w', newline='') as file:
            file.write(json.dumps(logs, indent=4))
    else:
        print('no matches found')
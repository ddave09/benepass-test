# benepass-test


Instructions:

1.) In the root tutorial directory, please run `docker-compose up`  (As asked listener will be on port 7331)

2.) Execute API format: /commands/<command_id>/execute/?machines=<comma_separated_machine_ids>
Example: http://localhost:7331/commands/1/execute/?machines=1,2,3

3.) Machines you mentioned are already added to the database. Accessible at `http://localhost:7331/machine/` API.

4.) I have added two commands. One valid (`ls -lrt`), one invalid (`qwew`). Accessible at `http://localhost:7331/commands/`

5.) Results are available at `http://localhost:7331/result`

6.) API authentication

    user: admin
    password: password123

**Please use the above credentials when making the request or log in to Django UI with the credentials.**

**Please note: strict slash is on, and pagination is set to 10**

Please let me know if you have any questions or concerns.

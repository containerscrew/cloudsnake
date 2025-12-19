# About

This is the tool I use every day to obtain local credentials (`~/.aws/credentials`) for all the accounts I have access
in my company’s AWS organization. We have AWS SSO configured with Google Workspaces. So, through a browser authenticated
with my Google Gmail account, I authenticate via AWS SSO.

For example, we have 40 accounts in our AWS organization, and as a member of the cloud team, I have access to all of
them. So, when using this tool, I will be able to get the credentials for all those accounts with the corresponding
mapped role (in my case `AdministratorAccess`).

Therefore, you’ll need:

- AWS SSO configured with your external `IdP`, which could be `Okta`, `Google Workspaces`, etc., and obtain an endpoint
  like: https://mycompany.awsapps.com/start

- To be authenticated in your `default` browser with the `IdP` you use (in my case, I’ve only tested it with the one I
  use, which is `Gmail (Google)`).

# Usage

Credentials will be stored in your `~/.aws/credentials` file, with the following format:

```ini
[AccountName@RoleName]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET
aws_session_token = YOUR_SESSION_TOKEN
region = YOUR_REGION
```

## Overriding the `AccountName@RoleName`

You can override the `AccountName@RoleName` in your `~/.aws/credentials` by using the following flags:

```shell
cloudsnake --region eu-west-1 sso get-credentials --start-url https://mycompany.awsapps.com/start--role-overrides cloudteam="" --account-overrides Development=development-account
```

Which will result in the following credentials file:

```ini
[Development@cloudteam] --> [development-account]
```

I'm changing the account name from `Development` to `development-account`, and the role name from `cloudteam` to an
empty string (no role name in the credentials file).

If you want to override the role name only, you can do it like this:

```shell
cloudsnake --region eu-west-1 sso get-credentials  --start-url https://mycompany.awsapps.com/start --role-overrides Developer-Team="developer-role"
```

```ini
[AccountName@Developer-Team] --> [AccountName@developer-role]
```

## Workers

If you have for example 40 accounts in your AWS organization, you can use the `--workers` flag to limit the number of concurrent tasks. This can help you avoid overwhelming the AWS API with too many requests (429) at once. More workers will speed up the process of fetching credentials for all accounts, but it may also lead to throttling if you set it too high.

```shell
cloudsnake --region eu-west-1 sso get-credentials --start-url https://test.awsapps.com/start --workers 15
```

> By default, the number of workers is set to `4`.

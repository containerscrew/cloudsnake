# RDS

[Official documentation, the good one](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html)

## Enable IAM authentication in your DB

Follow [this](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.Enabling.html) instructions


## Creating a user to authenticate using IAM

```shell
CREATE USER 'admin' IDENTIFIED WITH AWSAuthenticationPlugin AS 'RDS';
# Same persmissions as the admin user of an RDS
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, PROCESS, REFERENCES, INDEX, ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, BINLOG MONITOR, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER, DELETE HISTORY, SLAVE MONITOR ON *.* TO `admin`@`%`;
FLUSH PRIVILEGES;
```

> [!IMPORTANT]
> If you are assuming a role/iam user that has `Administrator privileges`, you don´t need to edit any IAM policy. You will be able to get the token to connect to the instance

If not, you need to edit the policies, like [here](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.IAMPolicy.html)

## Download TL/SSLS cert

If your database don´t enforce SSL/TLS connections, you can connect using `--skip-tls` flag from `mariadb cli`. But, I recommend to use always encrypted connections.

Download official cert, `please change the AWS region if needed`:

```shell
curl https://truststore.pki.rds.amazonaws.com/eu-west-1/eu-west-1-bundle.pem -O cert.pem
```

## Test your token before using `cloudsnake`

```shell
TOKEN=$(aws rds generate-db-auth-token --hostname sbx-rds-test.cyvl1212frfjnfrfregegspjksq.eu-west-1.rds.amazonaws.com --port 3306 --username
admin)
mariadb --host=sbx-rds-test.cyvl1212frfjnfrfregegspjksq.eu-west-1.rds.amazonaws.com --port=3306 --ssl-ca=cert.pem --user=admin --password=$TOKEN
select user from mysql.users;
```

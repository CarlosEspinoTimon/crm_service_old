#!/bin/bash
mysql -u user -h 127.0.0.1 -ppassword -D crm_db < initial_dump.sql
mysql -u user -h 127.0.0.1 -ppassword -D crm_db -e "INSERT INTO \`users\` (\`id\`, \`email\`, \`admin\`, \`admin_privileges_by\`, \`created_at\`, \`created_by\`, \`modified_at\`, \`modified_by\`) VALUES (1,'$1',1,1,NOW(),1,NOW(),1);"

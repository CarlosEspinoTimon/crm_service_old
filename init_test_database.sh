#!/bin/bash
mysql -u user -h 127.0.0.1 -ppassword -D test_crm < initial_dump_test.sql

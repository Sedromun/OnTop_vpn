#!/bin/bash

psql -U postgres <<-EOSQL
    CREATE DATABASE "vpn";
EOSQL

psql -U postgres -d "vpn" <<-EOSQL
    CREATE SCHEMA IF NOT EXISTS "users";
EOSQL


"""
Collection of functions to help establish the database
"""
import mysql.connector
import csv
import os


# Connect to MySQL and the task database
def connect_db(config):
    conn = mysql.connector.connect(
        host=config["DBHOST"],
        user=config["DBUSERNAME"],
        password=config["DBPASSWORD"],
        database=config["DATABASE"]
    )
    return conn


def setup_database(bookfile, customerfile, config):
    populate_book_tables(bookfile, config)
    populate_customer_tables(customerfile, config)


def populate_book_tables(csvfile, config):
    conn = connect_db(config)
    cursor = conn.cursor(dictionary=True)
    
    sql_books_insert = "INSERT INTO books (book_name, ISBN, author_lname, author_fname, library_location, status) VALUES (%s, %s, %s, %s, %s, %s)"

    with open(csvfile, "r") as csv_input:
        reader = csv.DictReader(csv_input)
        for row in reader:
            cursor.execute(sql_books_insert, (row["book_name"], row["ISBN"], row["author_lname"], row["author_fname"], row["library_location"], row["status"]))

    conn.commit()
    cursor.close()
    conn.close()


def populate_customer_tables(csvfile, config):
    conn = connect_db(config)
    cursor = conn.cursor(dictionary=True)
    
    sql_customers_insert = "INSERT INTO customers (lname, fname) VALUES (%s, %s)"

    with open(csvfile, "r") as csv_input:
        reader = csv.DictReader(csv_input)
        for row in reader:
            cursor.execute(sql_customers_insert, (row["lname"], row["fname"]))

    conn.commit()
    cursor.close()
    conn.close()


# Setup for the Database
#   Will erase the database if it exists
def init_db(config, bookfile, customerfile):
    conn = mysql.connector.connect(
        host=config["DBHOST"],
        user=config["DBUSERNAME"],
        password=config["DBPASSWORD"]
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"DROP DATABASE IF EXISTS {config['DATABASE']};")
    cursor.execute(f"CREATE DATABASE {config['DATABASE']};")
    cursor.execute(f"use {config['DATABASE']};")
    cursor.execute(
        f""" 
        CREATE TABLE books
        (
            book_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
            book_name VARCHAR(200),
            ISBN CHAR(13),
            author_lname VARCHAR(50),
            author_fname VARCHAR(50),
            library_location VARCHAR(15),
            status TINYINT(1),
            primary key (book_id)
        );

        CREATE TABLE customers
        (
            customer_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
            lname VARCHAR(30),
            fname VARCHAR(30),
            primary key (customer_id)
        );

        CREATE TABLE ledger
        (
            transaction_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
            book_fk SMALLINT UNSIGNED NOT NULL,
            customer_fk SMALLINT UNSIGNED NOT NULL,
            check_out_date DATE,
            return_date DATE,
            primary key (transaction_id)
        );
        """
    )
    cursor.close()
    conn.close()

    setup_database(bookfile, customerfile, config)

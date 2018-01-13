#!/usr/bin/env python3

'''
    udacity project 3 - log analysis

    aim

    your task is to create a reporting tool that prints out reports
    (in plain text) based on the data in the database. this reporting tool is a
    python program using the psycopg2 module to connect to the database.

    objective(s)

    a. what are the most popular three articles of all time?
    b. who are the most popualr article authors of all time?
    c. on which days did more than one percent of requests lead to an errors?
'''
import psycopg2
import datetime

DATABASE_NAME_ = "news"
FILE_NAME_ = "report.txt"

# this query retrieved the three most popular articles of all time;
query_popular_articles = """
    SELECT title, COUNT(log.path) as views
    FROM articles
    INNER JOIN log ON log.path = '/article/' || articles.slug
    WHERE log.status LIKE '200%'
    GROUP BY title
    ORDER BY views DESC
    LIMIT 3
"""

# this query retrieves the most popular article authors of all time;
query_popular_authors = """
    SELECT authors.name, COUNT(log.path) AS views
    FROM articles
    INNER JOIN authors ON authors.id = articles.author
    INNER JOIN log ON log.path = '/article/' || articles.slug
    WHERE log.status LIKE '200%'
    GROUP BY authors.name
    ORDER BY views DESC;
"""

# this query retrieves the date(s) where error/request ratio is above 1%;
query_error_occurrence = """
    SELECT
    errors.time::date AS date,
    ROUND((errors.count::float / totals.count::float)::numeric * 100, 2) AS
    percentage
    FROM
    errors
    INNER JOIN totals ON totals.time::date = errors.time::date
    WHERE errors.count::float / totals.count::float > 0.01;
"""


def title_format(title):
    '''
        function:- title_header;
        parameter(s):-
            + title   ~> a string describing the data table;

        return:- string;

        description:- function used to format the data table title;
    '''

    return "{:^60}".format(title.upper())


def header_format(colh1, colh2):
    '''
        function:- header_format;
        parameter(s):-
            + colh1    ~> a string describing the header for column one;
            + colh2    ~> a string describing the header for column two;

        return:- string;

        description:- function used to format data table column header(s);
    '''

    return "{:^32} | {:^20}".format(colh1, colh2)


def delimiter_format(sign='-'):
    '''
        function:- delimiter_format;
        parameter(s):-
            + sign     ~> a delimiter character;

        return:- string;

        description:- a function used to format row delimiter;
    '''

    return "{:-^33}+{:-^20}".format(sign, sign)


def row_format(col1, col2):
    '''
        function:- row_format;
        parameter(s):-
            + col1     ~> data element for column one;
            + col2     ~> data element for column two;

        return:- string;

        description:- a function used to format row(s);
    '''

    return "{:^32} | {:^20}".format(col1, col2)


def execute(command):
    '''
        function:- execute;
        parameter(s):-
            + command   ~>   SQL query string;

        return:- tuple;

        description:- function used to execute SQL command(s);
    '''
    try:
        db = psycopg2.connect(dbname=DATABASE_NAME_)

        cursor = db.cursor()

        cursor.execute(command)

        result = cursor.fetchall()

        db.close()

    except psycopg2.Error as error_message:
        print("woops! there was an error with the database connection")
        print("error:- ", error_message)

    return result


def print_to_terminal(label, headerx, headery, data):
    '''
        function:- print_to_terminal;
        parameter(s):-
            + label     ~>   label used to describe data inside the table;
            + headerx   ~>   first column header;
            + headery   ~>   second column header;

        return:- void;

        description:- based on two-column data table structure, a function
                      used to write content of executed SQL query to file;
    '''

    title = title_format(label)
    header = header_format(headerx, headery)
    delimiter = delimiter_format()

    print("\n" + title + "\n")
    print(header)

    for row in data:
        print(delimiter)

        if(isinstance(row[0], datetime.date)):
            col_one = row[0].strftime("%m/%d/%Y")
            col_two = str(row[1]) + "%"
        else:
            col_one = row[0]
            col_two = row[1]

        entry = row_format(col_one, col_two)

        print(entry)


def print_to_report(label, headerx, headery, data, fop='a'):
    '''
        function:- print_to_report;
        parameter(s):-
            + label     ~>   label used to describe data inside the table;
            + headerx   ~>   first column header;
            + headery   ~>   second column header;
            + data      ~>   SQL query result;
            + fop       ~>   file operation type ('r', 'w', 'a' etc.)

        return:- void;

        description:- based on two-column data table structure, a function
                      used to write content of executed SQL query to output
                      file;
    '''

    title = title_format(label)
    header = header_format(headerx, headery)
    delimiter = delimiter_format()

    with open(FILE_NAME_, fop) as output_file:
        output_file.write("\n" + title + "\n")
        output_file.write(header + "\n")

        for row in data:
            if(isinstance(row[0], datetime.date)):
                col_one = row[0].strftime("%m/%d/%Y")
                col_two = str(row[1]) + "%"
            else:
                col_one = row[0]
                col_two = row[1]

            entry = row_format(col_one, col_two)

            output_file.write(delimiter + "\n")
            output_file.write(entry + "\n")

        output_file.close()


if __name__ == "__main__":
    '''
        main program

        story:-
            1 ~ execute first SQL query to deduce the popular articles;
            2 ~ initialize table properties title and column headers;
            3 ~ get result(s)
            4 ~ execute second SQL query to deduce the popular authors;
            5 ~ (2);
            6 ~ (3);
            7 ~ execute third SQL query to deduce date(s) with error/request
                ratio above one percent;
            8 ~ (2);
            9 ~ (3);
    '''

    # (1)
    data = execute(query_popular_articles)

    # (2)
    label = "what are the most popular articles of all time"
    headerx = "article"
    headery = "views"

    # (3)
    print_to_terminal(label, headerx, headery, data)
    print_to_report(label, headerx, headery, data, 'w')

    # (4)
    data = execute(query_popular_authors)

    # (5)
    label = "who are the most popular article authors of all time?"
    headerx = "author"
    headery = "article views"

    # (6)
    print_to_terminal(label, headerx, headery, data)
    print_to_report(label, headerx, headery, data)

    # (7)
    data = execute(query_error_occurrence)

    # (8)
    label = "on which days did more than 1% of requests lead to an errors?"
    headerx = "date"
    headery = "error rate"

    # (9)
    print_to_terminal(label, headerx, headery, data)
    print_to_report(label, headerx, headery, data)

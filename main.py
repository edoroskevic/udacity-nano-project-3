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

database_name_ = "news"
file_name_ = "report.txt"

# this query retrieved the three most popular articles of all time;
query_popular_articles = """
    SELECT articles.title, COUNT(log.path) as views
    FROM articles
    INNER JOIN authors ON authors.id = articles.author
    INNER JOIN log ON log.path LIKE '%' || articles.slug || '%'
    WHERE log.status LIKE '%200%'
    GROUP BY authors.name, articles.title
    ORDER BY views DESC
    LIMIT 3
"""

# this query retrieves the most popular article authors of all time;
query_popular_authors = """
    SELECT authors.name, COUNT(log.path) AS views
    FROM articles
    INNER JOIN authors ON authors.id = articles.author
    INNER JOIN log ON log.path LIKE '%' || articles.slug || '%'
    WHERE log.status LIKE '%200%'
    GROUP BY authors.name
    ORDER BY views DESC;
"""

# this query retrieves the date(s) where error/request ratio is above 1%;
query_error_occurrence = """
    CREATE OR REPLACE VIEW errors AS
    SELECT time::date, COUNT(status) FROM log WHERE status LIKE '%404%'
    GROUP BY time::date;

    CREATE OR REPLACE VIEW totals AS
    SELECT time::date, COUNT(status) FROM log GROUP BY time::date;

    SELECT
    errors.time::date AS date,
    ROUND((errors.count::float / totals.count::float)::numeric * 100, 2) AS
    percentage
    FROM
    errors
    INNER JOIN totals ON totals.time::date = errors.time::date
    WHERE errors.count::float / totals.count::float > 0.01;
"""

# table properties;
title_format = lambda title: "{:^60}".format(title.upper())
header_format = lambda colh1, colh2: "{:^32} | {:^20}".format(colh1, colh2)
delimiter_format = lambda sign="-": "{:-^33}+{:-^20}".format(sign, sign)
row_format = lambda col1, col2: "{:^32} | {:^20}".format(col1, col2)

'''
    function:- execute;
    parameter(s):-
        + command   ~>   SQL query string;

    return:- tuple;

    description:- function used to execute SQL command(s);
'''
def execute(command):
    cursor.execute(command);
    result = cursor.fetchall();

    return result

'''
    function:- print_to_terminal;
    parameter(s):-
        + label     ~>   label used to describe data inside the table;
        + headerx   ~>   first column header;
        + headery   ~>   second column header;

    return:- void;

    description:- based on two-column data table structure, a function used to
                  write content of executed SQL query to file;
'''
def print_to_terminal(label, headerx, headery, data):
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

'''
    function:- print_to_report;
    parameter(s):-
        + label     ~>   label used to describe data inside the table;
        + headerx   ~>   first column header;
        + headery   ~>   second column header;
        + data      ~>   SQL query result;
        + fop       ~>   file operation type ('r', 'w', 'a' etc.)

    return:- void;

    description:- based on two-column data table structure, a function used to
                  write content of executed SQL query to output file;
'''
def print_to_report(label, headerx, headery, data, fop='a'):
    title = title_format(label)
    header = header_format(headerx, headery)
    delimiter = delimiter_format()

    with open(file_name_, fop) as output_file:
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

'''
    main program

    story:-
        1 ~ initialize connection to the database using 'psycopg2' interface;
        2 ~ check connection to the database;
        3 ~ retrieve database cursor;
        4 ~ execute first SQL query to deduce the popular articles;
        5 ~ initialize table properties title and column headers;
        6 ~ present result(s)
        7 ~ execute second SQL query to deduce the popular authors;
        8 ~ (5);
        9 ~ (6);
        10 ~ execute third SQL query to deduce date(s) with error/request ratio
            above one percent;
        11 ~ (5);
        12 ~ (6);
'''
if __name__ == "__main__":
    # (1)
    db = psycopg2.connect(dbname=database_name_)

    # (2)
    if db.closed < 1:
        # (3)
        cursor = db.cursor()

        # (4)
        data = execute(query_popular_articles)

        # (5)
        label = "what are the most popular articles of all time"
        headerx = "article"
        headery = "views"

        # (6)
        print_to_terminal(label, headerx, headery, data)
        print_to_report(label, headerx, headery, data, 'w')

        # (7)
        data = execute(query_popular_authors)

        # (8)
        label = "who are the most popular article authors of all time?"
        headerx = "author"
        headery = "article views"

        # (9)
        print_to_terminal(label, headerx, headery, data)
        print_to_report(label, headerx, headery, data)

        # (10)
        data = execute(query_error_occurrence)

        # (11)
        label = "on which days did more than 1% of requests lead to an errors?"
        headerx = "date"
        headery = "error rate"

        # (12)
        print_to_terminal(label, headerx, headery, data)
        print_to_report(label, headerx, headery, data)
    else:
        print("oops! something went wrong connecting to the database!")

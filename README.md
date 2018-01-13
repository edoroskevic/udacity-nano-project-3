# Description

Based on the data in the database, the aim of this task is to create a reporting tool that prints out reports
(in plain text). This project is a demonstration of a progress in knowledge and skill whilst undertaking
a _Nanodegree in Full-Stack Web Development_ provided by Udacity and partner(s).

The reporting tool is developed using [Python](https://www.python.org/) programming language and [PostgreSQL](https://www.postgresql.org/) - a popular open-source Object-Relational Database System. For demonstration purposes, the project is using a database of
a fictional news website.

The project has been checked for [PEP8](https://www.python.org/dev/peps/pep-0008/) compliance using latest version of [pycodestyle](https://pypi.python.org/pypi/pycodestyle)

Based on information stored inside the database, the project will answer following question(s):-

a. what are the most popular three articles of all time?
b. who are the most popular article authors of all time?
c. on which days did more than one percent of requests lead to an errors?

keyword(s): Python, PostgreSQL

# Learning Outcome

+ Technical demonstration of knowledge and skill when using Python and PostgreSQL

# Requirements

+ [Download and Install VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
+ [Download and Install Vagrant](https://www.vagrantup.com/downloads.html)
+ [Download and Install Vagrant Configuration File](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip)
+ [Download and Install Database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

# Running Vagrant

From command-line or terminal, inside the vagrant sub-directory run command

`vagrant up`

Given this is the first time you are running the above command, `vagrant` will download
the Linux OS and install it for future virtualization. This process can take some time
depending on users internet connection. Upon completing the installation, run

`vagrant ssh`

This will connect you to your newly downloaded and installed Linux OS. In order to terminate
this connection enter

`exit` or press `CTRL + D`

# Setting Database

Given you've downloaded database file described in requirements section, you must unzip this file retrieving `newsdata.sql` file on output.
Place this file into vagrant directory and run

`psql -d news -f newsdata.sql`

The above command will execute SQL commands stored in `newsdata.sql`, and it will connect you to the `news` database.

NOTE:- In order to quit `psql`, type `\q` and hit enter;

Given the above has been executed, the project requires some additional views to be loaded. The project contains file `create_views.sql`.
Similarly to the above, pleace this file into vagrant directory and run

`psql -d news -f create_views.sql`

It contains necessary SQL command(s) to create required views to assist in answering the questions described in the description.

# Execution

1. Launch your vagrant emulator
`vagrant up`
2. SSH into emulated virtual machine
`vagrant ssh`
3. Navigate to vagrant folder
`cd /vagrant/`
4. Execute Python code
`python main.py`

# Output

###    WHAT ARE THE MOST POPULAR ARTICLES OF ALL TIME

|            article              |        views      |
| --- | --- |
|Candidate is jerk, alleges rival |        338647     |
|Bears love berries, alleges bear |        253801     |
|Bad things gone, say good people |        170098     |

###  WHO ARE THE MOST POPULAR ARTICLE AUTHORS OF ALL TIME?

|            author               |    article views  |
| --- | --- |
|        Ursula La Multa          |        507594     |
|    Rudolf von Treppenwitz       |        423457     |
|     Anonymous Contributor       |        170098     |
|         Markoff Chaney          |        84557      |

### ON WHICH DAYS DID MORE THAN 1% OF REQUESTS LEAD TO AN ERRORS?

|              date               |      error rate    |
| --- | --- |
|           07/17/2016            |        2.26%       |

this data will also be made available in newly generated file ~ `report.txt`

# Description

The aim of this task is to create a reporting tool that prints out reports
(in plain text) based on the date in the database. This reporting tool is a
Python program using the `psycopg2` module to connect to the database.

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

Given you've downloaded database file described in requirements, you must unzip this file retrieving `newsdata.sql` file on output.
Place this file into vagrant directory and run

`vagrant -d news -f newsdata.sql`

The above command will execute SQL commands stored in `newsdata.sql`, and it will connect you to the `news` database.

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


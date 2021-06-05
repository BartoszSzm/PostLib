PostLib
=======

Library management system with the PostgreSQL database written in the Python tkinter.
<img src="https://imgur.com/a/sBzD2GM" alt="Screenshot on Pop!OS Linux">

__About__
-----------

The program is fully written in the Python Tkinter. It's an admin side of a library management system with the PostgreSQL database under hood. The capabilities of the program are divided into three sections: books, readers and issues. 

The program offers basic operations like:

### Adding a publication/reader <br>
Here you can enter some data about the new publications or readers. Some information is mandatory. The program will throw an error window when you do something wrong.

### Deleting publications from the library stock <br>
This window gives you the possibility to carefully remove publications from the library stock. To delete a publication you need to enter the library ID (unique number assigned automatically when publication is added to the library stock). Then in the small window below all its data will be shown. Now, before confirming deletion you can check if the given library ID is correct and see publication data. 

### Publications/readers/issues searching engine <br>
You can also search for any publication, reader or issue in the database. To get results select criteria, enter the phrase and hit the Enter key or Search button. You can also show all records by leaving the search entry blank.

### Issue book to someone
Of course, this function is also included. To issue a book you need to give information about the reader (reader ID) and the publication that will be issued (library ID). The limit date when the publication should be returned is also needed - this date will be selected automatically, depending on the default setting in config.ini. When you try to issue a publication that doesn't exist in the database or the reader's name doesn't exist in the database, you will receive an error from the program. Also, an error will be thrown when you select the wrong date (date from the past for example) or when the publication is already issued. 

### Return a book to the library stock
In this window you can return a publication to the library stock. To do this, enter the Reader ID and hit the Search or Enter key. From searched publications select the one you want to be returned. If the reader is delayed, a penalty will be imposed - you can see it in the penalty entry. Also, if you know the password, you can edit the penalty. The app will throw an error if the Reader ID is wrong or doesn't exist, or when the selected publication has been already returned. By hitting the Accept button you save changes in the database - the publication is returned and can be issued again.

### Database
The database is divided into three tables - publications, issues and person. As the name suggests, the publications table holds the data about all publications (title, author, kind, ISBN, pages, language, etc.). Issues table holds information about all issues (issue ID, reader ID, library ID, issue date, etc.). Similarly, person table - here information about readers will be stored (reader ID, full name, phone number, e-mail, etc.).
Tables have implemented triggers which make all database more automatic. For example, when publication is being returned, the triggers automatically update the issued record with the current date and change the 'is_issued' value to False. There are few more triggers - ff you want to see them all, just use PgAdmin or psql.

__Installation__
----------------
1. Clone repository.
2. Use setup.py to install app. Change directory to folder with setup.py and:
```
$ pip install .
```
```
$ pip3 install .
```
3. To use the app you need the PostgreSQL so please, install it and create two new databases using PgAdmin or psql. One of them will be production db, the second one will be for testing purposes.
4. In folder 'db_dumps' you have dumps of production and test databases. Load it from this files using pgAdmin or psql. In psql it will be:
```
$ psql -U postgres -d (your production db name) < /path/to/postlib_db.sql
```
5. Repeat above process to load the test database:
```
$ psql -U postgres -d (your test db name) < /path/to/postlib_test.sql
```
6. The last step is to configure config.ini. In this file you can change some app options and here you should enter information about the connection with your database. Change only:<br>
'database' - your production/test database name <br>
'user' - your user name or just 'postgres' <br>
'password' - your user password <br>

__Contents__
-------------
App files structure consists of three directories:<br>
1. Main 'PostLib' folder - here you find the main file PostLib.py which runs the whole app. In config.ini you can change some in-program options (penalty, issue_limit and password).
2. Buttons folder - each of .py files in this folder represents files with different functions of the app. 
3. db_dumps folder - it's pg_dump files to create a new database.
4. tests folder - here you can find all the tests. One file to one program function.
5. images - folder contains picture which will be displayed in main window

__Future developments__
-----------------------
- Deleting readers/issues
- Improved searching
- Including sorting in tables
- Client side app


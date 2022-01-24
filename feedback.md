# Project Feedback

Firstly really well done for such a well presented and executed project. The presentations were fantastic and documentation was through.

This was not an easy project as I can imagine. The team went above expectations by implementing a frontend and authentication to manage user 
login time and sessions.

This feedback goes more into detail what was good and what could be improved.

## Presentation & Reporting

- The report is well written and provides a through explanation of inner workings of the app plus a through background. The structure of the report can be improved by moving all the implementation details and game logic to the implementation section.
- Sometimes it was hard to follow along report as a lot of implementation details have been provided in the background section. The report jumps around quite a lot.
- Perfect elaboration of project management and tools used.
- Great practice working with a dev db to test the implementation.
- Good and concise conclusion providing a summary and future work.

## Code
- Great uses of OOP principles all around the codebase and short routines
- Some functions seem to monkey patch the logic - For instance the tictac toe game is_a_win function is literally coding every possible scenario instead of coding the logic pattern.
- Great use of decorators to manage db connections - well done
- The routes file is MASSIVE! Makes it hard to maintain. Break down the routes into several files.
- Some variable and function names are way too long - making it harder to read the code.
- Not a lot of error handling some of the functions that take expose the app to the outside world (routes and endpoints)
- Not clear what the purpose of models.py is.
- Amazing test suite covering all of the games and several logic around the app.
- Some folder namings and file structure could be improved (i.e. Bootstrap folder could be renamed stylesheets). Static folder could be renamed Views. and templates could be provided in the views.
- It's not clear which python file is the entry point of the app.
- Good readme with screenshots, usage and installation instructrions.

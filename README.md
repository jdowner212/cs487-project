# CS 487 Project
GUI APP written in Python using tkinter and sqlite.
Application is secured for inserting incorrect data.
All methods, modules and classes have proper docstrings.


## Features
- create new account
- login as admin or user (the appropriate window will open based on permissions)
- User: search and order products (if available in stock), edit account
- Admin: CRUD operations for customers, products and orders

## Handy solutions
- All tables are interactive, each row can be selected - based on selection other tables or inputs handle specific event
- Example: When admin clicks on specific order, appropriate user and products will be listed in tables,
it works identically the other way round so there is no need to manually write user's or product's details

# example acc:

- Admin perms

login: admin,
passsword: admin123

- User perms

login: wojtekkk,
password: mojehaslo123



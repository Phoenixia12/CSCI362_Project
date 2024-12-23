from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import connection
from django.utils.safestring import mark_safe
import calendar
import datetime
import requests
import logging
import os


import os
import logging
import logging.config

# Set BASE_DIR to the directory containing app_logs.log

logger = logging.getLogger('django')

# Log a test message



def add_account(user_acct_id, perm_id, username, email, gym_id, firstname, lastname, datejoined, password_val):
    with connection.cursor() as cursor:
        cursor.callproc('AddAccount', [
            user_acct_id, perm_id, username, email, gym_id, firstname, lastname, datejoined, password_val
        ])
import pyodbc
from django.shortcuts import render

import pyodbc
import random
from django.contrib.auth.hashers import make_password  # Use to hash the password
from django.shortcuts import render, redirect
from django.contrib import messages

def register_account(request):
    logger = logging.getLogger('django')
    if request.method == 'POST':
        # Extract form data from request
        username = request.POST.get('username')
        email = request.POST.get('email')
        perm_id = 1 # Ensure you have this in your form
        gym_id = 3  # Ensure you have this in your form
        firstname = request.POST.get('firstname')  # Ensure you have this in your form
        lastname = request.POST.get('lastname')  # Ensure you have this in your form
        #datejoined = request.POST.get('datejoined')  # Ensure you have this in your form
        password_val = request.POST.get('password')  # Ensure you have this in your form

        # Connect to the database
        conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=gymassisthost2.database.windows.net;DATABASE=gymassistdb;UID=admin_user;PWD=lamp4444!')
        cursor = conn.cursor()

        # Check if username or email already exists
        cursor.execute("SELECT COUNT(*) FROM user_accounts WHERE username = ? OR email = ?", (username, email))
        count = cursor.fetchone()[0]
        if count > 0:
            messages.error(request, 'Username or email already exists.')
            return render(request, 'register_account.html')

        # Generate a unique user_acct_id
        while True:
            user_acct_id = random.randint(1, 10000000)  # Adjust range as needed
            cursor.execute("SELECT COUNT(*) FROM user_accounts WHERE user_acct_id = ?", (user_acct_id,))
            count = cursor.fetchone()[0]
            if count == 0:  # If the ID is unique, break the loop
                break

        # Hash the password before storing it
        hashed_password = make_password(password_val)
        
        # Call the stored procedure to insert the user
        print('inserting')
        cursor.execute(
            "EXEC AddAccount @user_acct_id=?, @perm_id=?, @username=?, @email=?, @gym_id=?, @firstname=?, @lastname=?, @datejoined=?, @password_val=?", 
            (user_acct_id, perm_id, username, email, gym_id, firstname, lastname, datetime.date.today(), hashed_password)
        
        )
        print('insert sucessful')
        logger.info(f"User registered with username: {username}, email: {email}")
        #try:
            # Call the stored procedure to add user credentials to the pass table
            #cursor.execute(
              #  "EXEC AddUserToPass @user_acct_id=?, @password=?", 
              #  (user_acct_id, hashed_password)  # Use the hashed password
           # )
        #except Exception as e:
          #  messages.error(request, f'An error occurred while adding user to pass: {str(e)}')

        # Commit the transaction
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()
        
        # Redirect to login or render success message
        messages.success(request, 'Account registered successfully! Please log in.')
        return redirect('login')

    user_acct_id = request.user.id  # assigns the authenticated user’s ID to user_acct_id
    
    return render(request, 'register_account.html')


def add_member(request):
    logger = logging.getLogger('django')
    # Connect to the database
    conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=gymassisthost2.database.windows.net;DATABASE=gymassistdb;UID=admin_user;PWD=lamp4444!')
    cursor = conn.cursor()

    if request.method == 'POST':
        # Extract form data from request
        username = request.POST.get('username')
        email = request.POST.get('email')
        perm_id = 4  # Ensure you have this in your form (assuming a default for gym goer)
        gym_id = cache.get('gym_id')  # Ensure you have this in your form (from session or elsewhere)
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password_val = request.POST.get('password')

        # Check if username or email already exists
        cursor.execute("SELECT COUNT(*) FROM user_accounts WHERE username = ? OR email = ?", (username, email))
        count = cursor.fetchone()[0]
        if count > 0:
            logger.warning(f"Username or email already exists: username={username}, email={email}")
            messages.error(request, 'Username or email already exists.')
            return render(request, 'add_member.html')

        # Generate a unique user_acct_id
        while True:
            user_acct_id = random.randint(1, 10000000)  # Adjust range as needed
            cursor.execute("SELECT COUNT(*) FROM user_accounts WHERE user_acct_id = ?", (user_acct_id,))
            count = cursor.fetchone()[0]
            if count == 0:  # If the ID is unique, break the loop
                break

        # Hash the password before storing it
        hashed_password = make_password(password_val)

        # Log the account creation attempt
        logger.info(f"Attempting to create account for user {username} (ID: {user_acct_id}) at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        try:
            # Call the stored procedure to insert the user
            cursor.execute(
                "EXEC AddAccount @user_acct_id=?, @perm_id=?, @username=?, @email=?, @gym_id=?, @firstname=?, @lastname=?, @datejoined=?, @password_val=?", 
                (user_acct_id, perm_id, username, email, gym_id, firstname, lastname, datetime.date.today(), hashed_password)
            )

            # Commit the transaction
            conn.commit()

            # Log success
            logger.info(f"Successfully created account for user {username} (ID: {user_acct_id}) and assigned to gym ID: {gym_id} on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # Close the connection
            cursor.close()
            conn.close()

            # Redirect to login or render success message
            messages.success(request, 'Account registered successfully! Please log in.')
            return redirect('home_owner')

        except Exception as e:
            # Log the error if something goes wrong with the stored procedure
            logger.error(f"Error occurred while creating account for {username} (ID: {user_acct_id}). Error: {str(e)}")
            messages.error(request, f'An error occurred while registering: {str(e)}')

            # Close the connection
            cursor.close()
            conn.close()

    return render(request, 'add_member.html')

def add_employee(request):
    logger = logging.getLogger('django')
     # Connect to the database
    conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=gymassisthost2.database.windows.net;DATABASE=gymassistdb;UID=admin_user;PWD=lamp4444!')
    cursor = conn.cursor()

    
    if request.method == 'POST':
        # Extract form data from request
        username = request.POST.get('username')
        email = request.POST.get('email')
        perm_id = request.POST.get('employeetype')  # Ensure you have this in your form
        gym_id = cache.get('gym_id') # Ensure you have this in your form
        firstname = request.POST.get('firstname')  # Ensure you have this in your form
        lastname = request.POST.get('lastname')  # Ensure you have this in your form
        #datejoined = request.POST.get('datejoined')  # Ensure you have this in your form
        password_val = request.POST.get('password')  # Ensure you have this in your form

        

        # Check if username or email already exists
        cursor.execute("SELECT COUNT(*) FROM user_accounts WHERE username = ? OR email = ?", (username, email))
        count = cursor.fetchone()[0]
        if count > 0:
            messages.error(request, 'Username or email already exists.')
            return render(request, 'add_employee.html')

        # Generate a unique user_acct_id
        while True:
            user_acct_id = random.randint(1, 10000000)  # Adjust range as needed
            cursor.execute("SELECT COUNT(*) FROM user_accounts WHERE user_acct_id = ?", (user_acct_id,))
            count = cursor.fetchone()[0]
            if count == 0:  # If the ID is unique, break the loop
                break

        # Hash the password before storing it
        hashed_password = make_password(password_val)

        # Call the stored procedure to insert the user
        print('inserting')
        cursor.execute(
            "EXEC AddAccount @user_acct_id=?, @perm_id=?, @username=?, @email=?, @gym_id=?, @firstname=?, @lastname=?, @datejoined=?, @password_val=?", 
            (user_acct_id, perm_id, username, email, gym_id, firstname, lastname, datetime.date.today(), hashed_password)
        
        )
        print('insert sucessful')
        # New db does not have pass db 
        #try:
            # Call the stored procedure to add user credentials to the pass table
        #    cursor.execute(
        #        "EXEC AddUserToPass @user_acct_id=?, @password=?", 
        #        (user_acct_id, hashed_password)  # Use the hashed password
        #    )
        #except Exception as e:
        #    messages.error(request, f'An error occurred while adding user to pass: {str(e)}')

        # Commit the transaction
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        # Redirect to login or render success message
        messages.success(request, 'Account registered successfully! Please log in.')
        return redirect('home_owner')

    return render(request, 'add_employee.html')


# Create your views here.
def index(request, *args, **kwargs):
    return render(request, 'frontend/index.html')



import pyodbc
from django.contrib.auth.hashers import check_password  # To compare hashed passwords
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.cache import cache
from django.utils import timezone

#update_gym_info(297577, "individual test for about", "individual test for contact")

def login_view(request):
    print("login is being run")
    logger = logging.getLogger('django')
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        ip_address = request.META.get('REMOTE_ADDR')
        logger.info(f"Login attempt for user: {username}, IP: {ip_address}")
        
        # Unique key for this user/IP pair
        cache_key = f"login_attempts_{username}_{ip_address}"
        lockout_key = f"lockout_{username}_{ip_address}"

        # Check if user is locked out
        lockout_until = cache.get(lockout_key)
        if lockout_until:
            if timezone.now() < lockout_until:
                messages.error(request, "Account temporarily locked. Try again later.")
                logger.info(f"Locked out user '{username}' attempted login.")
                return redirect('login')
            else:
                cache.delete(lockout_key)  # Clear lockout if expired

        # Retrieve current failed attempt count
        attempts = cache.get(cache_key, 0)

        # Connect to the database
        try:
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 18 for SQL Server};'
                'SERVER=gymassisthost2.database.windows.net;'
                'DATABASE=gymassistdb;UID=admin_user;PWD=lamp4444!'
            )
            cursor = conn.cursor()

            # Query to get the user based on the username and retrieve perm_id as well
            cursor.execute("SELECT user_acct_id, password_val, perm_id, gym_id FROM user_accounts WHERE username = ?", (username,))
            user = cursor.fetchone()

            if user:
                user_id, stored_password_hash, perm_id, gym_id = user
                cache.set('gym_id', gym_id, None)
                cache.set('user_id', user_id, None)

                # Check if the provided password matches the stored hash
                if check_password(password, stored_password_hash):
                    # Password matches, log the user in
                    request.session['user_id'] = user_id  # Store user ID in session
                    #messages.success(request, 'You are now logged in!')
                    
                    # Log successful login
                    logger.info(f"User '{username}' successfully logged in with user_acct_id={user_id}.")

                    # Reset login attempts on successful login
                    cache.delete(cache_key)

                    # Check if perm_id is null, if so redirect to role selection
                    if gym_id == 3:  # If perm_id is null
                        return redirect('owner_setup')
                    
                    if perm_id == 1:
                        return redirect('home_owner')  # Redirect to owner's home page
                    elif perm_id == 2:
                        return redirect('home_staff')  # Redirect to staff's home page
                    elif perm_id == 4:
                        return redirect('home_goer')  # Redirect to goer's home page
                else:
                    # If password doesn't match
                    attempts += 1
                    cache.set(cache_key, attempts, 1800)  # Cache failed attempts for 30 minutes

                    # Lock out user if they exceed limit
                    if attempts >= 5:
                        lockout_duration = timezone.now() + timezone.timedelta(minutes=30)
                        cache.set(lockout_key, lockout_duration, 1800)  # Set 30-min lockout
                        cache.delete(cache_key)  # Reset attempts after lockout
                        messages.error(request, "Account locked due to multiple failed login attempts.")
                        logger.warning(f"User '{username}' locked out after multiple failed login attempts.")
                    else:
                        messages.error(request, "Invalid username or password.")
                        logger.warning(f"Failed login attempt for non-existent user '{username}'.")
                    return redirect('login')
            else:
                # If no user found with the given username
                messages.error(request, 'Invalid username or password.')
                logger.warning(f"Failed login attempt for non-existent user '{username}'.")
                return redirect('login')

        except Exception as e:
            # Log the exception
            messages.error(request, f'An error occurred: {str(e)}')
            logger.error(f"Error during login process for user '{username}': {str(e)}")
            return redirect('login')

        finally:
            # Ensure both cursor and connection are closed safely
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    return render(request, 'login.html')






def create_gym(gym_name):
    logger = logging.getLogger('django')
    # Generate a new gym_id (ensure it meets your existing constraints)
    gym_id = random.randint(1, 1000000)  # Adjust range as necessary

    user_acct_id = cache.get('user_id')
    # Connect to the database and insert the new gym
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=gymassisthost2.database.windows.net;'
            'DATABASE=gymassistdb;'
            'UID=admin_user;'
            'PWD=lamp4444!'
        )
        cursor = conn.cursor()

        # Insert the gym into the gym table
        cursor.execute("INSERT INTO gym (gym_id, gym_name,owner_id) VALUES (?, ?, ?)", (gym_id, gym_name, user_acct_id))
        conn.commit()

        print(f'Created gym: {gym_name} with ID: {gym_id}')
        cache.set('gym_id', gym_id, None)
        return gym_id, gym_name  # Return the gym ID and name

    except Exception as e:
        print(f'Failed to create gym. Error: {str(e)}')
        return None, None  # Return None if the operation fails

    finally:
        # Ensure cursor and connection are closed
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# gym db no longer holds owner_id as of 11/5/24

def set_owner_for_gym(gym_id, owner_id):
    # Connect to the database
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=gymassisthost2.database.windows.net;'
            'DATABASE=gymassistdb;'
            'UID=admin_user;'
            'PWD=lamp4444!'
        )
        cursor = conn.cursor()

    
        # Update the owner_id for the specified gym
        cursor.execute("UPDATE user_accounts SET gym_id = ? WHERE user_acct_id = ?", (gym_id, owner_id))
        # Commit the transaction
        conn.commit()
        #cursor.execute("UPDATE gym SET owner_id = ? WHERE gym_id = ?", (owner_id, gym_id))
        #conn.commit()

        # Check if the update was successful
        if cursor.rowcount > 0:
            print(f'Successfully updated owner_id for gym_id: {gym_id}')
        else:
            print(f'No gym found with gym_id: {gym_id}')

    except Exception as e:
        print(f'Failed to execute query. Error: {str(e)}')

    finally:
        # Ensure both cursor and connection are closed safely
        if cursor:
           cursor.close()
        if conn:
            conn.close()


def get_user_acct_id_by_username(username):
    try:
        # Connect to the database
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=gymassisthost2.database.windows.net;'
            'DATABASE=gymassistdb;UID=admin_user;PWD=lamp4444!'
        )
        cursor = conn.cursor()

        # Query to get user_acct_id by username
        cursor.execute("SELECT user_acct_id FROM user_accounts WHERE username = ?", (username,))
        result = cursor.fetchone()

        if result:
            return result[0]  # Return the user_acct_id
        else:
            return None  # Username not found

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

    finally:
        # Ensure both cursor and connection are closed safely
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def owner_setup(request):
    logger = logging.getLogger('django')
    if request.method == 'POST':
        gym_name = request.POST.get('gym_name')
        user_acct_id = cache.get('user_id')  # Get the user_acct_id from session
        username = request.POST.get('username')
        
        logger.info(f"Owner setup initiated for user_acct_id: {user_acct_id}, gym_name: {gym_name}")

        if user_acct_id is None:
            logger.error(f"User account ID not found in session for username: {username}")
            messages.error(request, 'User account ID not found in session.')
            # No URL exists for 'error_page'
          #  return redirect('error_page')  # Redirect to an error page or handle appropriately
            return redirect('login')

        #user_acct_id = get_user_acct_id_by_username(username)
        #convert_user_to_owner(user_acct_id)
        # Step 1: Create a new gym and get the gym_id
        gym_id, gym_name_created = create_gym(gym_name)

        # Check if gym creation was successful
        if gym_id is None:
            logger.error(f"Failed to create gym: {gym_name} for user_acct_id: {user_acct_id}")
            messages.error(request, 'Failed to create gym. Please try again.')
            #return redirect('error_page')  # Redirect to an error page if gym creation fails
            return redirect('login')

        
        # Step 2: Set the owner_id for the created gym
        set_owner_for_gym(gym_id, user_acct_id)

        logger.info(f"Gym created successfully with gym_id: {gym_id}, gym_name: {gym_name_created}")
        messages.success(request, 'Owner setup completed successfully!')

        
        return redirect('home_owner')  # Redirect to the owner's home page

    return render(request, 'owner_setup.html')  # Render the owner setup page for GET requests



def gym_selection(request):
    logger = logging.getLogger('django')
    conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};'
                'SERVER=gymassisthost2.database.windows.net;'
                'DATABASE=gymassistdb;UID=admin_user;PWD=lamp4444!')
    cursor = conn.cursor()

    cursor.execute("SELECT gym_id, name FROM gym")
    gym = cursor.fetchall()
    
    if request.method == 'POST':
        selected_gym_id = request.POST.get('gym_id')

        # Update user account with the selected gym_id and perm_id
        cursor.execute("UPDATE user_accounts SET perm_id = ?, gym_id = ? WHERE user_acct_id = ?", (request.session['perm'], selected_gym_id, request.session['user_acct_id']))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect('home')

    return render(request, 'gym_selection.html', {'gyms': gym})

def staff_setup(request):
    logger = logging.getLogger('django')
    if request.method == 'POST':
        gym_id = request.POST.get('gym')  # Get the selected gym ID from the form
        user_acct_id = request.session.get('user_acct_id')  # Get the user ID from the session

        try:
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 18 for SQL Server};'
                'SERVER=gymassisthost2.database.windows.net;'
                'DATABASE=gymassistdb;UID=admin_user;PWD=lamp4444!'
            )
            cursor = conn.cursor()

            # Debugging: Check the values before updating
            print(f"Updating gym_id: {gym_id} for user_acct_id: {user_acct_id}")

            # Update the user's gym_id in the database
            cursor.execute("UPDATE user_accounts SET gym_id = ? WHERE user_acct_id = ?", (gym_id, user_acct_id))
            rows_affected = cursor.rowcount
            conn.commit()

            # Debugging: Check if the update was successful
            if rows_affected > 0:
                messages.success(request, 'You have successfully joined the gym!')
                return redirect('staff_setup')  # Redirect to the home page
            else:
                messages.error(request, 'Update failed. Please check the user ID or gym ID.')

        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('staff_setup')  # Redirect back to the setup page

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # For GET request, fetch the list of gyms
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=gymassisthost2.database.windows.net;'
            'DATABASE=gymassistdb;UID=admin_user;PWD=lamp4444!'
        )
        cursor = conn.cursor()

        # Fetch gyms from the correct table name
        cursor.execute("SELECT gym_id, gym_name FROM gym")
        gyms = cursor.fetchall()

    except Exception as e:
        messages.error(request, f'An error occurred while fetching gyms: {str(e)}')
        gyms = []  # Set gyms to an empty list if there was an error

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render(request, 'staff_setup.html', {'gyms': gyms})


def goer_setup(request):
    logger = logging.getLogger('django')
    if request.method == 'POST':
        gym_id = request.POST.get('gym')  # Get the selected gym ID from the form
        user_acct_id = request.session.get('user_acct_id')  # Get the user ID from the session
        username = request.session.get('username')  # Assuming username is stored in the session
        
        if not username:
            logger.error(f"Username not found for user_acct_id: {user_acct_id}")
            messages.error(request, 'Username not found in session.')
            return redirect('goer_setup')  # Redirect back to the setup page if username is missing

        try:
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 18 for SQL Server};'
                'SERVER=gymassisthost2.database.windows.net;'
                'DATABASE=gymassistdb;UID=admin_user;PWD=lamp4444!'
            )
            cursor = conn.cursor()

            # Log the action before updating
            logger.info(f"User {username} (ID: {user_acct_id}) is attempting to join gym ID: {gym_id}.")

            # Update the user's gym_id in the database
            cursor.execute("UPDATE user_accounts SET gym_id = ? WHERE user_acct_id = ?", (gym_id, user_acct_id))
            rows_affected = cursor.rowcount
            conn.commit()

            if rows_affected > 0:
                # Log success: user has successfully joined a gym
                logger.info(f"User {username} (ID: {user_acct_id}) successfully joined gym ID: {gym_id} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                messages.success(request, 'You have successfully joined the gym!')
                return redirect('home')  # Redirect to the home page
            else:
                # Log error: update failed
                logger.error(f"Failed to update gym_id for user {username} (ID: {user_acct_id}). Gym ID: {gym_id} not found.")
                messages.error(request, 'Update failed. Please check the user ID or gym ID.')

        except Exception as e:
            # Log any exception that occurs during the process
            logger.error(f"Error occurred while user {username} (ID: {user_acct_id}) was joining gym ID: {gym_id}. Error: {str(e)}")
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('goer_setup')  # Redirect back to the setup page in case of error

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # For GET request, fetch the list of gyms
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=gymassisthost2.database.windows.net;'
            'DATABASE=gymassistdb;UID=admin_user;PWD=lamp4444!'
        )
        cursor = conn.cursor()

        # Fetch gyms from the correct table name
        cursor.execute("SELECT gym_id, gym_name FROM gym")
        gyms = cursor.fetchall()

    except Exception as e:
        logger.error(f"An error occurred while fetching gyms: {str(e)}")
        messages.error(request, f'An error occurred while fetching gyms: {str(e)}')
        gyms = []  # Set gyms to an empty list if there was an error

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render(request, 'goer_setup.html', {'gyms': gyms})



def home_owner(request):
    logger = logging.getLogger('django')
    user_acct_id = cache.get('user_id')
    print(f"user_acct_id: {user_acct_id}")  # Log user_acct_id for debugging

    if not user_acct_id:
        messages.error(request, 'You need to log in to access this page.')
        return redirect('login')

    # Connect to the database
    conn = None
    cursor = None
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=gymassisthost2.database.windows.net;'
            'DATABASE=gymassistdb;UID=admin_user;PWD=lamp4444!'
        )
        cursor = conn.cursor()

        # Fetch user information first
        cursor.execute("SELECT username, perm_id, gym_id, email FROM user_accounts WHERE user_acct_id = ?", (user_acct_id,))
        user = cursor.fetchone()

        if user:
            username, perm_id, user_gym_id, email = user  # Get the gym_id here
            print(f"Fetched user info: {username}, Gym ID: {user_gym_id}")

            # Check for the gym info associated with the owner
            cursor.execute("SELECT gym_name, gym_id, about_content, contact_content FROM gym WHERE owner_id = ?", (user_acct_id,))
            gyms = cursor.fetchall()

            # Initialize variables for gym content
            about_content = contact_content = None

            # Fetch monthly user counts and associated members
            gym_id = cache.get('gym_id')
            print(f"Cached gym_id: {gym_id}")
            monthly_user_counts = get_monthly_user_counts(gym_id)
            class_info = {}
            cursor.execute("SELECT username, first_name, last_name, email, user_acct_id FROM user_accounts WHERE gym_id = ? AND perm_id = ?", (gym_id, 4))
            members = cursor.fetchall()
            cursor.execute("SELECT username, first_name, last_name, email, user_acct_id FROM user_accounts WHERE gym_id = ? AND (perm_id = ? OR perm_id = ?)", (gym_id, 2, 3))
            employees = cursor.fetchall()
            cursor.execute("SELECT class_name, data_date, data_time FROM class WHERE gym_id = ?", (gym_id,))
            classes = cursor.fetchall()
            print("test7")
            for gym in gyms:
                gym_name, gym_id, about_content, contact_content = gym
                print(f"Gym ID: {gym_id}, About: {about_content}, Contact: {contact_content}")
            print("test6")
            # Handle POST request only after the necessary information is set
            if request.method == 'POST':
                print(request.POST)
                if 'gym_name' in request.POST:
                    gym_name = request.POST.get('gym_name')
                    cursor.execute("UPDATE gym SET gym_name = ? WHERE gym_id = ?", (gym_name, gym_id))
                    conn.commit()
                    return redirect('home_owner')
                if 'about_content' in request.POST:
                    about_content = request.POST.get('about_content')
                    cursor.execute("UPDATE gym SET about_content = ? WHERE gym_id = ?", (about_content, gym_id))
                    conn.commit()
                if 'contact_content' in request.POST:
                    contact_content = request.POST.get('contact_content') 
                    cursor.execute("UPDATE gym SET contact_content = ? WHERE gym_id = ?", (contact_content, gym_id))
                    conn.commit()
                
                cursor.execute("UPDATE user_accounts SET gym_id = ? WHERE user_acct_id = ?", (gym_id, user_acct_id))
                conn.commit()
                # Now handle gym content update (about_content and contact_content)
                about_content = request.POST.get('about_content')
                contact_content = request.POST.get('contact_content')

                if not gym_id or not about_content or not contact_content:
                    return redirect('home_owner')

                print("Updating the content:")
                print(f"About: {about_content}")
                print(f"Contact: {contact_content}")
                # Update the gym content with the newly provided values
                update_gym_info(gym_id, about_content, contact_content)
                
                return redirect('home_owner')  # Redirect to refresh the page

            # Pass necessary context to the template
            return render(request, 'home_owner.html', {
                'username': username,
                'perm_id': perm_id,
                'email': email,
                'userGymId': user_gym_id,  # Add userGymId to the context
                'members_info': members,
                'employee_info': employees,
                'class_info': classes,
                'monthly_user_counts': monthly_user_counts,
                'about_content': about_content,
                'contact_content': contact_content,
                'gyms': gyms,  # Pass gyms for editing
            })
        else:
            messages.error(request, 'User not found.')
            return redirect('login')

    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('login')

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



'''
def convert_user_to_owner(user_acct_id):
    try:
        # Connect to the database
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=gymassisthost2.database.windows.net;'
            'DATABASE=gymassistdb;UID=admin_user;PWD=lamp4444!'
        )
        cursor = conn.cursor()

        # Prepare to execute the stored procedure
        print('test1')
        cursor.execute("EXEC ConvertUserToOwner2 @user_acct_id = ?", (user_acct_id,))

        # Fetch the result (if needed)
        print('test2')
        new_owner_id = cursor.fetchone()
        
        if new_owner_id:
            return new_owner_id[0]  # Return the NewOwnerID
        else:
            return None  # No new owner ID returned

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

    finally:
        # Ensure both cursor and connection are closed safely
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Example usage
 '''

def home_staff(request):
    user_acct_id = cache.get('user_id')

    if not user_acct_id:
        messages.error(request, 'You need to log in to access this page.')
        return redirect('login')

    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=gymassisthost2.database.windows.net;'
            'DATABASE=gymassistdb;UID=admin_user;PWD=lamp4444!'
        )
        cursor = conn.cursor()

        # Fetch user info
        cursor.execute("SELECT username, perm_id, gym_id, first_name, last_name, email FROM user_accounts WHERE user_acct_id = ?", (user_acct_id,))
        user = cursor.fetchone()

        if user:
            username, perm_id, gym_id, first_name, last_name, email = user

            # Fetch gym name and about/contact content
            cursor.execute("SELECT gym_name, about_content, contact_content FROM gym WHERE gym_id = ?", (gym_id,))
            gym_info = cursor.fetchone()

            if gym_info:
                gym_name, about_content, contact_content = gym_info
            else:
                about_content = contact_content = None

            # Fetch members associated with the user's gym
            cursor.execute("SELECT username, first_name, last_name FROM user_accounts WHERE gym_id = ? AND perm_id = ?", (gym_id, 4))
            members = cursor.fetchall()

            # Pass the necessary context to the template
            return render(request, 'home_staff.html', {
                'username': username,
                'email': email,
                'perm_id': perm_id,
                'gym_info': gym_name,
                'about_content': about_content,
                'contact_content': contact_content,
                'members': members,
                'first_name': first_name,
                'last_name': last_name,
            })
        else:
            messages.error(request, 'User not found.')
            return redirect('login')

    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('login')

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()




def home_goer(request):
    user_acct_id = cache.get('user_id')
    print(user_acct_id) 
    
    if not user_acct_id:    
        messages.error(request, 'You need to log in to access this page.')
        return redirect('login')

    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=gymassisthost2.database.windows.net;'
            'DATABASE=gymassistdb;UID=admin_user;PWD=lamp4444!'
        )
        cursor = conn.cursor()

        # Fetch user info
        cursor.execute("SELECT username, perm_id, gym_id, email, first_name, last_name, user_acct_id FROM user_accounts WHERE user_acct_id = ?", (user_acct_id,))
        user = cursor.fetchone()

        if user:
            username, perm_id, gym_id, email, first_name, last_name, user_acct_id = user

            # Fetch gym name and about/contact content
            cursor.execute("SELECT gym_name, about_content, contact_content FROM gym WHERE gym_id = ?", (gym_id,))
            gym_info = cursor.fetchone()

            if gym_info:
                gym_name, about_content, contact_content = gym_info
            else:
                about_content = contact_content = None

            # Fetch workouts or other data if needed
            workouts = []  # This can be populated as needed

            # Pass the necessary context to the template
            return render(request, 'home_goer.html', {
                'username': username,
                'perm_id': perm_id,
                'gym_name': gym_name,
                'workouts': workouts,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'about_content': about_content,
                'contact_content': contact_content,
                'user_acct_id': user_acct_id,
            })
        else:
            messages.error(request, 'User not found.')
            return redirect('login')

    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('login')

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

            
        from django.http import JsonResponse
from django.db import connection

def get_classes(request):
    with connection.cursor() as cursor:
        cursor.execute("EXEC AddClass")  # Call the procedure to get the classes
        rows = cursor.fetchall()

    classes = []
    for row in rows:
        classes.append({
            'id': row[0],  # Assuming the first column is class_id
            'title': row[4],  # Assuming the fifth column is class_name
            'start': str(row[2]),  # Assuming the third column is data_date
            'end': str(row[2]),  # Use appropriate end date if available
            'time': str(row[5])  # Optional: class time if needed
        })

    return JsonResponse(classes, safe=False)

from django.views.decorators.csrf import csrf_exempt

import pyodbc
from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.db import connection

from django.shortcuts import render, redirect
from django.db import connection

#view user so can access owner id in add class.
def view_user(request):
    return render(request, 'add_class.html', {'user': request.user})

import uuid

def add_class(request):
    if request.method == 'POST':
        instructor_id = request.POST.get('instructor_id')
        data_date = request.POST.get('data_date')
        data_time = request.POST.get('data_time')
        class_name = request.POST.get('class_name')
        class_type = request.POST.get('class_type')
        price = request.POST.get('price')
        seats_available = request.POST.get('seats_available')
        gym_id = cache.get('gym_id')
      #  print(f"This is the Gym ID: {gym_id}")
        

        # Generating roster_id
        roster_id = str(uuid.uuid4().fields[-1])[:5]

        # Retrieving gym_id
        #gym_id = request.GET.get('gym_id')

        # Get the next class_id by finding the max and adding 1
        with connection.cursor() as cursor:
            cursor.execute("SELECT COALESCE(MAX(class_id), 0) + 1 FROM class")
            class_id = cursor.fetchone()[0]  # Fetch the next class_id
        

        # Call the stored procedure to add the class (without gym_id)
        with connection.cursor() as cursor:
            cursor.execute("""
                EXEC AddClass1 @class_id = %s, @instructor_id = %s, 
                @data_date = %s, @roster_id = %s, @class_name = %s, 
                @data_time = %s, @class_type = %s, @gym_id = %s, @price = %s, @seats_available = %s
            """, [class_id, instructor_id, data_date, roster_id, class_name, data_time, class_type, gym_id, price, seats_available])
    
        print('Class added successfully!')
        return redirect('home_owner')  # Redirect to a success page or home

    return render(request, 'add_class.html')   #  # Render the form on GET request

                

# views.pyjkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk


from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm



from django.http import JsonResponse


def get_classes(request):
    if request.method == 'GET':
        gym_id = cache.get("gym_id")  # Get gym ID from the request
        events = []
        if gym_id:
            try:
                conn = pyodbc.connect(
                'DRIVER={ODBC Driver 18 for SQL Server};'
                'SERVER=gymassisthost2.database.windows.net;'
                'DATABASE=gymassistdb;UID=admin_user;PWD=lamp4444!'
                )
        
                cursor = connection.cursor()
            # Fetch classes from the database based on gym_id
                query = """
                    SELECT class_name, data_date, data_time, class_id
                    FROM class
                    WHERE gym_id = %s
                """
                cursor.execute(query, [gym_id])
                sql_results = cursor.fetchall()

                
            # Convert SQL results to the format required by FullCalendar
                for event in sql_results:
                    class_name, data_date, data_time,class_id = event
                    events.append({
                        'title': class_name,
                        'start': f"{data_date}T{data_time}",  # Format for FullCalendar
                        'end': f"{data_date}T{data_time}",    # Adjust end time if needed
                        'id':class_id
                    })

                return JsonResponse(events, safe=False)
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
        else:
            return JsonResponse({'error': 'No gym_id provided'}, status=400)

def get_gymID(request):
    if request.method == 'GET':
        gym_id = request.GET.get('gym_id')
        if gym_id:
          return JsonResponse({'gym_id': gym_id})
        else:
            return JsonResponse({'error': 'No gym_id provided'}, status=400)
    else:
        return JsonResponse({'error': 'No gym_id provided'}, status=400)

def getClass(request):
    if request.method == 'GET':
        user_id = cache.get('user_id')
        gym_id = cache.get('gym_id')
        class_id = request.GET['class_id']
        # needed for pay_class
        request.session['class_id'] = class_id
       
        print(f"Testing getClass --> Gym ID: {gym_id}, Class ID: {class_id}")
        try:
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 18 for SQL Server};'
                'SERVER=gymassisthost2.database.windows.net;'
                'DATABASE=gymassistdb;UID=admin_user;PWD=lamp4444!'
                )
        
            cursor = conn.cursor()
           
            cursor.execute("SELECT class_id, instructor_id, data_date, roster, class_name, class_type, price, seats_available FROM class WHERE class_id = ?", (class_id))
            row = cursor.fetchone()
            print(row[0])
            cursor.execute("EXEC GetAccount @user_acct_id = ?", (row[1]))
            instructor = cursor.fetchone()
            print(instructor)
            instructorName = str(instructor[1]) + " " + str(instructor[2])
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    return render(request, 'class_view.html', {
                'class_id': row[0],
                'instructor_name':instructorName,
                'data_date': row[2],
                'roster_id': row[3],
                'class_name': row[4],
                'class_type': row[5],
                'price': row[6],
                'seats_available' : row[7],
                'user_id' : user_id
            })
def get_user_classes(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')  # Retrieve the user_id from the GET parameters
        if not user_id:
            return JsonResponse({'error': 'User ID is required'}, status=400)

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT class_id 
                    FROM User_class_register
                    WHERE user_acct_id = %s
                """, [user_id])
                
                # Fetch all class_ids from the result
                result = cursor.fetchall()
                class_ids = [row[0] for row in result]  # Extract class_id from each row

            return JsonResponse({'class_ids': class_ids})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)      


# disabling CSRF security for simplicity -- security issues MAKE SURE TO FIX THIS
#from django.views.decorators.csrf import csrf_exempt


from django import forms
import square
from square.client import Client
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)


# From Square: https://developer.squareup.com/explorer/square/payments-api/create-payment
#      also check: https://developer.squareup.com/forums/t/python-and-square-payment-form-in-windows/1218 

@csrf_exempt  # Remove this if your CSRF token is working correctly
def pay_class(request):
    if request.method == "POST":
        try:
            logger.debug(f'Request body: {request.body}')  # Log the raw request body
            
            # Parse JSON data
            data = json.loads(request.body)
            logger.debug(f'Parsed JSON data: {data}')  # Log parsed data

            # Retrieve the token from the parsed JSON
            token = data.get('token')
            if not token:
                logger.error('Token not provided in request')
                return JsonResponse({'success': False, 'message': 'Token not provided'}, status=400)

            # Payment logic 
            client = Client(
                access_token="EAAAl-QdxeZFdlyEpI398pNIRXIsD34v6jeN2DsHVq5LvzjhDjdsREj1gmu9ycbI",
                environment="sandbox"
            )

            # get payment token from frontend
            #data = json.loads(request.body)
            #token = data.get('token')

            if not token:
                return JsonResponse({'success': False, 'message': 'No payment token provided'}, status=400)

            # payment parameters

            result = client.payments.create_payment(
            body = {
                #creates unique key for each transaction
                "idempotency_key": str(uuid.uuid4()),
                # In future, replace  cnon:card-nonce-ok token received from HTML
                #           and get amount from db or cache
                "source_id": token, #"cnon:card-nonce-ok",
                "amount_money":{
                    "amount": 100,
                    "currency": "USD"
                },
                "autocomplete": True,
                "location_id": "LQRBC20NRTG0Y",
                #"accept_partial_authorization": False,
                #"external_details": {
                #"type": "' '",
                #"source": "' '"
            }
                
          #  }
            )
 
            logger.debug(f'Token received: {token}')
            
            # get class_id from session. Originally retrieved in getClass(request)
            class_id = request.session.get('class_id')

            # subtract seats_available
            if class_id:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        EXEC SubClassSeat @class_id = %s""",
                        [class_id]
                    )
            
            user_acct_id = cache.get('user_id')
            if not user_acct_id:
                print("Error: 'user_id' not found in cache.")
            if user_acct_id is None:
                print("Error: user_acct_id is None. Check if 'user_id' is set in cache.")
                # You can return an error response if needed
                return JsonResponse({'error': "User not found in cache."}, status=400)

            print(f"User acct id: {user_acct_id}")
            has_paid = 1
            register_id = str(uuid.uuid4().fields[-1])[:5]

            # update user_class_registration db
            if class_id and user_acct_id:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        EXEC AddClassRegister @register_id = %s, @user_acct_id = %s, @class_id = %s, @has_paid = %s""",
                        [register_id, user_acct_id, class_id, has_paid]
                    )
            
            return JsonResponse({
                'success': True,
                'message': 'Payment processed successfully!',
            })
            
        except json.JSONDecodeError:
            logger.error('Failed to decode JSON data')
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
        
        except Exception as e:
            logger.exception('An error occurred while processing the payment')
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    return render(request, "pay_class.html")
    # If it's not a POST request, return an error
    #return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
        
    

from django.http import Http404   

...
def member_details(request, user_acct_id):
    # Retrieve member details based on user_acct_id from the database
    conn = None
    cursor = None
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=gymassisthost2.database.windows.net;'
            'DATABASE=gymassistdb;UID=admin_user;PWD=lamp4444!'
        )
        cursor = conn.cursor()

        # Query to get member details by user_acct_id
        cursor.execute("SELECT username, first_name, last_name, email FROM user_accounts WHERE user_acct_id = ?", (user_acct_id,))
        member = cursor.fetchone()

        if member:
            username, first_name, last_name, email = member
            member_details = {
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'user_acct_id': user_acct_id,
                'email': email
            }
            return render(request, 'member_details.html', {'member': member_details})
        else:
            raise Http404("Member not found")
    
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_instructors(request):
    instructors = []
    conn = None
    cursor = None
    gym_id = cache.get('gym_id')
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=gymassisthost2.database.windows.net;'
            'DATABASE=gymassistdb;UID=admin_user;PWD=lamp4444!'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT user_acct_id, first_name, last_name FROM user_accounts WHERE gym_id = ? AND perm_id = ?",(gym_id, 2))
        instructors_in = cursor.fetchall()
        print(instructors_in)
        for instructor in instructors_in:
            user_acct_id, first_name, last_name = instructor
            print(user_acct_id)
            print(first_name)
            instructors.append({
                'id': user_acct_id,
                'name':first_name + " " + last_name
            })
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return JsonResponse(instructors, safe=False)
...

import json
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_monthly_user_counts(gym_id):
    SPLUNK_API_URL = 'https://localhost:8089/services/search/jobs/export'
    SPLUNK_USERNAME = 'admin_user'
    SPLUNK_PASSWORD = 'leeward99'
    print("testing whether or not get monthlu user count works")
    print(gym_id)
    splunk_query = f"""
    search index=* sourcetype="Gym_Assist_logs" gym_id={gym_id}
    | timechart span=1mon count
    | eval Month=strftime(_time, "%B %Y")
    | table Month count
    """
    params = {
        'search': splunk_query,
        'output_mode': 'json'
    }
    
    response = requests.get(SPLUNK_API_URL, auth=(SPLUNK_USERNAME, SPLUNK_PASSWORD), params=params, verify=False)
    
    monthly_counts = []
    
    # Split response by lines and parse each line as JSON
    for line in response.text.strip().splitlines():
        try:
            data = json.loads(line)
            result = data.get('result', {})
            month = result.get('Month')
            count = int(result.get('count', 0))
            monthly_counts.append({'month': month, 'count': count})

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
    
    if not monthly_counts:
        monthly_counts.append({'month': 'None', 'count': 0})
    return monthly_counts


def edit_gym_content(request, gym_id):
    logger = logging.getLogger('django')
    conn = None
    cursor = None
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=gymassisthost2.database.windows.net;'
            'DATABASE=gymassistdb;UID=admin_user;PWD=lamp4444!'
        )
        cursor = conn.cursor()

        if request.method == 'POST':
            about_content = request.POST.get('about_content')
            contact_content = request.POST.get('contact_content')

            if not about_content or not contact_content:
                messages.error(request, 'About or Contact content cannot be empty.')
                return redirect('home_owner')

            cursor.execute("""
                UPDATE gym
                SET about_content = ?, contact_content = ?
                WHERE gym_id = ?
            """, (about_content, contact_content, gym_id))
            conn.commit()

            messages.success(request, 'Successfully updated gym content!')
            return redirect('home_owner')

    except Exception as e:
        logger.error(f"Error in edit_gym_content: {str(e)}")
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('home_owner')

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def update_gym_info(gym_id, about_content, contact_content):
    print("testing...")
    try:
        # Validate inputs
        if not isinstance(gym_id, int):
            raise ValueError("gym_id must be an integer.")
        if not isinstance(about_content, str) or not isinstance(contact_content, str):
            raise ValueError("about_content and contact_content must be strings.")

        # Database connection
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=gymassisthost2.database.windows.net;'
            'DATABASE=gymassistdb;UID=admin_user;PWD=lamp4444!'
        )
        cursor = conn.cursor()

        # Execute update
        print("Updating gym ID {gym_id}...")
        cursor.execute(
            "UPDATE gym SET about_content = ?, contact_content = ? WHERE gym_id = ?",
            (about_content, contact_content, gym_id)
        )
        
        conn.commit()
        print("Rows affected: {cursor.rowcount}")
        
        if cursor.rowcount == 0:
            return "No gym found with the specified gym_id. No changes made."
        
        return "Gym information updated successfully."

    except pyodbc.Error as e:
        return f"Database error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
    finally:
        if 'conn' in locals() and conn:
            conn.close()
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import connection

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
    if request.method == 'POST':
        # Extract form data from request
        username = request.POST.get('username')
        email = request.POST.get('email')
        perm_id = request.POST.get('perm_id')  # Ensure you have this in your form
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
        try:
            # Call the stored procedure to add user credentials to the pass table
            cursor.execute(
                "EXEC AddUserToPass @user_acct_id=?, @password=?", 
                (user_acct_id, hashed_password)  # Use the hashed password
            )
        except Exception as e:
            messages.error(request, f'An error occurred while adding user to pass: {str(e)}')

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
     # Connect to the database
    conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=gymassisthost2.database.windows.net;DATABASE=gymassistdb;UID=admin_user;PWD=lamp4444!')
    cursor = conn.cursor()

    
    if request.method == 'POST':
        # Extract form data from request
        username = request.POST.get('username')
        email = request.POST.get('email')
        perm_id = 4  # Ensure you have this in your form
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

        # Call the stored procedure to insert the user
        print('inserting')
        cursor.execute(
            "EXEC AddAccount @user_acct_id=?, @perm_id=?, @username=?, @email=?, @gym_id=?, @firstname=?, @lastname=?, @datejoined=?, @password_val=?", 
            (user_acct_id, perm_id, username, email, gym_id, firstname, lastname, datetime.date.today(), hashed_password)
        
        )
        print('insert sucessful')
        try:
            # Call the stored procedure to add user credentials to the pass table
            cursor.execute(
                "EXEC AddUserToPass @user_acct_id=?, @password=?", 
                (user_acct_id, hashed_password)  # Use the hashed password
            )
        except Exception as e:
            messages.error(request, f'An error occurred while adding user to pass: {str(e)}')

        # Commit the transaction
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        # Redirect to login or render success message
        messages.success(request, 'Account registered successfully! Please log in.')
        return redirect('login')

    return render(request, 'add_member.html')

def add_employee(request):
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
        return redirect('login')

    return render(request, 'add_employee.html')


# Create your views here.
def index(request, *args, **kwargs):
    return render(request, 'frontend/index.html')



import pyodbc
from django.contrib.auth.hashers import check_password  # To compare hashed passwords
from django.contrib import messages
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

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
                user_acct_id, stored_password_hash, perm_id, gym_id = user
                cache.set('gym_id', gym_id, None)

                # Check if the provided password matches the stored hash
                if check_password(password, stored_password_hash):
                    # Password matches, log the user in
                    request.session['user_acct_id'] = user_acct_id  # Store user ID in session
                    messages.success(request, 'You are now logged in!')
                    
                    # Check if perm_id is null, if so redirect to role selection
                    if perm_id is None:  # If perm_id is null
                        return redirect('select_role')
                    
                    if perm_id == 1:
                        return redirect('home_owner')  # Redirect to owner's home page
                    elif perm_id == 2:
                        return redirect('home_staff')  # Redirect to staff's home page
                    elif perm_id == 3:
                        return redirect('home_goer')  # Redirect to goer's home pagee
                else:
                    # If password doesn't match
                    messages.error(request, 'Invalid username or password.')
                    return redirect('login')
            else:
                # If no user found with the given username
                messages.error(request, 'Invalid username or password.')
                return redirect('login')

        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('login')

        finally:
            # Ensure both cursor and connection are closed safely
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render(request, 'login.html')



def select_role(request):
    if request.method == 'POST':
        selected_role = request.POST.get('role')
        
        # Get the current logged-in user's ID from the session
        user_acct_id = request.session.get('user_acct_id')
        
        # Connect to the database
        try:
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 18 for SQL Server};'
                'SERVER=gymassisthost2.database.windows.net;'
                'DATABASE=gymassistdb;UID=admin_user;PWD=lamp4444!'
            )
            cursor = conn.cursor()

            # Set the perm_id based on the selected role
            if selected_role == 'owner':
                perm_id = 1
            elif selected_role == 'staff':
                perm_id = 2
            elif selected_role == 'goer':
                perm_id = 3
            else:
                perm_id = None

            if perm_id is not None:
                # Update the user's perm_id in the database
                cursor.execute("UPDATE user_accounts SET perm_id = ? WHERE user_acct_id = ?", (perm_id, user_acct_id))
                conn.commit()

                # Redirect based on role (e.g., owners go to gym setup, others go to home)
                if perm_id == 1:
                    return redirect('owner_setup')  # This should be another view where owners set up the gym
                if perm_id == 2:
                    return redirect('staff_setup')
                if perm_id == 3:
                    return redirect('goer_setup')
                else:
                    return redirect('home')

        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render(request, 'select_role.html')


def create_gym(gym_name):
    # Generate a new gym_id (ensure it meets your existing constraints)
    gym_id = random.randint(1, 1000000)  # Adjust range as necessary

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
        cursor.execute("INSERT INTO gym (gym_id, gym_name) VALUES (?, ?)", (gym_id, gym_name))
        conn.commit()

        print(f'Created gym: {gym_name} with ID: {gym_id}')
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

# gym db no longer holds owner_id
'''
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
        cursor.execute("UPDATE gym SET owner_id = ? WHERE gym_id = ?", (owner_id, gym_id))
        
        # Commit the transaction
        conn.commit()

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
'''

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
    if request.method == 'POST':
        gym_name = request.POST.get('gym_name')
        user_acct_id = request.session.get('user_acct_id')  # Get the user_acct_id from session
        username = request.POST.get('username')
        
        if user_acct_id is None:
            messages.error(request, 'User account ID not found in session.')
            return redirect('error_page')  # Redirect to an error page or handle appropriately

        # user_acct_id = get_user_acct_id_by_username(username)
        convert_user_to_owner(user_acct_id)
        # Step 1: Create a new gym and get the gym_id
        gym_id, gym_name_created = create_gym(gym_name)

        # Check if gym creation was successful
        if gym_id is None:
            messages.error(request, 'Failed to create gym. Please try again.')
            return redirect('error_page')  # Redirect to an error page if gym creation fails

        
        # Step 2: Set the owner_id for the created gym
        set_owner_for_gym(gym_id, user_acct_id)


        messages.success(request, 'Owner setup completed successfully!')

        
        return redirect('home_owner')  # Redirect to the owner's home page

    return render(request, 'owner_setup.html')  # Render the owner setup page for GET requests



def gym_selection(request):
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
                return redirect('home')  # Redirect to the home page
            else:
                messages.error(request, 'Update failed. Please check the user ID or gym ID.')

        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('goer_setup')  # Redirect back to the setup page

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
        messages.error(request, f'An error occurred while fetching gym: {str(e)}')
        gyms = []  # Set gyms to an empty list if there was an error

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render(request, 'goer_setup.html', {'gyms': gyms})



def home_owner(request):
    user_acct_id = request.session.get('user_acct_id')
    print(user_acct_id)
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

        # Handle gym name submission
        if request.method == 'POST':
            gym_name = request.POST.get('gym_name')  # Get the gym name from the form
            
            # Query to find the gym_id based on the provided gym_name
            cursor.execute("SELECT gym_id FROM gym WHERE gym_name = ?", (gym_name,))
            gym_id_row = cursor.fetchone()

            if gym_id_row is None:
                messages.error(request, 'Gym name not found. Please check the name and try again.')
                return redirect('home_owner')  # Redirect back to the home owner's page

            gym_id = gym_id_row[0]  # Extract the gym_id from the result

            # Update the user's gym_id in the database
            cursor.execute("UPDATE user_accounts SET gym_id = ? WHERE user_acct_id = ?", (gym_id, user_acct_id))
            rows_affected = cursor.rowcount
            conn.commit()

            # Check if the update was successful
            if rows_affected > 0:
                messages.success(request, 'Successfully updated gym information!')
            else:
                messages.error(request, 'Update failed. Please check the user ID or gym ID.')

            return redirect('home_owner')  # Redirect to refresh the page

        # Query to fetch the user information based on user_acct_id
        cursor.execute("SELECT username, perm_id, gym_id, email FROM user_accounts WHERE user_acct_id = ?", (user_acct_id,))
        user = cursor.fetchone()

        if user:
            username, perm_id, user_gym_id, email = user  # Get the gym_id here

            # Fetch gym information associated with the owner
            cursor.execute("SELECT gym_name, gym_id FROM gym WHERE owner_id = ?", (user_acct_id,))
            gyms = cursor.fetchall()

            # Print the gym_id(s) for debugging
            for gym in gyms:
                print(f"Gym ID: {gym[1]}")  # This should print each gym_id

            # Fetch members associated with each gym
            members_info = {}
            for gym in gyms:
                gym_name, gym_id = gym
                cursor.execute("SELECT user_acct_id, first_name, last_name FROM user_accounts WHERE gym_id = ?", (gym_id,))
                members = cursor.fetchall()
                members_info[gym_name] = members  # List of members for each gym

            return render(request, 'home_owner.html', {
                'username': username,
                'perm_id': perm_id,
                'email' : email,
                'userGymId': user_gym_id,  # Add userGymId to the context
                'gym_info': gyms,
                'members_info': members_info,
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
    user_acct_id = request.session.get('user_acct_id')
    

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

        # Update the query to fetch additional fields
        cursor.execute("SELECT username, perm_id, gym_id, first_name, last_name, email FROM user_accounts WHERE user_acct_id = ?", (user_acct_id,))
        user = cursor.fetchone()

        if user:
            username, perm_id, gym_id, first_name, last_name,email = user

            # Fetch gym information
            cursor.execute("SELECT gym_name FROM gym WHERE gym_id = ?", (gym_id,))
            gym_name = cursor.fetchone()

            # Fetch members associated with the user's gym
            cursor.execute("SELECT username FROM user_accounts WHERE gym_id = ? AND perm_id = 3", (gym_id,))  # Assuming perm_id = 3 corresponds to goers
            members = cursor.fetchall()
            members_list = [member[0] for member in members]  # Create a simple list of usernames

            return render(request, 'home_staff.html', {
                'username': username,
                'email': email,
                'perm_id': perm_id,
                'gym_info': gym_name,
                'members': members_list,
                'first_name': first_name,  # Pass the first name
                'last_name': last_name,    # Pass the last name
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
    user_acct_id = request.session.get('user_acct_id')
    user_acct_id = request.session.get('user_acct_id')

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

        # Update the query to fetch additional fields
        cursor.execute("SELECT username, perm_id, gym_id, email, first_name, last_name FROM user_accounts WHERE user_acct_id = ?", (user_acct_id,))
        user = cursor.fetchone()

        if user:
            username, perm_id, gym_id, email, first_name, last_name = user

            # Fetch gym information
            cursor.execute("SELECT gym_name FROM gym WHERE gym_id = ?", (gym_id,))
            gym_info = cursor.fetchone()

            gym_name = gym_info[0] if gym_info else "No gym found"
            workouts = []  # You can fetch workouts if needed

            return render(request, 'home_goer.html', {
                'username': username,
                'perm_id': perm_id,
                'gym_name': gym_name,
                'workouts': workouts,
                'email': email,
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

#view user so can access owner id in add class
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
    #    roster_id = request.POST.get('roster_id')
    #    gym_id = request.POST.get('gym_id')

        # Generating roster_id
        roster_id = str(uuid.uuid4().fields[-1])[:5]

        # Retrieving gym_id
        gym_id = request.GET.get('gym_id')

        # Get the next class_id by finding the max and adding 1
        with connection.cursor() as cursor:
            cursor.execute("SELECT COALESCE(MAX(class_id), 0) + 1 FROM class")
            class_id = cursor.fetchone()[0]  # Fetch the next class_id

        # Call the stored procedure to add the class (without gym_id)
        with connection.cursor() as cursor:
            cursor.execute("""
                EXEC AddClass1 @class_id = %s, @instructor_id = %s, 
                @data_date = %s, @roster_id = %s, @class_name = %s, 
                @data_time = %s, @class_type = %s, @gym_id = %s
            """, [class_id, instructor_id, data_date, roster_id, class_name, data_time, class_type, gym_id])
        
        print('Class added successfully!')
        return redirect('home_owner')  # Redirect to a success page or home

    return render(request, 'add_class.html')   #  # Render the form on GET request



            
            

# views.pyjkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk


from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm



from django.http import JsonResponse
import datetime

def get_classes(request):
    if request.method == 'GET':
        gym_id = request.GET.get('gym_id')  # Get gym ID from the request
        if gym_id:
            cursor = connection.cursor()
            # Fetch classes from the database based on gym_id
            query = """
                SELECT class_name, data_date, data_time
                FROM class
                WHERE gym_id = %s
            """
            cursor.execute(query, [gym_id])
            sql_results = cursor.fetchall()

            events = []
            # Convert SQL results to the format required by FullCalendar
            for event in sql_results:
                class_name, data_date, data_time = event
                events.append({
                    'title': class_name,
                    'start': f"{data_date}T{data_time}",  # Format for FullCalendar
                    'end': f"{data_date}T{data_time}"    # Adjust end time if needed
                })

            return JsonResponse(events, safe=False)
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
        



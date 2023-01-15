# =====importing libraries==============================================================================================
'''This is the section where you will import libraries'''
import datetime
import sys

# ====reg_user==========================================================================================================
def reg_user():
    '''code block to register user'''
    reg_flag = False
    username = input("Enter the new username that need to be registered:\t")

    # Check for duplicate and if found get a new username
    username = duplicate_user_check(username)

    # Get Password
    password = input("Enter the password:\t")
    confirm_password = input("Enter password again to confirm it:\t")
    if password == confirm_password:
        with open("user.txt", "a", encoding="utf-8") as user_data_file:
            user_data_file.write(f"\n{username}, {password}")
            reg_flag = True
    else:
        reg_flag = False

    return reg_flag

# ====Duplicate user check=============================================================================================
def duplicate_user_check(user):
    '''code block to check if username is duplicate during registration'''
    user_and_password_dict = get_user_db()
    while True:
        if user in user_and_password_dict.keys():
            #username already exist ask user to enter new one
            print("\nError: Username already in use please enter different Username")
            user = input("Enter the new username that need to be registered:\t")
        else:
            # Username is not in use so break out of the loop
            break
    return user

# ====get user and convert it as dictionary====
def get_user_db():
    '''get user and convert it as dictionary'''
    user_dict = {}
    with open("user.txt", "r", encoding="utf-8") as user_data_txt_file:
        user_and_pwd_list = user_data_txt_file.read().splitlines()
        #loop to each line and add user into dictionary
        for eachline in user_and_pwd_list:
            seperatorindex = eachline.find(", ")
            user_dict[eachline[0:seperatorindex]] = eachline[seperatorindex+2::]

    return user_dict

# ====get task and convert it as List==================================================================================
def get_task_db():
    '''get task and convert it as list'''
    task_2d_list = []
    with open("tasks.txt", "r", encoding="utf-8") as task_file:
        tasks_list = task_file.read().splitlines()

        # loop to each line and add user into list
        # data will be in below format ["TaskNo.", "User", "Title", "Date Assigned", "Due Date", "Completion Status", "Description"]
        for counter, task in enumerate(tasks_list):
            task_item_split = task.split(", ")
            task_item_split.insert(0, counter)
            task_item_split.append(task_item_split[3])
            task_item_split.pop(3)
            task_2d_list.append(task_item_split)
    return task_2d_list


def add_task():
    '''add new task into task manager'''
    task_user = input("Enter the username of the person whom the task is assigned to:\t")
    task_title = input("Enter the title of the task:\t")
    task_desc = input("Enter the description of the task:\t")
    task_duedate = input("Enter the due date of the task in dd mmm YYYY format:\t")
    current_date = datetime.date.today()
    # converting the current date to dd mmm YYYY format
    task_date = current_date.strftime("%d %b %Y")
    task_string = f"{task_user}, {task_title}, {task_desc}, {task_date}, {task_duedate}, No"
    with open("tasks.txt", "a", encoding="utf-8") as task_file:
        task_file.write(f"\n{task_string}")

    print(f"\nBelow task details added to task.txt successfully:\n {task_string}")
    print("\n**********************Task added successfully************************\n")


def view_all():
    '''In this block you will put code so that the program will read the task from task.txt file'''
    tasks_list_in_2d = get_task_db()
    # data will be in below format ["TaskNo.", "User", "Title", "Date Assigned", "Due Date", "Completion Status", "Descriptiom]

    for task_list in tasks_list_in_2d:
        formatprint(task_list)

def view_mine():
    '''In this block you will put code the that will read the task from task.txt file'''
    tasks_2d_data_list = get_task_db()
    # data will be in below format ["TaskNo.", "User", "Title", "Date Assigned", "Due Date", "Completion Status", "Descriptiom]
    task_found_flag = False
    task_file_update = False
    for task_list in tasks_2d_data_list: 
        if task_list[1] == username_input:
            task_found_flag = True
            formatprint(task_list)

    if task_found_flag is False:
        print(f"No Task assigned to user {username_input}")
    else:
        while True:
            print("\nEnter -1 avoid editing and goto previous menu:\t")
            task_number = input("Enter the task number you wish to edit:\t")
            row_number = int(task_number) - 1
            if int(task_number) == -1:
                print("\n**********************going back to previous menu**********************")
                break
            if tasks_2d_data_list[row_number][1] == username_input:
                if tasks_2d_data_list[row_number][5].lower() == "no":
                    print("Options available for your task\n" \
                          "\tOption 1 - mark the task as complete\n" \
                          "\tOption 2 - edit the task\n")
                    vm_option_selected = int(input("Please select operation 1, 2 :\t"))
                    if vm_option_selected == 1:
                        # User requesting for task to be marked as complete
                        tasks_2d_data_list[row_number][5] = "Yes"
                        task_file_update = True
                        print(f"\n**********************Task {task_number} is marked as completed sucessfully**********************")
                        break
                    elif vm_option_selected == 2:
                        # user requesting to edit the taks               
                        print("Below field can be edited in the task\n" \
                        "\tOption 1 - Edit the due date of the task\n" \
                        "\tOption 2 - Change the username and reassign it to another user\n")
                        vm_edit_option_selected = int(input("Please select operation 1, 2 :\t"))
                        if vm_edit_option_selected == 1:
                            # User requested for edting due date
                            new_due_date = input("Enter the new due date of the task in dd mmm YYYY format:\t")
                            tasks_2d_data_list[row_number][4] = new_due_date
                            task_file_update = True
                            print(f"\n**********************Task {task_number}'s due date is updated successfully**********************")
                            break
                        elif vm_edit_option_selected == 2:
                            # user requested for editing assigned to field
                            new_task_user = input("Enter the new username of the person whom the task should be assigned to:\t")
                            tasks_2d_data_list[row_number][1] = new_task_user
                            task_file_update = True
                            print(f"\n**********************Task {task_number}'s is reassigned to new user successfully**********************")
                            break
                        else:
                            print("No such option available going back to previous menu")
                    else:
                        print("No such option available going back to previous menu")

                else:    
                    print(f"Task {task_number} is already closed you no longer edit it or mark it as closed")
            else:
                print(f"Task ID {task_number} is not assigned to you to perform edit on it")

    if task_file_update is True:
        #if task data was editted updated it back to file
        file_data = ""
        for task_item_line in tasks_2d_data_list:
            task_item_line.pop(0) # remove the counter at the beginning
            task_item_line.insert(2, task_item_line[-1]) # change the postion of description to index as per the file
            task_item_line.pop(-1)
            single_task_full_data = ", ".join(str(v) for v in task_item_line)
            file_data = file_data + single_task_full_data + "\n"

        with open("tasks.txt", "w", encoding="utf-8") as task_file:
            task_file.write(f"{file_data.rstrip()}")

# ============Output in modulare format=============================================================
def formatprint(current_task_list):
    '''code to print the task in formated manner'''
    # forming fstring in required format for outputting
    # Reference: https://www.geeksforgeeks.org/string-alignment-in-python-f-string/
    task_line = f"{'Task:':<20s}{current_task_list[2]}"
    assigneduser_line = f"{'Assigned to:':<20s}{current_task_list[1]}"
    dateassigned_line = f"{'Date assigned:':<20s}{current_task_list[3]}"
    duedate_line = f"{'Due date:':<20s}{current_task_list[4]}"
    taskcompleted_line = f"{'Task completed?:':<20s}{current_task_list[5]}"
    taskdescription_line = f"{'Task description?:':<20s}{current_task_list[6]}"

    #Print each Task details
    print(f"-------------------------Task {current_task_list[0]+1}-----------------------")
    print (f"""{task_line}
{assigneduser_line}
{dateassigned_line}
{duedate_line}
{taskcompleted_line}
{taskdescription_line}""") #using multiline to avoid C0301
    print(f"----------------------End of Task {current_task_list[0]+1}--------------------\n")

# ================Create task_overview.txt====================================================
def create_task_overview():
    '''In this block you will put code that will create task_overview.txt file'''
    tasks_2dim_list = get_task_db()
    task_overview_list = []
    no_of_completed_tasks = 0
    no_of_uncompleted_tasks = 0
    no_of_uncompleted_overdue_tasks = 0
    for i in range(len(tasks_2dim_list)):
        if tasks_2dim_list[i][5].lower() == "yes":
            # task that is completed
            no_of_completed_tasks += 1
        if tasks_2dim_list[i][5].lower() == "no":
            # task that is not completed
            no_of_uncompleted_tasks += 1
            due_date = datetime.datetime.strptime(tasks_2dim_list[i][4], "%d %b %Y").date()
            current_date = datetime.datetime.today().date()
            if due_date > current_date:
                # tasks that haven't been completed and that are overdue
                no_of_uncompleted_overdue_tasks += 1

        percentage_of_incomplete_task = no_of_uncompleted_tasks*100/len(tasks_2dim_list)
        percentage_of_overdue_task = no_of_uncompleted_overdue_tasks*100/len(tasks_2dim_list)

    task_overview_list.append(f"The total number of tasks that have been generated and tracked using the task_manager.py: {len(tasks_2dim_list)}\n")
    task_overview_list.append(f"The total number of completed tasks: {no_of_completed_tasks}\n")
    task_overview_list.append(f"The total number of uncompleted tasks: {no_of_uncompleted_tasks}\n")
    task_overview_list.append(f"The total number of tasks that haven't been completed and that are overdue: {no_of_uncompleted_overdue_tasks}\n")
    task_overview_list.append(f"The percentage of tasks that are incomplete: {round(percentage_of_incomplete_task, 2)}%\n")
    task_overview_list.append(f"The percentage of tasks that are overdue: {round(percentage_of_overdue_task, 2)}%\n")

    with open("task_overview.txt", "w", encoding="utf-8") as task_overview:
        task_overview.writelines(task_overview_list)

# ================Create user_overview.txt======================================================
def create_user_overview():
    '''In this block you will put code that will create user_overview.txt file'''
    user_db = get_user_db()
    tasks_db = get_task_db()
    each_user_data = []
    for key in user_db:
        no_of_tasks_of_user = 0
        no_of_tasks_completed_user = 0
        no_of_tasks_uncompleted_user = 0
        no_of_uncompleted_overdue_user = 0
        for task_idx in range(len(tasks_db)):
            if tasks_db[task_idx][1] == key:
                no_of_tasks_of_user += 1
                if tasks_db[task_idx][5].lower() == "yes":
                    no_of_tasks_completed_user += 1
                if tasks_db[task_idx][5].lower() == "no":
                    no_of_tasks_uncompleted_user += 1
                    due_date = datetime.datetime.strptime(tasks_db[task_idx][4], "%d %b %Y").date()
                    current_date = datetime.datetime.today().date()
                    if due_date > current_date:
                        # tasks that haven't been completed and that are overdue for current user
                        no_of_uncompleted_overdue_user += 1

        each_user_data.append(f"The total number of tasks assigned to {key}: {no_of_tasks_of_user}\n")
        each_user_data.append(f"The percentage of the total number of tasks that have been assigned to {key}: {round(no_of_tasks_of_user*100/len(tasks_db), 2)}%\n")
        each_user_data.append(f"The percentage of the tasks assigned to {key} that have been completed: {round(no_of_tasks_completed_user*100/len(tasks_db), 2)}%\n")
        each_user_data.append(f"The percentage of the tasks assigned to {key} that must still be completed: {round(no_of_tasks_uncompleted_user*100/len(tasks_db), 2)}%\n")
        each_user_data.append(f"The percentage of the tasks assigned to {key} that have not yet been completed and are overdue: "
                              f"{round(no_of_uncompleted_overdue_user*100/len(tasks_db), 2)}%\n")
        each_user_data.append(f"==================================End of the {key} data===============================================\n")
        with open("user_overview.txt", "w", encoding="utf-8") as user_overview:
            user_overview.writelines(each_user_data)


# ====Login Section================================================================
while True:
    username_input = input("Enter your Task_Manager.py program username:\t")
    password_input = input("Enter your password:\t")

    # we are combining the username followed by a comma, a space
    # and then the password to make string in smae format as user.txt lines
    username_and_password_combo_string = f"{username_input}, {password_input}"
    login_flag = False

    with open("user.txt", "r", encoding="utf-8") as user_file:
        user_and_password_list = user_file.read().splitlines()
        # using read().splitlines() instead of readlines to remove newline char at end of each line
        while True:
            if username_and_password_combo_string in user_and_password_list:
                print("\n**************Logined successfully***************")
                login_flag = True
                break  #this will break the loop if username and password combo is inside

            print("\n**************Incorrect Username and Password**************")
            username_input = input("Enter your Task_Manager.py program username:\t")
            password_input = input("Enter your password:\t")
            username_and_password_combo_string = f"{username_input}, {password_input}"


    if login_flag:
        break #this will break the loop from asking username and password again if login is sucess

while True:
    # presenting the menu to the user and
    # making sure that the user input is coneverted to lower case.
    if username_input == "admin":
        menu = input('''\nSelect one of the following Options below:
        r - Registering a user
        a - Adding a task
        va - View all tasks
        vm - view my task
        gr - generate reports
        ds - display statistics
        e - Exit
        : ''').lower()
    else:
        menu = input('''\nSelect one of the following Options below:
        a - Adding a task
        va - View all tasks
        vm - view my task
        e - Exit
        : ''').lower()


    if menu == 'r' and username_input == "admin":
        # In this block you will write code to ad`d a new user to the user.txt file
        if reg_user() is False:
            print("\nError: Password and Confirm password mismatched\n")
        else:
            print("\nSucess: Added new user to the user.txt file\n")

    elif menu == 'a':        
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == 'ds':
        create_task_overview()
        create_user_overview()
        # generating file incase user has done update before asking statistics
        # or he is trying ask stats before generating file
        with open("task_overview.txt", "r", encoding="utf-8") as task_stat_file:
            tasks = task_stat_file.readlines()
            print("**********************Task Statistics**********************")
            task_overview_data = [print(eachline.rstrip()) for eachline in tasks]
            print("*******************End of Task Statistics*******************\n")

        with open("user_overview.txt", "r", encoding="utf-8") as user_stat_file:
            users = user_stat_file.readlines()
            print("**********************User Statistics**********************")
            user_overview_data = [print(eachline.rstrip()) for eachline in users]
            print("*******************End of User Statistics*******************")

    elif menu == 'gr':
        create_task_overview()
        create_user_overview()
        print("*****************task_overview.txt and user_overview.txt generated*****************")

    elif menu == 'e':
        print('Goodbye!!!')
        sys.exit()

    else:
        print("\nYou have made a wrong choice, Please Try again\n")

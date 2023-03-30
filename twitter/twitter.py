from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:

    def __init__(self):
        self.current_user = None
    """
    The menu to print once a user has logged in
    """
    def print_menu(self):
        print("\nPlease select a menu option:")
        print("1. View Feed")
        print("2. View My Tweets")
        print("3. Search by Tag")
        print("4. Search by User")
        print("5. Tweet")
        print("6. Follow")
        print("7. Unfollow")
        print("0. Logout")
    
    """
    Prints the provided list of tweets.
    """
    def print_tweets(self, tweets):
        for tweet in tweets:
            print("==============================")
            print(tweet)
        print("==============================")

    """
    Should be run at the end of the program
    """
    def end(self):
        print("Thanks for visiting!")
        db_session.remove()
    
    """
    Registers a new user. The user
    is guaranteed to be logged in after this function.
    """
    def register_user(self):
        username = input("What will your twitter handle be? \n")
        user = db_session.query(User).where(User.username == username).first()
        while user != None:
                print("That username is already taken. Try Again")
                username = input("What will your twitter handle be? \n")
                user = db_session.query(User).where(User.username == username).first()
        password = input("Enter your password: \n")
        confirm_password = input("Re-enter your password: \n")
        while password != confirm_password:
            print("Passwords don't match. Try again.")
            password = input("Enter your password: \n")
            confirm_password = input("Re-enter your password: \n")
        db_session.add(User(username = username, password = password))
        db_session.commit()
        print("\n Welcome " + username + "!")
    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        while True:
            username = input("Username: ")
            password = input("Password: ")
            user = db_session.query(User).where(username == User.username, password == User.password).first()
            if user != None:
                self.current_user = user
                print("Login successful!")
                break
            else:
                print("Invalid username or password.")

    
    def logout(self):
        self.current_user = None

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        print("Please select a Menu Option")
        print("1. Login")
        print("2. Register User")
        print("0. Exit")
        choice = int(input(""))
        if choice == 1:
            self.login()
        elif choice == 2:
            self.register_user()
        elif choice == 0:
            self.end()



    def follow(self):
        follow = input("Who would you like to follow?")
        user = db_session.query(User).where(follow == User.username).first()
        if user != None:
            #TODO query to check if person already follows them
            check_following = db_session.query(Follower).where(follower_id = user.id)
            if check_following != None:
                print("You already follow " + follow)
        else:
            follower = Follower(follower_id = user.id)
            db_session.add(follower)
            db_session.commit()
            print("You are now following " + follow + "!")


    def unfollow(self):
        unfollow = input("Who would you like to unfollow?")
        user = db_session.query(User).where(unfollow == User.username).first()
        if user != None:
            #TODO check if current user is following them
            follower = db_session.query(Follower).where(follower_id = user.id).first()
            if follower != None:
                #TODO remove follower
                db_session.commit()
                print("You are no longer following " + unfollow)
            else:
                print("You don't follow " + unfollow)


    def tweet(self):
        content = input("Create Tweet: ")
        tags = input("Enter your tags separated by spaces: ")
        timestamp = datetime.now()
        tweet = Tweet(content = content, timestamp = timestamp, username = self.current_user.username, tags = tags)
        db_session.add(tweet)
        db_session.commit()
    
    def view_my_tweets(self):
        user_tweets = db_session.query(Tweet).where(username = self.current_user.username).all()
        self.print_tweets(user_tweets)
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        pass

    def search_by_user(self):
        pass

    def search_by_tag(self):
        pass

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()
        while self.current_user != None:
            self.print_menu()
            option = int(input(""))

            if option == 1:
                self.view_feed()
            elif option == 2:
                self.view_my_tweets()
            elif option == 3:
                self.search_by_tag()
            elif option == 4:
                self.search_by_user()
            elif option == 5:
                self.tweet()
            elif option == 6:
                self.follow()
            elif option == 7:
                self.unfollow()
            else:
                self.logout()
            
            self.end()

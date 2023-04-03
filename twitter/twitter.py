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
        user = db_session.query(User).where(User.username == follow).first()
        if user in self.current_user.following:
            print("You already follow " + follow)
        else:
            follower = Follower(follower_id = self.current_user.username, following_id = user.username)
            db_session.add(follower)
            db_session.commit()
            print("You are now following " + follow + "!")
        
    def unfollow(self):
        unfollow = input("Who would you like to unfollow?")
        user = db_session.query(User).where(unfollow == User.username).first()
        if user in self.current_user.following:
                #remove follower
                following = db_session.query(Follower).filter_by(follower_id = self.current_user.username, following_id = user.username).first()
                db_session.delete(following)
                db_session.commit()
                print("You are no longer following " + unfollow)
        else:
            print("You don't follow " + unfollow)


    def tweet(self):
        content = input("Create Tweet: ")
        tag_strings = input("Enter your tags separated by spaces: ").split()
        tags = []
        for tag in tag_strings:
            #create tags object 
            tag = Tag(content = tag)
            db_session.add(tag)
            tags.append(tag)

        timestamp = datetime.now()
        tweet = Tweet(content = content, timestamp = timestamp, username = self.current_user.username, tags = tags)
        db_session.add(tweet)
        db_session.commit()
    
    def view_my_tweets(self):
        user_tweets = db_session.query(Tweet).where(Tweet.username == self.current_user.username).all()
        self.print_tweets(user_tweets)
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        tweets = []
        for following in self.current_user.following:
            user_tweets = db_session.query(Tweet).where(Tweet.username == following.username).order_by(Tweet.timestamp.desc()).limit(5)
            tweets.extend(user_tweets)
        #put tweets in order
        tweets.sort(reverse=True, key=lambda tweet: tweet.timestamp)
        self.print_tweets(tweets)

    def search_by_user(self):
        username = input("Enter username to search for: ")
        user = db_session.query(User).where(User.username == username).first()
        if user == None:
            print("There is no user by that name")
        else:
            user_tweets = db_session.query(Tweet).where(Tweet.username == username).all()
            self.print_tweets(user_tweets)

    def search_by_tag(self):
        tag = input("Enter tag to search for: ")
        tag = db_session.query(Tag).filter(Tag.content == tag).first()
        if tag != None:
            tweets_with_tag = db_session.query(Tweet).join(TweetTag).filter(TweetTag.tag_id == tag.id).all()    
            self.print_tweets(tweets_with_tag)
        else:
            print("There is no tag by that name")

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

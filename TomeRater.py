## Program name: TomerRater
## Program purpose: A book rating program.
## Developer: Donna Walker 09.17.18

## Define the User Class
class User(object):
    def __init__(self, name, email):
        self.name = str(name).strip().title()
        self.email = str(email).lower()
        self.books = {}

    ##Make User object hashable
    def __hash__(self):
        return hash((self.name, self.email))

    ## Display the user's email address
    def get_email(self):
        return "The email address associated to this account is {email}.".format(email=self.email)

    ## Change the user's email address
    def change_email(self, address):
        ## check for valid email format. return error if ill formed
        if "@" in address:
            address_components = address.split('.')
            tld = "." + address_components[-1]
            ## Check for common top level domains
            if tld not in top20tlds:
                str_tlds = ' '.join(top20tlds)
                print("The top-level domain (i.e. .com, .edu, .net) you provided is not in our list. Please enter an email address using any of these top-level domains: " + str_tlds)
                return
            else:
                ## Email address formatted properly
                old_email = self.email
                self.email = address.strip()
                print("The email address has been changed from {old_email} to {new_email}).".format(old_email=old_email, new_email=address))
                return
        else:
            return 'The address you provided, {address}, is missing the "@" symbol. Please enter a valid email address.'.format(address=address)

    ## Display basic user information (name, email address, number of books rated
    def __repr__(self):
        rtn_str=["User: "+self.name, "Email: "+self.email, "Books read: "+str(len(self.books))]
        return "'\r'".join(rtn_str)
        
    ## Check for duplicate user
    def __eq__(self, other_user):
        return self.name == other_user.name

    ##Add user's book rating to book dict
    def read_book(self,book,rating=None):
        self.books[book] = rating
        return

    ##Get average book rating per user
    def get_average_rating(self):
        total_ratings = 0
        for book, rate in self.books.items():
            total_ratings += rate
        return total_ratings / len(self.books)

## Define the Book Class
class Book:
    def __init__(self, title, isbn):
        self.title = title.strip().title()
        self.isbn = isbn
        self.ratings = []

    ## Display book title
    def get_title(self):
        return self.title

    ##Display book isbn
    def get_isbn(self):
        return self.isbn

    ##Update book isbn. validate new isbn before changing
    def set_isbn(self, newisbn):
        ## Check that newisbn is an integer
        if type(newisbn) != int:
            print("ISBNs must be numeric values only. Try again")
            return

        ##newisbn must be either the old 10 digit format or the new 13 digit EAN format
        elif len(str(newisbn)) != 10 and len(str(newisbn)) != 13:
                print("ISBN {isbn} is not the correct number of digits. Must be either 10 or 13 digits. Try again. ".format(isbn=newisbn))
                return
        else:
            ## 13 digit EAN isbns must begin with 978
            if len(str(newisbn)) == 13 and str(newisbn)[0:3] != '978':
                print("ISBN {isbn} should have a 978 prefix. Try again. ".format(isbn=newisbn))
                return
        ##newisbn passed validation now update book isbn
        old_isbn = self.isbn
        self.isbn = newisbn
        print("ISBN for {title} changed from {old_isbn} to {newisbn}.".format(title=self.title,old_isbn=old_isbn,newisbn=newisbn))
        return

    ##Add user rating. validate input is within 0-4 range
    def add_rating(self,rating):
        if type(rating) == int:
            if  rating < 0 or rating > 4:
                print("Invalid Rating")
                return
            else:
                self.ratings.append(rating)
        else:
            self.ratings.append(None)
        return

    ##Check for duplicate Book
    def __eq__(self, other):
        return self.title == other.title

    ##Get Book's average rating
    def get_average_rating(self):
        total_book_rating = 0
        for rate in self.ratings:
            if type(rate) == int:
                total_book_rating += rate

        return total_book_rating / len(self.ratings)

    ##Make Book object hashable
    def __hash__(self):
        return hash((self.title, self.isbn))


##Define Fiction Class. inherit from parent Book class.
class Fiction(Book):
    def __init__(self,title, author, isbn):
        super().__init__(title, isbn)
        self.author = str(author).strip().title()

    ##Display book author
    def get_author(self):
        return self.author

    ##Display basic book information (title, author)
    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)


##Define Non_Fiction Class. inherit from parent Book class.
class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = str(subject).strip().title()
        self.level = str(level).strip().lower()

    ##Display book subject
    def get_subject(self):
        return self.subject

    ##Display book level
    def get_level(self):
        return self.level

    ##Disply basic book info (title, level, subject)
    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)


##Define TomeRater Class
class TomeRater:
    def __init__(self):
        self.users = {}
        self.books = {}

    ##Create a book
    def create_book(self, title, isbn):
        new_book = Book(title, isbn)
        return new_book
    
    ##Create a novel
    def create_novel(self, title, author, isbn):
        new_novel = Fiction(title, author, isbn)
        return new_novel

    ##Create a non fiction book
    def create_non_fiction(self, title, subject, level, isbn):
        new_non_fiction = Non_Fiction(title, subject, level, isbn)
        return new_non_fiction

    ## Add book rating to user
    def add_book_to_user(self, book, email, rating=None):
        try:
            self.users.get(email)
            User.read_book(self, book, rating)
            Book.add_rating(book, rating)
            if book in self.books:
                if self.books[book] == None:
                    self.books[book] = 0
                self.books[book] += 1
            else:
                self.books[book] = 1
        except KeyError:
            print('"No user with email {email}!"'.format(email=email))

        return

    ## Link book to user
    def add_user(self, name, email, user_books=None):
        new_user = User(name, email)
        self.users[email] = name
        if user_books:
            for xbook in user_books:
                #print(xbook)
                self.add_book_to_user(xbook,email)
        return

    ##Print books in catalog
    def print_catalog(self):
        for xbook in self.books.keys():
            print(xbook)
        return

    ##Print users
    def print_users(self):
        for xemail, xuser in self.users.items():
            print(xuser)
        return

    ##Print the most read book
    ##Create a dictionary of read count and books list key:pair to group books
    ## with count then display the highest count and the books associated
    def most_read_book(self):
        most_read = ''
        read_count = 0
        read_dict = {}
        for xbook, xrate in self.books.items():
            ##Check if read count is in the read_dict keys. If found then
            ## check if book is in books list assoicated to the read count.
            ##If the books is not in the list then add it.
            if xrate in read_dict.keys():
                books_list = read_dict[xrate]
                if xbook not in books_list:
                    books_list.append('"' + str(xbook) + '"')
                    read_dict[xrate] = books_list
            else:
                read_dict[xrate] = ['"' + str(xbook) + '"']

        sorted_read = sorted(read_dict, reverse=True)
        return read_dict[sorted_read[0]]

    ##Get the highest rated book
    def highest_rated_book(self):
        book_name = ''
        high_rate = 0
        for xbook in self.books.keys():
            avg_rate = Book.get_average_rating(xbook)
            if avg_rate > high_rate:
                book_name = xbook
                high_rate = avg_rate
        return book_name

    ##Get most positive user
    def most_positive_user(self):
        user_name = ''
        high_rate = 0
        for xemail, xuser in self.users.items():
            avg_rate = User.get_average_rating(self)
            if avg_rate > high_rate:
                user_name = xuser
                high_rate = avg_rate
        return user_name
        

top20tlds=['.com', '.org', '.edu', '.gov', '.uk', '.net', '.ca', '.de', '.jp', '.fr', '.au', '.us', '.ru', '.ch', '.it', '.nl', '.se', '.no', '.es', '.mil', '.net']


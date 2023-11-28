
import datetime
import json

class Student:
    def __init__(self, name, id_no, stream):
        self.name = name
        self.id_no = id_no
        self.stream = stream
        self.books_issued = []

class Book:
    def __init__(self, title, author, quantity):
        self.title = title
        self.author = author
        self.quantity = quantity
        self.available = quantity

class Transaction:
    def __init__(self, book_title, student_id):
        self.book_title = book_title
        self.student_id = student_id
        self.issue_date = datetime.datetime.now()
        self.return_date = None
        self.fine = 0

class LibraryManagement:
    def __init__(self):
        self.students = {}
        self.books = {}
        self.transactions = []

    def load_data(self):
        # Load students' data from file
        with open("students.json", "r") as file:
            students_data = json.load(file)
            for student_id, student_info in students_data.items():
                self.students[int(student_id)] = Student(student_info['name'], student_info['id_no'], student_info['stream'])

        # Load books' data from file
        with open("books.json", "r") as file:
            books_data = json.load(file)
            for book_title, book_info in books_data.items():
                self.books[book_title] = Book(book_title, book_info['author'], book_info['quantity'])

        # Load transactions' data from file
        with open("transactions.json", "r") as file:
            transactions_data = json.load(file)
            for transaction_info in transactions_data:
                transaction = Transaction(transaction_info['book_title'], transaction_info['student_id'])
                transaction.issue_date = datetime.datetime.strptime(transaction_info['issue_date'], '%Y-%m-%d %H:%M:%S')
                transaction.return_date = datetime.datetime.strptime(transaction_info['return_date'], '%Y-%m-%d %H:%M:%S') if transaction_info['return_date'] else None
                transaction.fine = transaction_info['fine']
                self.transactions.append(transaction)

    def save_data(self):
        # Save students' data to file
        students_data = {str(student_id): {'name': student.name, 'id_no': student.id_no, 'stream': student.stream} for student_id, student in self.students.items()}
        with open("students.json", "w") as file:
            json.dump(students_data, file, indent=4)

        # Save books' data to file
        books_data = {book.title: {'author': book.author, 'quantity': book.quantity} for book in self.books.values()}
        with open("books.json", "w") as file:
            json.dump(books_data, file, indent=4)

        # Save transactions' data to file
        transactions_data = []
        for transaction in self.transactions:
            transaction_info = {
                'book_title': transaction.book_title,
                'student_id': transaction.student_id,
                'issue_date': transaction.issue_date.strftime('%Y-%m-%d %H:%M:%S'),
                'return_date': transaction.return_date.strftime('%Y-%m-%d %H:%M:%S') if transaction.return_date else None,
                'fine': transaction.fine
            }
            transactions_data.append(transaction_info)
        with open("transactions.json", "w") as file:
            json.dump(transactions_data, file, indent=4)

    def add_student(self, name, id_no, stream):
        if id_no not in self.students:
            self.students[id_no] = Student(name, id_no, stream)
            print("Student added successfully!")
        else:
            print("Student already exists!")

    def add_book(self, title, author, quantity):
        if title not in self.books:
            self.books[title] = Book(title, author, quantity)
            print("Book added successfully!")
        else:
            print("Book already exists!")

    def issue_book(self, title, student_id):
        if title in self.books and student_id in self.students:
            book = self.books[title]
            student = self.students[student_id]
            if book.available > 0 and len(student.books_issued) < 2:
                book.available -= 1
                self.transactions.append(Transaction(title, student_id))
                student.books_issued.append(title)
                print("Book issued successfully!")
            else:
                print("Book not available or limit reached!")
        else:
            print("Book or student not found!")

    def return_book(self, title, student_id):
        for transaction in self.transactions:
            if transaction.book_title == title and transaction.student_id == student_id and not transaction.return_date:
                transaction.return_date = datetime.datetime.now()
                return_date = transaction.return_date
                issue_date = transaction.issue_date
                days_difference = (return_date - issue_date).days
                if days_difference > 7:
                    transaction.fine = (days_difference - 7) * 5  # Charging 5 Rs per day after the 7-day limit
                self.books[title].available += 1
                self.students[student_id].books_issued.remove(title)
                print("Book returned successfully!")
                return

        print("Book or student not found or book already returned!")

    # Other methods for updating, deleting users, books, viewing history, fines, etc.

if __name__ == "__main__":
    library = LibraryManagement()
    library.load_data()

    while True:
        print("\n.....................................")
        print("1. Add Student.")
        print("2. Add Book.")
        print("3. Issue Book.")
        print("4. Return Book.")
        print("5. Save and Exit.")
        print("\n.....................................")

        choice = int(input("\nEnter Your choice: "))

        if choice == 1:
            name = input("Enter name: ")
            id_no = int(input("Enter ID: "))
            stream = input("Enter stream: ")
            library.add_student(name, id_no, stream)
        elif choice == 2:
            title = input("Enter title: ")
            author = input("Enter author: ")
            quantity = int(input("Enter quantity: "))
            library.add_book(title, author, quantity)
        elif choice == 3:
            title = input("Enter book title: ")
            student_id = int(input("Enter student ID: "))
            library.issue_book(title, student_id)
        elif choice == 4:
            title = input("Enter book title: ")
            student_id = int(input("Enter student ID: "))
            library.return_book(title, student_id)
        elif choice == 5:
            library.save_data()
            break

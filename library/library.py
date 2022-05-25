# make a library system to track books and check in/out 


available_books = ["book01", "book02", "book03", "book04", "book05", "book06", "book07", "book08", "book09", "book10"]

checked_out_books = []
invalidBooks = []
validBooks = []


def can_be_checked_out(books):
	return books in available_books

def can_be_checked_in(books):
	return books not in available_books

#def book_is_invalid(books):
	#return books not in available_books and checked_out_books

def book_is_invalid(books):
	if books not in available_books and books not in checked_out_books:
		return books

def books_are_valid(books):
	return books not in invalidBooks


desired_books = ["book01", "book08"]
returning_books = ["book01", "book11"]

#returning_books = ["book01"]


def check_out_books(books):
	global checked_out_books
	global available_books
	# check to see if the books are available and add to list if they are
	receivedBooks = list(filter(can_be_checked_out, books))
	# if they are...
	# remove available books from available_books
	# add same books to checked_out_books
	checked_out_books = checked_out_books + receivedBooks
	# if they aren't available, say so
	for book in books:
		if book in available_books:
			available_books.remove(book)
			print("You have checked out: ", book)
			checked_out_books.sort()
		else:
			print("Sorry, this book is not in our system: ", book)


# MY CHECK-IN METHOD

def check_in_books(books):
	global checked_out_books
	global available_books
	global invalidBooks
	global validBooks

	returningBooks = list(filter(can_be_checked_in, books))
	# need list of valid returning books

	invalidBooks = list(filter(book_is_invalid, returningBooks))

	validBooks = list(filter(books_are_valid, returningBooks))

	#available_books = available_books + validBooks


	for book in returningBooks:
		if book in checked_out_books:
			checked_out_books.remove(book)
			available_books = available_books + validBooks
			print("You have returned: ", book)
			available_books.sort()
		else:
			print("Sorry, this book is not able to be returned: ", book)






# JOHN'S CHECK-IN METHOD
"""
def check_in_books(books):
	global checked_out_books
	global available_books

	# Can't check in books that aren't checked out; these books are invalid
	invalid_books = list(filter(lambda b: b not in checked_out_books, books))
	if len(invalid_books) > 0:
		print("Uh oh!  You tried to check in books you did not check out yet!\n", invalid_books)
		return

	# Checked-out books list gets shorter as we return books
	checked_out_books = list(filter(lambda b: b not in books, checked_out_books))

	# Available books list gets larger as books are returned
	available_books = available_books + books

	print("You have returned ", books)

"""



print("Available to check out: ", available_books)

check_out_books(desired_books)

#print("Checked out books: ", checked_out_books)
#print("Available to check out: ", available_books)

#check_out_books(["book02"])


print("Checked out books: ", checked_out_books)
print("Available to check out: ", available_books)

check_in_books(returning_books)

print("Checked out books: ", checked_out_books)
print("Available to check out: ", available_books)


print("Invalid books: ", invalidBooks)
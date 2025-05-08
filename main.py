import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from collections import defaultdict
import time

# Bright Color Palette
BG_COLOR = "#f0f4f7"        # Light blue-gray
PRIMARY_COLOR = "#3a506b"   # Dark blue
SECONDARY_COLOR = "#5bc0be" # Teal
ACCENT_COLOR = "#ff9f1c"    # Orange
TEXT_COLOR = "#1c2541"      # Dark blue
ENTRY_COLOR = "#ffffff"     # White

class Book:
    def __init__(self, title, author, isbn, pdf_path):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.pdf_path = pdf_path

class BSTNode:
    def __init__(self, book, key_func):
        self.book = book
        self.key = key_func(book)
        self.left = None
        self.right = None

class BST:
    def __init__(self, key_func):
        self.root = None
        self.key_func = key_func

    def insert(self, book):
        key = self.key_func(book)
        if not self.root:
            self.root = BSTNode(book, self.key_func)
        else:
            self._insert(book, self.root, key)

    def _insert(self, book, node, key):
        if key < node.key:
            if node.left:
                self._insert(book, node.left, key)
            else:
                node.left = BSTNode(book, self.key_func)
        else:
            if node.right:
                self._insert(book, node.right, key)
            else:
                node.right = BSTNode(book, self.key_func)

    def search(self, search_key):
        search_key = search_key.lower() if isinstance(search_key, str) else search_key
        return self._search(self.root, search_key)

    def _search(self, node, search_key):
        if not node:
            return None
        node_key = node.key.lower() if isinstance(node.key, str) else node.key
        if search_key == node_key:
            return node.book
        elif search_key < node_key:
            return self._search(node.left, search_key)
        else:
            return self._search(node.right, search_key)

class HashTable:
    def __init__(self, key_func, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.key_func = key_func

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, book):
        key = self.key_func(book)
        index = self._hash(key)
        self.table[index].append(book)

    def search(self, search_key):
        search_key = search_key.lower() if isinstance(search_key, str) else search_key
        index = self._hash(search_key)
        for book in self.table[index]:
            key = self.key_func(book)
            key = key.lower() if isinstance(key, str) else key
            if key == search_key:
                return book
        return None

class LibrarySystem:
    def __init__(self):
        self.title_bst = BST(key_func=lambda b: b.title.lower())
        self.isbn_bst = BST(key_func=lambda b: b.isbn)
        self.title_hash = HashTable(key_func=lambda b: b.title.lower())
        self.isbn_hash = HashTable(key_func=lambda b: b.isbn)
        self.author_hash = defaultdict(list)
        self.books = []
        self.search_log = []
        self._load_sample_books()

    def _load_sample_books(self):
        samples = [
            Book("አህያ በወረቀት ቤት", "Alemayehu Wase", "9781234", "books/ahya.pdf"),
            Book("ፍቅር እስከ መቃብር", "Hadis Alemayehu", "9785678", "books/fikir.pdf"),
            Book("ወርቅ ያለበት ድርቅ", "Bealu Girma", "9789101", "books/werk.pdf"),
        ]
        for book in samples:
            self.add_book(book)

    def add_book(self, book):
        self.title_bst.insert(book)
        self.isbn_bst.insert(book)
        self.title_hash.insert(book)
        self.isbn_hash.insert(book)
        self.author_hash[book.author.lower()].append(book)
        self.books.append(book)

    def linear_author_search(self, author):
        return [book for book in self.books if book.author.lower() == author.lower()]

class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📚 Ethiopian Digital Library")
        self.geometry("1200x800")
        self.configure(bg=BG_COLOR)
        
        self.library = LibrarySystem()
        self.current_user = None
        self.style = ttk.Style()
        self.configure_styles()
        self.show_home_page()

    def configure_styles(self):
        self.style.theme_use('clam')
        
        # Base styles
        self.style.configure('.', background=BG_COLOR, foreground=TEXT_COLOR)
        self.style.configure('TFrame', background=BG_COLOR)
        self.style.configure('TLabel', background=BG_COLOR, foreground=TEXT_COLOR, font=('Helvetica', 10))
        self.style.configure('TButton', background=PRIMARY_COLOR, foreground=TEXT_COLOR,
                           font=('Helvetica', 10, 'bold'), borderwidth=0)
        self.style.map('TButton',
                      background=[('active', SECONDARY_COLOR), ('pressed', "#4a8fe7")],
                      foreground=[('active', TEXT_COLOR)])
        
        # Specialized styles
        self.style.configure('Accent.TButton', background=ACCENT_COLOR, 
                           foreground=TEXT_COLOR, font=('Helvetica', 11, 'bold'))
        self.style.configure('Nav.TButton', background=SECONDARY_COLOR, 
                           foreground=TEXT_COLOR, font=('Helvetica', 10))
        self.style.configure('Card.TFrame', background=ENTRY_COLOR, 
                           relief='raised', borderwidth=2)
        self.style.configure('Stats.TFrame', background=ENTRY_COLOR, padding=20)
        self.style.configure('StatLabel.TLabel', font=('Helvetica', 12),
                           foreground=PRIMARY_COLOR)
        self.style.configure('StatValue.TLabel', font=('Helvetica', 16, 'bold'))
        self.style.configure('SubHeader.TLabel', font=('Helvetica', 14, 'bold'),
                           foreground=PRIMARY_COLOR)
        
        # Entry and Combobox
        self.style.configure('TEntry', fieldbackground=ENTRY_COLOR, foreground=TEXT_COLOR,
                           bordercolor=SECONDARY_COLOR, lightcolor=SECONDARY_COLOR)
        self.style.configure('TCombobox', fieldbackground=ENTRY_COLOR, background=PRIMARY_COLOR)
        self.style.map('TCombobox',
                     fieldbackground=[('readonly', ENTRY_COLOR)],
                     selectbackground=[('readonly', PRIMARY_COLOR)])

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def create_nav_button(self, text, command):
        return ttk.Button(self, text=text, command=command, style='Nav.TButton')

    def show_home_page(self):
        self.clear_window()
        header_frame = ttk.Frame(self)
        header_frame.pack(pady=40)
        
        ttk.Label(header_frame, text="ኢትዮጵያ ዲጂታል ቤተመጻሕፍት", style='Header.TLabel').pack(pady=20)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=30)
        
        buttons = [
            ("📚 Manager Login", self.show_manager_login),
            ("👤 User Login", self.show_user_login),
            ("🚪 Exit", self.destroy)
        ]
        
        for text, cmd in buttons:
            btn = ttk.Button(btn_frame, text=text, command=cmd, style='Accent.TButton')
            btn.pack(pady=10, padx=20, ipadx=30, ipady=8, fill=tk.X)
        
        ttk.Separator(self, orient='horizontal').pack(fill=tk.X, pady=20)
        ttk.Label(self, text="Discover • Learn • Grow", foreground=PRIMARY_COLOR).pack()

    def show_manager_login(self):
        self.clear_window()
        self.create_nav_button("← Back", self.show_home_page).pack(anchor='nw', padx=10, pady=10)
        ttk.Label(self, text="Manager Login", style='SubHeader.TLabel').pack(pady=30)
        
        login_frame = ttk.Frame(self)
        login_frame.pack(pady=20)
        
        ttk.Label(login_frame, text="University Code:").grid(row=0, column=0, padx=10, pady=10)
        self.mgr_code = ttk.Entry(login_frame)
        self.mgr_code.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        self.mgr_pwd = ttk.Entry(login_frame, show="*")
        self.mgr_pwd.grid(row=1, column=1, padx=10, pady=10)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Login", command=self.manager_login, style='Accent.TButton').pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Cancel", command=self.show_home_page).pack(side=tk.LEFT, padx=10)

    def manager_login(self):
        if self.mgr_code.get() == "1234" and self.mgr_pwd.get() == "admin":
            self.show_manager_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials", parent=self)

    def show_manager_dashboard(self):
        self.clear_window()
        self.create_nav_button("← Logout", self.show_home_page).pack(anchor='nw', padx=10, pady=10)
        ttk.Label(self, text="Manager Dashboard", style='SubHeader.TLabel').pack(pady=30)
        
        dashboard_frame = ttk.Frame(self)
        dashboard_frame.pack(pady=20)
        
        cards = [
            ("📥 Add Book", self.show_add_book),
            ("📊 View Logs", self.show_logs),
            ("📈 Statistics", self.show_stats)
        ]
        
        for i, (text, cmd) in enumerate(cards):
            card = ttk.Frame(dashboard_frame, style='Card.TFrame')
            card.grid(row=0, column=i, padx=20)
            ttk.Button(card, text=text, command=cmd, style='Accent.TButton').pack(padx=30, pady=20)
        
        stats_frame = ttk.Frame(self, style='Stats.TFrame')
        stats_frame.pack(pady=30)
        
        stats = [
            ("📚 Total Books", len(self.library.books)),
            ("👥 Active Users", "1,234"),
            ("🔍 Searches Today", "89")
        ]
        
        for i, (label, value) in enumerate(stats):
            ttk.Label(stats_frame, text=label, style='StatLabel.TLabel').grid(row=0, column=i, padx=30)
            ttk.Label(stats_frame, text=value, style='StatValue.TLabel').grid(row=1, column=i, padx=30)

    def show_add_book(self):
        self.clear_window()
        self.create_nav_button("← Dashboard", self.show_manager_dashboard).pack(anchor='nw', padx=10, pady=10)
        ttk.Label(self, text="Add New Book", style='SubHeader.TLabel').pack(pady=30)
        
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=20)
        
        fields = [
            ("📖 Title:", "Enter book title"),
            ("👤 Author:", "Enter author name"),
            ("🔢 ISBN:", "Enter ISBN number"),
            ("📁 PDF Path:", "Enter PDF file path")
        ]
        
        self.entries = []
        for i, (label, ph) in enumerate(fields):
            row_frame = ttk.Frame(form_frame)
            row_frame.grid(row=i, column=0, pady=10, sticky='ew')
            
            ttk.Label(row_frame, text=label, font=('Helvetica', 11)).pack(side=tk.LEFT, padx=10)
            entry = ttk.Entry(row_frame, width=40)
            entry.insert(0, ph)
            entry.bind("<FocusIn>", lambda e, entry=entry: self.clear_placeholder(e, entry, ph))
            entry.pack(side=tk.RIGHT, expand=True)
            self.entries.append(entry)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=30)
        ttk.Button(btn_frame, text="Submit", command=self.add_book, style='Accent.TButton').pack(side=tk.LEFT, padx=20)
        ttk.Button(btn_frame, text="Cancel", command=self.show_manager_dashboard).pack(side=tk.LEFT, padx=20)

    def clear_placeholder(self, event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def add_book(self):
        book = Book(
            self.entries[0].get(),
            self.entries[1].get(),
            self.entries[2].get(),
            self.entries[3].get()
        )
        self.library.add_book(book)
        messagebox.showinfo("Success", "Book added successfully", parent=self)
        self.show_manager_dashboard()

    def show_logs(self):
        self.clear_window()
        self.create_nav_button("← Dashboard", self.show_manager_dashboard).pack(anchor='nw', padx=10, pady=10)
        ttk.Label(self, text="Search Logs", style='SubHeader.TLabel').pack(pady=30)
        
        log_frame = ttk.Frame(self)
        log_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        log_text = tk.Text(log_frame, height=15, width=80, yscrollcommand=scrollbar.set,
                          bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
                          font=('Helvetica', 10))
        log_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=log_text.yview)
        
        for log in self.library.search_log:
            log_text.insert(tk.END, 
                f"User: {log['user']['name']} (ID: {log['user']['id']})\n"
                f"Query: {log['query']} ({log['type']})\n"
                f"Time: {log['timestamp']}\n"
                "──────────────────────────────\n"
            )
        
        ttk.Button(self, text="Back", command=self.show_manager_dashboard).pack(pady=20)

    def show_stats(self):
        self.clear_window()
        self.create_nav_button("← Dashboard", self.show_manager_dashboard).pack(anchor='nw', padx=10, pady=10)
        ttk.Label(self, text="Library Statistics", style='SubHeader.TLabel').pack(pady=30)
        
        stats_frame = ttk.Frame(self, style='Stats.TFrame')
        stats_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        # Add charts or additional statistics here
        ttk.Label(stats_frame, text="📊 Search Distribution", style='StatLabel.TLabel').pack()
        
        # Sample chart data
        chart_data = {
            'Title Searches': 45,
            'Author Searches': 30,
            'ISBN Searches': 25
        }
        
        chart_frame = ttk.Frame(stats_frame)
        chart_frame.pack(pady=20)
        
        for i, (label, value) in enumerate(chart_data.items()):
            ttk.Label(chart_frame, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='w')
            ttk.Progressbar(chart_frame, length=200, value=value).grid(row=i, column=1, padx=10)

    def show_user_login(self):
        self.clear_window()
        self.create_nav_button("← Back", self.show_home_page).pack(anchor='nw', padx=10, pady=10)
        ttk.Label(self, text="User Login", style='SubHeader.TLabel').pack(pady=30)
        
        login_frame = ttk.Frame(self)
        login_frame.pack(pady=20)
        
        ttk.Label(login_frame, text="Student ID:").grid(row=0, column=0, padx=10, pady=10)
        self.user_id = ttk.Entry(login_frame)
        self.user_id.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(login_frame, text="Name:").grid(row=1, column=0, padx=10, pady=10)
        self.user_name = ttk.Entry(login_frame)
        self.user_name.grid(row=1, column=1, padx=10, pady=10)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Login", command=self.user_login, style='Accent.TButton').pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Cancel", command=self.show_home_page).pack(side=tk.LEFT, padx=10)

    def user_login(self):
        if not self.user_id.get() or not self.user_name.get():
            messagebox.showerror("Error", "Please fill all fields", parent=self)
            return
        
        self.current_user = {
            'id': self.user_id.get(),
            'name': self.user_name.get()
        }
        self.show_user_dashboard()

    def show_user_dashboard(self):
        self.clear_window()
        self.create_nav_button("← Logout", self.show_home_page).pack(anchor='nw', padx=10, pady=10)
        ttk.Label(self, text=f"Welcome {self.current_user['name']}", style='SubHeader.TLabel').pack(pady=30)
        
        search_frame = ttk.Frame(self)
        search_frame.pack(pady=20)
        
        ttk.Label(search_frame, text="Search By:").grid(row=0, column=0, padx=10)
        self.search_type = ttk.Combobox(search_frame, values=["Title", "Author", "ISBN"], state="readonly")
        self.search_type.current(0)
        self.search_type.grid(row=0, column=1, padx=10)
        
        ttk.Label(search_frame, text="Search Query:").grid(row=1, column=0, padx=10)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.grid(row=1, column=1, padx=10)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Search", command=self.search_book, style='Accent.TButton').pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="History", command=self.show_search_history).pack(side=tk.LEFT, padx=10)

    def search_book(self):
        query = self.search_entry.get()
        search_by = self.search_type.get().lower()
        
        if not query:
            messagebox.showerror("Error", "Please enter a search query", parent=self)
            return
        
        results = self.perform_search(query, search_by)
        self.display_results(results, search_by)

    def perform_search(self, query, search_by):
        start_time = time.perf_counter()
        results = {
            'bst_time': None,
            'hash_time': None,
            'linear_time': None,
            'bst_result': None,
            'hash_result': None,
            'linear_result': None
        }
        
        if search_by == "title":
            results['bst_result'] = self.library.title_bst.search(query)
            results['bst_time'] = time.perf_counter() - start_time
            
            start_time = time.perf_counter()
            results['hash_result'] = self.library.title_hash.search(query)
            results['hash_time'] = time.perf_counter() - start_time
            
        elif search_by == "isbn":
            results['bst_result'] = self.library.isbn_bst.search(query)
            results['bst_time'] = time.perf_counter() - start_time
            
            start_time = time.perf_counter()
            results['hash_result'] = self.library.isbn_hash.search(query)
            results['hash_time'] = time.perf_counter() - start_time
            
        else:
            start_time = time.perf_counter()
            results['hash_result'] = self.library.author_hash.get(query.lower(), [])
            results['hash_time'] = time.perf_counter() - start_time
            
            start_time = time.perf_counter()
            results['linear_result'] = self.library.linear_author_search(query)
            results['linear_time'] = time.perf_counter() - start_time
        
        self.library.search_log.append({
            'user': self.current_user,
            'query': query,
            'type': search_by,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        })
        
        return results

    def display_results(self, results, search_type):
        result_window = tk.Toplevel(self)
        result_window.title("Search Results")
        result_window.geometry("1000x600")
        result_window.configure(bg=BG_COLOR)
        
        self.create_nav_button("← Close", result_window.destroy).pack(anchor='nw', padx=10, pady=10)
        result_frame = ttk.Frame(result_window)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        if search_type in ["title", "isbn"]:
            self.display_bst_hash_results(result_frame, results)
        else:
            self.display_author_results(result_frame, results)

    def display_bst_hash_results(self, frame, results):
        content_frame = ttk.Frame(frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Comparison Table
        columns = ('Method', 'Time (ms)', 'Result')
        tree = ttk.Treeview(content_frame, columns=columns, show='headings')
        tree.heading('Method', text='Search Method')
        tree.heading('Time (ms)', text='Time Taken (ms)')
        tree.heading('Result', text='Search Result')
        
        tree.column('Method', width=150)
        tree.column('Time (ms)', width=100)
        tree.column('Result', width=200)
        
        tree.insert('', 'end', values=(
            'Binary Search Tree',
            f"{results['bst_time']*1000:.2f}",
            'Found' if results['bst_result'] else 'Not Found'
        ))
        
        tree.insert('', 'end', values=(
            'Hash Table',
            f"{results['hash_time']*1000:.2f}",
            'Found' if results['hash_result'] else 'Not Found'
        ))
        
        tree.pack(pady=20, fill=tk.X)
        
        # Detailed Results
        details_frame = ttk.Frame(content_frame)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        if results['bst_result']:
            ttk.Label(details_frame, text="BST Result Details:", style='StatLabel.TLabel').pack(anchor='w')
            ttk.Label(details_frame, text=f"Title: {results['bst_result'].title}").pack(anchor='w')
            ttk.Label(details_frame, text=f"Author: {results['bst_result'].author}").pack(anchor='w')
        
        if results['hash_result']:
            ttk.Label(details_frame, text="Hash Table Result Details:", style='StatLabel.TLabel').pack(anchor='w', pady=10)
            ttk.Label(details_frame, text=f"Title: {results['hash_result'].title}").pack(anchor='w')
            ttk.Label(details_frame, text=f"Author: {results['hash_result'].author}").pack(anchor='w')

    def display_author_results(self, frame, results):
        content_frame = ttk.Frame(frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Comparison Table
        columns = ('Method', 'Time (ms)', 'Books Found')
        tree = ttk.Treeview(content_frame, columns=columns, show='headings')
        tree.heading('Method', text='Search Method')
        tree.heading('Time (ms)', text='Time Taken (ms)')
        tree.heading('Books Found', text='Number of Books')
        
        tree.column('Method', width=150)
        tree.column('Time (ms)', width=100)
        tree.column('Books Found', width=150)
        
        tree.insert('', 'end', values=(
            'Hash Table',
            f"{results['hash_time']*1000:.2f}",
            len(results['hash_result'])
        ))
        
        tree.insert('', 'end', values=(
            'Linear Search',
            f"{results['linear_time']*1000:.2f}",
            len(results['linear_result'])
        ))
        
        tree.pack(pady=20, fill=tk.X)
        
        # Book Lists
        list_frame = ttk.Frame(content_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        hash_list = tk.Listbox(list_frame, bg=ENTRY_COLOR, fg=TEXT_COLOR)
        hash_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        for book in results['hash_result']:
            hash_list.insert(tk.END, f"{book.title} - {book.author}")
        
        linear_list = tk.Listbox(list_frame, bg=ENTRY_COLOR, fg=TEXT_COLOR)
        linear_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        for book in results['linear_result']:
            linear_list.insert(tk.END, f"{book.title} - {book.author}")

    def show_search_history(self):
        history_window = tk.Toplevel(self)
        history_window.title("Search History")
        history_window.geometry("800x400")
        
        ttk.Label(history_window, text="Your Search History", style='SubHeader.TLabel').pack(pady=10)
        
        scrollbar = ttk.Scrollbar(history_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        history_list = tk.Listbox(history_window, yscrollcommand=scrollbar.set,
                                 bg=ENTRY_COLOR, fg=TEXT_COLOR)
        history_list.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=history_list.yview)
        
        for log in self.library.search_log:
            if log['user']['id'] == self.current_user['id']:
                history_list.insert(tk.END, 
                    f"{log['timestamp']} - {log['query']} ({log['type']})"
                )

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
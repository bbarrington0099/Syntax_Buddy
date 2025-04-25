import tkinter as tk
from tkinter import ttk
import json
import os
from tkinter.scrolledtext import ScrolledText
import pygments
from pygments import lexers
from pygments import formatters
from pygments import styles
from pygments.styles import get_style_by_name

class SyntaxHighlighter:
    def __init__(self):
        self.lexers = {
            'python': lexers.PythonLexer(),
            'javascript': lexers.JavascriptLexer(),
            'java': lexers.JavaLexer(),
            'go': lexers.GoLexer()
        }
        self.formatter = formatters.TerminalFormatter(style='monokai')

    def highlight(self, code, language):
        if language.lower() in self.lexers:
            lexer = self.lexers[language.lower()]
            return pygments.highlight(code, lexer, self.formatter)
        return code

class LanguageCheatSheet:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Syntax Cheat Sheet")
        self.root.geometry("1200x800")
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#2d2d2d')
        self.style.configure('TLabel', background='#2d2d2d', foreground='white')
        self.style.configure('TCombobox', background='#2d2d2d', foreground='white')
        self.style.configure('Treeview', background='#2d2d2d', foreground='white', fieldbackground='#2d2d2d')
        self.style.configure('Treeview.Heading', background='#2d2d2d', foreground='white')
        
        # Create main container
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create side panel
        self.side_panel = ttk.Frame(self.main_container, width=250)
        self.side_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Create main content panel
        self.content_panel = ttk.Frame(self.main_container)
        self.content_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Initialize language data
        self.languages = {}
        self.load_languages()
        
        # Create language selector
        self.language_var = tk.StringVar()
        self.language_selector = ttk.Combobox(self.side_panel, textvariable=self.language_var, state='readonly')
        self.language_selector['values'] = list(self.languages.keys())
        self.language_selector.pack(fill=tk.X, padx=5, pady=5)
        self.language_selector.bind('<<ComboboxSelected>>', self.on_language_select)
        
        # Create sections tree
        self.sections_tree = ttk.Treeview(self.side_panel)
        self.sections_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.sections_tree.bind('<<TreeviewSelect>>', self.on_section_select)
        
        # Create content display
        self.content_frame = ttk.Frame(self.content_panel)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        self.description_label = ttk.Label(self.content_frame, wraplength=800, foreground='white')
        self.description_label.pack(fill=tk.X, padx=5, pady=5)
        
        # Create a frame for the code display with a dark background
        self.code_frame = ttk.Frame(self.content_frame)
        self.code_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.code_display = ScrolledText(self.code_frame, wrap=tk.WORD, font=('Consolas', 10), 
                                       bg='#1e1e1e', fg='white', insertbackground='white')
        self.code_display.pack(fill=tk.BOTH, expand=True)
        
        # Initialize syntax highlighter
        self.highlighter = SyntaxHighlighter()
        
        # Set initial state
        if self.languages:
            self.language_selector.set(list(self.languages.keys())[0])
            self.on_language_select(None)

    def load_languages(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Gets path to main.py
        languages_dir = os.path.join(script_dir, '..', 'languages')
        languages_dir = os.path.abspath(languages_dir)
        
        for filename in os.listdir(languages_dir):
            if filename.endswith('.json'):
                with open(os.path.join(languages_dir, filename), 'r') as f:
                    language_data = json.load(f)
                    self.languages[language_data['name']] = language_data

    def on_language_select(self, event):
        language = self.language_var.get()
        if language in self.languages:
            # Clear existing sections
            for item in self.sections_tree.get_children():
                self.sections_tree.delete(item)
            
            # Add new sections
            for section_name in self.languages[language]['sections'].keys():
                self.sections_tree.insert('', 'end', text=section_name.capitalize(), values=(section_name,))

    def on_section_select(self, event):
        language = self.language_var.get()
        selection = self.sections_tree.selection()
        if selection and language in self.languages:
            section_name = self.sections_tree.item(selection[0])['values'][0]
            section = self.languages[language]['sections'][section_name]
            
            # Update description
            self.description_label.config(text=section['description'])
            
            # Clear code display
            self.code_display.delete(1.0, tk.END)
            
            # Add examples
            for example in section['examples']:
                self.code_display.insert(tk.END, f"{example['title']}:\n", 'title')
                if 'explanation' in example:
                    self.code_display.insert(tk.END, f"{example['explanation']}\n\n", 'explanation')
                self.code_display.insert(tk.END, f"{example['code']}\n\n", 'code')
            
            # Configure tags
            self.code_display.tag_configure('title', foreground='#ffcc00', font=('Consolas', 10, 'bold'))
            self.code_display.tag_configure('explanation', foreground='#cccccc', font=('Consolas', 10))
            self.code_display.tag_configure('code', foreground='#ffffff', font=('Consolas', 10))

if __name__ == '__main__':
    root = tk.Tk()
    app = LanguageCheatSheet(root)
    root.mainloop() 
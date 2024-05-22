from django.shortcuts import render
# For usind Markdown Text:
# M1. Importing Markdown from markdown2
from markdown2 import Markdown 
import random

from . import util

# Creating a function to convert the desired EXISTING entry (dk how else to call it) 
def convert_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()

    # Checking to see if we have any entry to convert
    if content == None:
        return None
    else: 
        if content is not None:
        # We have content that needs conversion 
        # So we convert it 
            return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# The entry function below is the function reffered to in urls.py
def entry(request, title):
    
    # We need to see if the title given by the user is already existing or nah
    html_content = convert_to_html(title)
    if html_content == None:
        # Means that the title does not exist --> displaying an error message
        # Error message is displayed by creating a dictionary
        return render(request, "encyclopedia/error.html", {
            "message": "Page Not Found. Entry Does Not Exist"
        })
    else:
        # Otherwise the content requested is displayed 
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content 
        })
    
# for the search bar
def search(request):
    if request.method == "POST":
        # We need to get the data entered, labeled as "q" in layout.html 
        entry_search = request.POST['q'] 

        # Searching for existing data with the searched name
        html_content = convert_to_html(entry_search)
        if html_content is not None: 
            # The content requested and found is displayed 
            return render(request, "encyclopedia/entry.html", {
            "title": entry_search,
            "content": html_content 
        })
        else:
           # Display content having the query as a substring. 
           # Ex:Search for " ytho  --> Python should be in Search Results 
           
           # Checking if the input is a substring 
           general_entries = util.list_entries()
           # 1. Creating a list of recommendations
           recommendation = []
           # 2. If the searched entry is a substring --> give recommendation
           for entry in general_entries:
               if entry_search.lower() in entry.lower():
                   recommendation.append(entry)
                   return render(request, "encyclopedia/search.html", {
                       "recommendation": recommendation
                   })


# Creating the function needed for NewPage option
def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newPage.html")
    else:
        # This means we work with the post method --> the submission of the New Page
        # 1. Grab the Title and Content Data
        title = request.POST['title']
        content = request.POST['content']
        # 2. Check if the Title already exists
        # Send to Error if yes, Save New Page otherwise
        check_title = util.get_entry(title)
        if check_title is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Page Already Exists"
            })
        else:
            util.save_entry(title, content)
            html_content = convert_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
                
            })

# Creating the function needed for EditPage
def edit_page(request):

    # When this function is called by the user via pressind the Edir button
    # one should be redirected to a page 
    # pre-populated with the existing Markdown content of the initial one 
    if request.method == "POST":
        # Grabbing the initial Title
        pre_title = request.POST['entry_title']
        pre_content = util.get_entry(pre_title)
        return render(request, "encyclopedia/edit_page.html", {
            "title": pre_title,
            "content" : pre_content
        })

# Creating function for Saving Edited Page
def save_page(request):
    if request.method == "POST":
        # Getting the new title and content
        edit_title = request.POST['title']
        edit_content = request.POST['content']
        
        # Saving the New Entries
        util.save_entry(edit_title, edit_content)

        # Converting and rendering the page
        html_content = convert_to_html(edit_title)
        return render(request, "encyclopedia/entry.html", {
                "title": edit_title,
                "content": html_content
                
            })
    
# Creating function for Random Display of Content 
def random_page(request):
    allPages = util.list_entries()
    random_choice = random.choice(allPages)
    html_content = convert_to_html(random_choice)
    return render(request, "encyclopedia/entry.html", {
        "title" : random_choice,
        "content": html_content
    })

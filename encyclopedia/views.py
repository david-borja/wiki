from django.shortcuts import render
from random import randint
from markdown2 import markdown
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title)
    if not content:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "message": f"No content about {title} was found",
            "heading": "Not Found"
            })
    return render(request, "encyclopedia/entry.html", {
        "title": title.lower().capitalize(),
        "content": markdown(content)
    })


def search(request):
    query = request.GET['q']
    content = util.get_entry(query)
    if content:
        return render(request, "encyclopedia/entry.html", {
            "title": query.lower().capitalize(),
            "content": markdown(content)
        })
    
    entries = util.list_entries()
    similar_entries = []
    for entry in entries:
        if query.lower() in entry.lower():
            similar_entries.append(entry)

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "entries": similar_entries
    })


def new_page(request):
    if request.POST:
        title = request.POST['title']
        content = request.POST['content']
        entries = util.list_entries()
        for entry in entries:
            if entry.lower() == title.lower():
                return render(request, "encyclopedia/error.html", {
                    "title": title,
                    "message": f"Entry about {title} already exists",
                    "heading": "Entry already exists"
                })
        util.save_entry(title, content)

        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
    return render(request, "encyclopedia/new-page.html")


def edit_entry(request, title):
    if request.POST:
        updated_entry = request.POST['content']
        util.save_entry(title, updated_entry)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown(updated_entry)
        })

    entry = util.get_entry(title)
    return render(request, "encyclopedia/edit-entry.html", {
        "title": title,
        "entry": entry
    })


def random(request):
    entries = util.list_entries()
    index = randint(0, len(entries) - 1)
    random_title = entries[index]
    content = util.get_entry(random_title)
    return render(request, "encyclopedia/entry.html", {
        "title": random_title,
        "content": markdown(content)
    })
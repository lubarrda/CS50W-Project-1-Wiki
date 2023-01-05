from django.shortcuts import render
from markdown2 import Markdown
import random

from . import util

def converter_md_to_html(title):
    content = util.get_entry(title)
    to_markdown = Markdown()
    if content == None:
        return None
    else:
        return to_markdown.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def entry(request, title):
    target_convert_html = converter_md_to_html(title)
    if target_convert_html == None: 
        return render(request, "encyclopedia/error.html", {
            "error_message": "Entry not found"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": target_convert_html
        })

def search(request):
    if request.method == "POST":
        look_search = request.POST['q']
        target_convert_html = converter_md_to_html(look_search)
        if target_convert_html is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": look_search,
                "content": target_convert_html
            })
        else:
            recommendedEntries = util.list_entries()
            recommendation = []
            for entry in recommendedEntries:
                if look_search.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request,"encyclopedia/search.html", {
                "recommendation": recommendation
            })

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleOK = util.get_entry(title)
        if titleOK is not None:
            return render(request, "encyclopedia/error.html", {
                "error_message" : "Page already exist"
            })
        else:
            util.save_entry(title, content)
            target_convert_html = converter_md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content" : target_convert_html
            })

def edit(request):
    if request.method == 'POST':
        title = request.POST['title_entry']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title" : title,
            "content" : content 
        })

def modified(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        target_convert_html = converter_md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title" : title,
            "content" : target_convert_html
        })

def rndm(request):
    recommendedEntries = util.list_entries()
    rndm_search = random.choice(recommendedEntries)
    target_convert_html = converter_md_to_html(rndm_search)
    return render(request, "encyclopedia/entry.html",{
        "title" : rndm_search,
        "content" : target_convert_html
    })





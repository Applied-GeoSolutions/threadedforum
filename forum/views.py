import os, sys, datetime
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse

from models import Post, Category, Forum
from forms import PostForm, CommentForm


def posts_recent(request):
    posts = Post.tree.root_nodes().order_by('created')

    return render_to_response("forum/post_list.html", {
        'posts': posts,
        'categories': Category.objects.all()
    }, context_instance=RequestContext(request))


def posts_all(request):
    posts = Post.objects.all().order_by('-created')

    return render_to_response("forum/post_list.html", {
        'posts': posts,
        'categories': Category.objects.all()
    }, context_instance=RequestContext(request))


def categories(request):
    return HttpResponse()


def category_posts(request, category_id):
    cat = Category.objects.get(pk=category_id)
    posts = Post.objects.filter(is_comment=False, categories=cat).order_by('created')

    return render_to_response("forum/post_list.html", {
        'posts': posts,
        'category': cat,
        'categories': Category.objects.all()
    }, context_instance=RequestContext(request))


def category_post_new(request, category_id):
    return HttpResponse()


def post(request, id, title=None):
    if request.method == 'POST' and 'type' in request.POST:
        if request.POST['type'] == 'reply':
            try:
                parent_id = int(request.POST['reply_to'])
            except:
                parent_id = id
            parent = Post.objects.get(pk=parent_id)
            comment = Post(
                user=request.user,
                content=request.POST['content'],
                heading="Re:"+parent.heading,
                parent=parent,
                is_comment=True,
                forum=parent.forum
            )
            comment.save()
        elif request.POST['type'] == 'delete':
            del_id = int(request.POST['delete_id'])
            comment = Post.objects.get(pk=del_id)
            if request.user.is_staff or comment.user == request.user:
                comment.delete()
                if del_id == int(id):
                    return HttpResponseRedirect('/forum/category/general/')

    post = Post.objects.get(pk=id)

    if post.is_comment:
        post = post.get_root()

    if post.hits is None:
        post.hits = 1
    else:
        post.hits = post.hits + 1
    post.save()

    replies = post.get_descendants().select_related("parent")

    reply_numbers = []
    for r in replies:
        reply_numbers.append([r.created, r.pk])

    reply_numbers.sort(key=lambda l: l[0])

    i = 1
    pk_numbers = {}
    for r in reply_numbers:
        pk_numbers[r[1]] = i
        i += 1

    for r in replies:
        r.number = pk_numbers[r.id]

    for r in replies:
        try:
            r.parent_number = pk_numbers[r.parent.pk]
        except:
            r.parent_number = str(id)

    return render_to_response("forum/post.html", {
        'post': post,
        'replies': replies,
        'categories': Category.objects.all()
    }, context_instance=RequestContext(request))


def post_new(request, category_id=None):
    category = None
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.is_comment = False
            post.forum = Forum.objects.all()[0]
            post.post_ip = request.META.get('REMOTE_ADDR', "0.0.0.0")
            post.save()
            post_form.save_m2m()
            return HttpResponseRedirect(reverse("post", args=[post.pk]))
    else:
        if category_id is not None and category_id != '':
            category = Category.objects.get(pk=category_id)
            post_form = PostForm(initial={'categories': [category]})
        else:
            post_form = PostForm()

    return render_to_response("forum/form.html", {
        'form': post_form,
        'category': category,
        'categories': Category.objects.all()
    }, context_instance=RequestContext(request))


def post_edit(request, id):
    post = Post.objects.get(pk=id)

    if post.is_comment:
        Form = CommentForm
    else:
        Form = PostForm

    if request.method == 'POST':
        post_form = Form(request.POST, instance=post)
        if post_form.is_valid():
            post = post_form.save()
            return HttpResponseRedirect(reverse("post", args=[post.pk]))
    else:
        post_form = Form(instance=post)

    return render_to_response("forum/form.html", {
        'form': post_form,
        'categories': Category.objects.all()
    }, context_instance=RequestContext(request))

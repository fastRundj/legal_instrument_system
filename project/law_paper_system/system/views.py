from django.shortcuts import render, get_object_or_404, redirect, render_to_response
import os
from .models import Paper, Court
from django.utils import timezone
from .forms import loginForm, paperForm
from .search_func import search_api, search_one_api, delete_api, get_num
from django.views.decorators.csrf import csrf_exempt

def main_window(request):
    paper = search_one_api(1)
    paper[10] = paper[10][:8]
    return render(request, 'main_window.html', {'paper': paper})

#新开了一个页面，找到与custkey匹配的model来显示
#可作为一个文书的详细信息显示页面
def paper_detail(request, paper_id):
    try:
        paper = search_one_api(paper_id)
        #return render(request, 'paper_detail.html', {'paper': paper})
    except Exception as identifier:
        tmp_paper = get_object_or_404(Paper, id=paper_id)
        paper = search_one_api(1).copy()
        paper[0] = tmp_paper.id
        paper[2] = tmp_paper.title
        paper[6] = tmp_paper.time
        paper[9] = tmp_paper.paper_type
        paper[10] = [tmp_paper.content]
    return render(request, 'paper_detail.html', {'paper': paper})


@csrf_exempt
#跳转到新的页面，添加表项
def paper_add(request):
    #如果是保存操作
    if request.method == 'POST':
        print('123')
        form = paperForm(request.POST)
        if form.is_valid():
            print('ok')
            paper = form.save(commit=False)
            paper.save()
            return redirect('paper_detail', paper.id)
    else:
        form = paperForm()
    return render(request, 'paper_edit.html', {'form':form})

def search(request):
    q = request.GET.get('q')
    result_list = search_api(q)
    return render(request, 'paper_all.html', {'paper_list':result_list})
    
def login(request):
    form = loginForm()
    if request.method == 'POST':
        print(request.POST['username'])
        if request.POST['username'] == 'pp' and request.POST['password'] == '123':
            print('ok!')
        else:
            return render(request, 'login.html', {'form':form})
        return redirect('main_window')
    else:
        return render(request, 'login.html', {'form':form})

def delete(request, paper_id):
    delete_api(paper_id)
    return redirect('main_window')

    
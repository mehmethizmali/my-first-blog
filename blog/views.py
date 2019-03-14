from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm




def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
    

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

#veri Ekleme
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
          #Post veri tabanına kayıt etme(veri ekleme) işlemi yapıyoruz
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            #Veri ekleme işleminden sonra 'post_detail sayfasına yönlendiriyoruz'
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'myForm': form})


#veri güncelleme

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    #POST metodu ile pk(primary key) ile ilgili veri alınıyor
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        #Alınan veri Post tablosunda güncelleniyor
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            #veri güncelleme işleminden sonra 'post_detail sayfasına yönlendiriyoruz'
             # return redirect('post_list')
            return redirect('post_detail', pk=post.pk)
   #Veri güncellenmediğine 'blog/post_edit.html' sayfasını render ediyoruz
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'myForm': form})    
    

	



from django.shortcuts import render, redirect

from django.views import View
from .models import Video
from .forms import VideoForm


from django.db.models import Q

class IndexView(View):

    def get(self, request, *args, **kwargs):

        if "search" in request.GET:

            if request.GET["search"] == "" or request.GET["search"].isspace():
                return redirect("tube:index")


            search = request.GET["search"].replace("　", " ")
            search_list = search.split(" ")


            query = Q()
            for word in search_list:

                if "option" in request.GET:
                    query |= Q(comment__contains=word)
                else:
                    query &= Q(comment__contains=word)


            videos = Video.objects.filter(query).order_by("-dt")
        else:
            videos = Video.objects.all().order_by("-dt")


        context = {"videos": videos}



        return render(request, "tube/index.html", context)

    def post(self, request, *args, **kwargs):

        """
        if "title" in request.POST:

            if request.POST["title"] == "" or request.POST["title"].isspace():
                return redirect("tube:index")

        if "comment" in request.POST:

            if request.POST["comment"] == "" or request.POST["comment"].isspace():
                return redirect("tube:index")

        posted = Video( title = request.POST["title"], comment = request.POST["comment"])
        posted.save()

        """
        
        formset = VideoForm(request.POST)

        if formset.is_valid():
            print("バリデーションOK")
            formset.save()
        else:
            print("バリデーションエラー")



        return redirect("tube:index")

index = IndexView.as_view()


class DeleteView(View):

    def post(self, request, pk, *args, **kwargs):

        print("削除")

        #.first()で一番上のレコードを1つ取る。
        video   = Video.objects.filter(id=pk).first()
        video.delete()

        #TIPS:すでにurls.pyにてpkが数値型であることがわかっているので、バリデーションをする必要はない。

        return redirect("tube:index")

delete  = DeleteView.as_view()

class UpdateView(View):
    
    def get(self, request, pk,*args, **kwargs):

        video   = Video.objects.filter(id=pk).first()
        context = { "video":video }

        return render(request, "tube/update.html", context )

    def post(self, request, pk, *args, **kwargs):

        #まず、編集対象のレコードを特定
        instance    = Video.objects.filter(id=pk).first()

        #第二引数にinstanceを指定することで、対象の編集ができる
        formset     = VideoForm(request.POST, instance=instance)

        if formset.is_valid():
            print("バリデーションOK")
            formset.save()
        else:
            print("バリデーションNG")

        return redirect("tube:index")

update  = UpdateView.as_view()

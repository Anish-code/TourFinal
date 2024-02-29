
from decimal import Decimal
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string

from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from core.models import Tour, TourImages, TourReview, Trek

def index(request):
    tourfeatured = Tour.objects.filter(featured= True).order_by("-id")
    context = {
        "tourfeatured": tourfeatured
    }
    return render(request, 'core/index.html', context)

def tour_list_view(request):
    tours=Tour.objects.all().order_by("-id")
    context = {
        "tours": tours,
    }
    return render(request,'core/explore.html',context)


def tour_detail_view(request,tid):
    tour = Tour.objects.get(tid=tid)
    tours = Tour.objects.filter(category = tour.category).exclude(tid=tid)
    reviews = TourReview.objects.filter(tour=tour).aggregate(rating=AVG('rating'))
    review_form = TourReviewform()
    make_review = True

    if request.user.is_authenticated:
        user_review_count = TourReview.objects,filter(user=request.user, tour=tour).count()
        if user_review_count>0:
            make_review= False
    
    context= {
        "t":tour,
        "tours":tours,
        "t_image":t_image,
        "make_review":make_review,
        "reviews":reviews,
        "average_rating": average_rating,
        "review_form": review_form,

    }

    return render(request,"core/tour-detail.html",context)

def ajax_add_review(request,pid):
    tour = Tour.objects.get(tid=tid)
    user = request.user

    review=TourReview.objects,create(
        user=user,
        tour = tour,
        review= request.POST['review'],
        rating = request.POST['rating'],
    )

    context ={
        'user':iser.username,
        'review':request.POST['review'],
        'rating':request.POST['rating'],

    }

    average_reviews = TourReview.objects.filter(tour=tour).aggregate(rating =AVG('rating') )

    return JsonResponse(
        {
            'bool':True,
            'context':context,
            'avg_reviews':average_reviews,
        }
    )
    
def services(request):
    return render(request, 'core/services.html')

def getrecommendation(request):
    return render(request, 'core/getrecommendation.html')

def explore(request):
    return render(request, 'core/explore.html')

def gallery(request):
    return render(request, 'core/gallery.html')

def blogs(request):
    return render(request, 'core/blogs.html')

def contact(request):
    return render(request, 'core/contact.html')
def userdashboard(request):
    return render (request, 'core/userdashboard.html')

def import_trek_data(request):
    if request.method == 'POST':
        form = TrekImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Please upload a valid CSV file.')
                return redirect('import_trek_data')
            
            # Process the CSV file
            try:
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                csv_data = csv.reader(decoded_file)
                
                # Skip the header row
                next(csv_data)
                
                for row in csv_data:
                    trek = Trek.objects.create(
                        trek=row[0],
                        cost=row[1],
                        time=row[2],
                        trip_grade=row[3],
                        max_altitude=row[4],
                        accommodation=row[5],
                        best_travel_time=row[6],
                        contact=row[7]
                    )
                messages.success(request, 'Trek data imported successfully.')
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')
            
            return redirect('import_trek_data')
    else:
        form = TrekImportForm()
    
    return render(request, 'import_trek_data.html', {'form': form})



def tour_data(request):
    if request.method == 'POST':
        # Retrieve the selected values from the form
        trip_type = request.POST.get('trip_type')
        duration = request.POST.get('duration')
        budget_range = request.POST.get('budget_range')

    return render(request, 'core/getrecommendation.html')


def collaborativerecommend(self, user_id, num_recommendations):
        content_based_scores = {item_id: np.random.rand() for item_id in self.item_features.keys()}
        return content_based_scores
        

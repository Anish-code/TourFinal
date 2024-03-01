
from decimal import Decimal
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
import pandas as pd
from core.recommendationform import LocationForm
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from core.models import Tour, TourImages, TourReview, Trek
from core.hybridRecommendation import ContentBasedModel, CollaborativeFilteringModel, HybridRecommendationSystem
from django.http import JsonResponse


def index(request):
    tourfeatured = Tour.objects.filter(featured= True).order_by("-id")
    context = {
        "tourfeatured": tourfeatured
    }
    return render(request, 'core/index.html', context)

# def tour_list_view(request):
#     tours=Tour.objects.all().order_by("-id")
#     context = {
#         "tours": tours,
#     }
#     return render(request,'core/explore.html',context)


def tourdata(request):
    tourdata = tourdata
    context ={
        "tourdata": tourdata,
    }
    return render(request, 'core/explore.html', context)

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

def explore_destinations(request):
    # Assuming you have a CSV file named 'tourdata.csv' in your project directory
    csv_file = 'tourdata.csv'
    tourdata = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tourdata.append(row)
    
    return render(request, 'explore_destinations.html', {'tourdata': tourdata})

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
    df = pd.read_csv('../tourdatas.csv')
    unique_df = df.drop_duplicates(subset=['location'])

    locations = unique_df[['ID', 'location']].to_dict(orient='records')
    return render(request, 'core/getrecommendation.html', {"locations": locations})

def explore(request):
    df = pd.read_csv('../tourdatas.csv')
    unique_df = df.drop_duplicates(subset=['location'])

    tourdata = unique_df.to_dict(orient='records')
    print(tourdata)
    return render(request, 'core/explore.html', {"tourdata":tourdata})

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


def recommendation_view(request):
    item_id = request.GET.get('item_id')  
    hybrid_system = HybridRecommendationSystem(content_based_model, collaborative_filtering_model)

    num_recommendations = 10  
    recommendations = hybrid_system.recommend(item_id, num_recommendations)

    context = {
        'recommendations': recommendations,
    }

    return render(request, 'recommendation_template.html', context)


def button_clicked(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            selected_id = form.cleaned_data['locations']
            return HttpResponse("Button clicked: " + selected_id)
    else:
        form = LocationForm()
    return render(request, 'core/button_template.html', {'form': form})


def get_recommendations(request, item_id):
    if item_id:
        df = pd.read_csv('../tourdatas.csv')

        content_based_model = ContentBasedModel(df)
        collaborative_filtering_model = CollaborativeFilteringModel(df)

        num_recommendations = 10
        hybrid_system = HybridRecommendationSystem(content_based_model, collaborative_filtering_model)
        recommendations = hybrid_system.recommend(item_id, num_recommendations)
        recommendation_json = df[df["ID"].isin(recommendations)].to_json(orient="records")
    
        return JsonResponse({'recommendations': recommendation_json})
    else:
        return JsonResponse({'error': 'item_id parameter is missing'})
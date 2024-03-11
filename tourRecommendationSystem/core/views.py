
from decimal import Decimal
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
import pandas as pd
from core.recommendationform import CityForm
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from core.models import Tour, TourImages, TourReview, Trek
from core.hybridRecommendation import ContentBasedModel, CollaborativeFilteringModel, HybridRecommendationSystem
from django.http import JsonResponse
from core.content import Contentbased


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
    df = pd.read_csv('../complete_data.csv')

    # Dropping duplicate entries based on the 'city' column
    unique_df = df.drop_duplicates(subset=['city'])

    # Extracting city names and IDs as a list of dictionaries
    city = unique_df[['ID', 'city']].to_dict(orient='records')
    # Rendering the 'getrecommendation.html' template and passing the city data as context
    return render(request, 'core/getrecommendation.html', {"city": city})
def explore(request):
    df = pd.read_csv('../complete_data.csv')
    unique_df = df.drop_duplicates(subset=['city'])

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


# def recommendation_view(request):
#     item_id = request.GET.get('item_id')  
#     hybrid_system = HybridRecommendationSystem(content_based_model, collaborative_filtering_model)

#     num_recommendations = 10  
#     recommendations = hybrid_system.recommend(item_id, num_recommendations)

#     context = {
#         'recommendations': recommendations,
#     }

#     return render(request, 'recommendation_template.html', context)


# def contentbasedrecommendation_view(request):
#     city= request.GET.get('city')
#     contentbased= Contentbased('../Required_data.csv')
#     recommendation= contentbased.get_recommendations(city)
#     context = {
#         'recommendation':recommendation,
#     }
#     return render(request,'recommendation_template.html', context)

def button_clicked(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            selected_id = form.cleaned_data['locations']
            return HttpResponse("Button clicked: " + selected_id)
    else:
        form = LocationForm()
    return render(request, 'core/button_template.html', {'form': form})


# def get_recommendations(request, city):
#     if item_id:
#         df = pd.read_csv('../Requires_data.csv')
#         contentbased= Contentbased(df)
#         recommendation= contentbased.get_recommendations(city)
#         recommendation_json = df[df["city"].isin(recommendation)].to_json(orient="records")
#         # recommendation_json = df[df["city"].isin(recommendation)].to_json(orient="records")

    
#         return JsonResponse({'recommendations': recommendation_json})
#     else:
#         return JsonResponse({'error': 'city parameter is missing'})
def tour_details(request, item_id):
    if item_id:
        df = pd.read_csv('../complete_data.csv')
        item_data = df[df['ID'] == int(item_id)].iloc[0].to_dict()
        print(item_data)
        return render(request, 'core/tour-detail.html', {'item': item_data})


# def get_recommendations(request, city):
#     if city:
        
#         content_based = Contentbased('complete_data.csv')
#         recommendations = content_based.get_recommendations(city)
#         print(recommendations)
#         recommendation_json = recommendations.to_json(orient="records")
#         return JsonResponse({'recommendations': recommendation_json})
#     else:
#         return JsonResponse({'error': 'city parameter is missing'})

# def content_based_recommendation_view(request):
#     city = request.GET.get('city')
#     if city:
#         content_based = Contentbased('complete_data.csv')
#         recommendations = content_based.get_recommendations(city)
#         context = {'recommendations': recommendations.to_dict(orient='records')}
#         return render(request, 'core:recommendation_template.html', context)
#     else:
#         return JsonResponse({'error': 'city parameter is missing'})


def get_city_name_from_item_id(item_id):
    # Read the dataset
    df = pd.read_csv('../complete_data.csv')
    
    # Search for the row where ID matches the given item_id
    row = df[df['ID'] == item_id]
    
    # If the row exists, return the city name from that row
    if not row.empty:
        return row.iloc[0]['city']
    else:
        return None

def get_recommendations(request, item_id):
    if item_id:
        data_file = '../complete_data.csv'
        content_based = Contentbased(data_file)
        
        # Retrieve city name associated with the item_id
        city_name = get_city_name_from_item_id(item_id)
        df = pd.read_csv('../complete_data.csv')

        if city_name:
            recommendations = content_based.recommend(city_name)
            
            if recommendations is not None and not recommendations.empty:
    
    # Extract IDs from recommendations DataFrame
                recommendation_ids = recommendations['ID'].tolist()

    
    # Filter DataFrame based on recommendation IDs
                recommended_df = df[df["ID"].isin(recommendation_ids)]
    
    # Convert filtered DataFrame to JSON
                recommendation_json = recommended_df.to_json(orient="records")
                print(recommendation_json)
    
                return JsonResponse({'recommendations': recommendation_json})

            else:
                return JsonResponse({'message': 'No recommendations found for the given city'})
        else:
            return JsonResponse({'error': 'City name not found for the given item_id'})
    else:
        return JsonResponse({'error': 'item_id parameter is missing'})

# def get_recommendations(request, item_id):
#     if item_id:
#         data_file = '../complete_data.csv'
#         content_based = Contentbased(data_file)
#         recommendations = content_based.get_recommendations(item_id)
#         df = pd.read_csv('../complete_data.csv')
#         if recommendations is not None:
#             recommendation_json = df[df["ID"].isin(recommendations)].to_json(orient="records")
#             return JsonResponse({'recommendations': recommendation_json})
#         else:
#             return JsonResponse({'error': 'No recommendations found'})
#     else:
#         return JsonResponse({'error': 'item_id parameter is missing'})

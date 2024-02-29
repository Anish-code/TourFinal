from django.contrib import admin

from core.models import Tour, TourImages,TourReview, Trek, Category


class TourImagesAdmin(admin.TabularInline):
    model = TourImages


class TourAdmin(admin.ModelAdmin):
    inlines = [TourImagesAdmin]
    list_display = ['title', 'image', 'user', 'tid', 'description', 'price', 'rating', 'short_description','address']

class CategoryAdmin(admin.ModelAdmin):
    list_display= ['title','category_image', 'cid']

class TourReviewAdmin(admin.ModelAdmin):
    list_display = ['user','tour','review','rating']


admin.site.register(Tour, TourAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(TourReview, TourReviewAdmin)

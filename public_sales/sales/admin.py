from django.contrib import admin
from .models import (City, Neighborhood, ImmobileKind,
                     Status, Seller, AutomobileModel, AutomobileBrand,
                     AutomobileKind, Immobile, Automobile, Like_Immobile)


admin.site.register(City)
admin.site.register(Neighborhood)
admin.site.register(ImmobileKind)
admin.site.register(Status)
admin.site.register(Seller)
admin.site.register(AutomobileModel)
admin.site.register(AutomobileBrand)
admin.site.register(AutomobileKind)
admin.site.register(Immobile)
admin.site.register(Automobile)
admin.site.register(Like_Immobile)

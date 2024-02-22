from django.contrib import admin
from .models import MatchList,GamersList,ChempionsList


class MatchListAdmin(admin.ModelAdmin):
    list_display=MatchList.DisplyFields
    search_fields=MatchList.DisplyFields
    list_filter=MatchList.FiltersFields


    
class GamersListAdmin(admin.ModelAdmin):
    list_display=GamersList.DisplayFields
    search_fields=GamersList.SearchFields
    list_filter=GamersList.FiltersFields

class ChempionsListAdmin(admin.ModelAdmin):
    list_display=ChempionsList.DisplayFields
    search_fields=ChempionsList.SearchFields

admin.site.register(MatchList,MatchListAdmin)
admin.site.register(GamersList,GamersListAdmin)
admin.site.register(ChempionsList,ChempionsListAdmin)



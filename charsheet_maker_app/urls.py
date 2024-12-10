from django.urls import path

from . import views

app_name = "charsheet_maker_app"
urlpatterns = [
     path("", views.IndexView.as_view(), name="index"),

     path("sheet_template/<int:object_id>/", 
          views.SheetTemplateDetailVIew, name="sheet_template_detail"),
     path("character_sheet/<int:object_id>/", 
          views.CharacterSheetDetailVIew, name="character_sheet_detail"),

     path("sheet_template/create/", 
          views.SheetTemplateCreateView, name="sheet_template_create"),

     path("sheet_template/<int:template_id>/create_character_sheet/", 
          views.CharacterSheetCreateView, name="character_sheet_create"),
]

# Sheet templates and character sheets should be deletable, 
# but only character sheets editable, for simplicity;
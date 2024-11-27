from django.urls import path

from . import views

app_name = "charsheet_maker_app"
urlpatterns = [
     path("", views.IndexView.as_view(), name="index"),

     path("sheet_template/<int:object_id>/", 
          views.SheetTemplateDetailVIew, name="sheet_template_detail"),
     path("character_sheet/<int:object_id>/", 
          views.CharacterSheetDetailVIew, name="character_sheet_detail"),

     # sheet_template/<int:object_id>/create
     # sheet_template/<int:object_id>/update
     # sheet_template/<int:object_id>/delete

     # sheet_template/<int:object_id>/add_sheet
     # sheet/<int:object_id>/update
     # sheet/<int:object_id>/delete
]
from django.urls import path

from . import views

app_name = "charsheet_maker_app"
urlpatterns = [
     # Página inicial
     path("", views.IndexView.as_view(), name="index"), 

     # Detalhe do template
     path("sheet_template/<int:object_id>/", 
          views.SheetTemplateDetailVIew, name="sheet_template_detail"),

     # Detalhe do personagem
     path("character_sheet/<int:object_id>/", 
          views.CharacterSheetDetailVIew, name="character_sheet_detail"),

     # Criação de um novo template
     path("sheet_template/create/", 
          views.SheetTemplateCreateView, name="sheet_template_create"),

     # Criação de um personagem baseado em um template
     path("sheet_template/<int:template_id>/create_character_sheet/", 
          views.CharacterSheetCreateView, name="character_sheet_create"),
]
from django.urls import path

from . import views

app_name = "charsheet_maker_app"
urlpatterns = [

     # Página inicial - lista de templates de fichas;
     path("", views.IndexView.as_view(), name="index"), 

     # Visualização de um template de ficha;
     path("sheet_template/<int:template_id>/", 
          views.SheetTemplateDetailVIew, name="sheet_template_detail"),

     # Visualização/edição de uma ficha de personagem;
     path("character_sheet/<int:sheet_id>/", 
          views.CharacterSheetDetailView, name="character_sheet_detail"),

     # Criação de um novo template de ficha;
     path("sheet_template/create/", 
          views.SheetTemplateCreateView, name="sheet_template_create"),

     # Criação de uma ficha de personagem baseado em um template;
     path("sheet_template/<int:template_id>/create_character_sheet/", 
          views.CharacterSheetCreateView, name="character_sheet_create"),

     # Remoção de uma ficha de personagem;
     path("character_sheet/<int:sheet_id>/remove/",
          views.CharacterSheetRemoveView, name="character_sheet_remove"),

     # Adição de item ao inventário da ficha de um personagem;
     path("character_sheet/<int:sheet_id>/add_item/", 
          views.CharacterSheetAddItemView, name="character_sheet_add_item"),

     # Remoção de item do inventário da ficha de um personagem;
     path("character_sheet/<int:sheet_id>/remove_item/", 
          views.CharacterSheetRemoveItemView, name="character_sheet_remove_item"),
]
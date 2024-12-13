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
     
     # Exclusão de um template
     path("sheet_template/<int:object_id>/delete/", 
         views.SheetTemplateDeleteView, name="sheet_template_delete"),

     # Exclusão de um personagem
     #path("character_sheet/<int:object_id>/delete/", 
     #     views.CharacterSheetDeleteView, name="character_sheet_delete"),

     # Edição de um personagem
     #path("character_sheet/<int:object_id>/edit/", 
     #     views.CharacterSheetEditView, name="character_sheet_edit"),
          #views.CharacterSheetEditView.as_view(), name="character_sheet_edit"),
]

# Sheet templates and character sheets should be deletable, 
# but only character sheets editable, for simplicity;
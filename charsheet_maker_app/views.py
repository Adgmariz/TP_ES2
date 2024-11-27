from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from .models import SheetTemplate, CharacterSheet

class IndexView(LoginRequiredMixin, generic.ListView):

    login_url = '/accounts/login/'
    template_name = "charsheet_maker_app/sheet_templates.html"
    context_object_name = "sheet_template_list"
    
    def get_queryset(self):

        return SheetTemplate.objects.filter(sheetTemplateOwner=self.request.user).order_by("-creation_date")

@login_required
def SheetTemplateDetailVIew(request, object_id):

    sheet_template = get_object_or_404(SheetTemplate, id=object_id)
    character_sheets_list = CharacterSheet.objects.filter(template=sheet_template)

    return render(
        request, 
        "charsheet_maker_app/sheet_template_detail.html", 
        {
            "sheet_template": sheet_template,
            "owner": sheet_template.sheetTemplateOwner,
            "character_sheets_list": character_sheets_list,
        },
    )

@login_required
def CharacterSheetDetailVIew(request, object_id):

    character_sheet = get_object_or_404(CharacterSheet, id=object_id)
    sheet_template = character_sheet.template

    return render(
        request,
        "charsheet_maker_app/character_sheet_detail.html",
        {
            "character_sheet": character_sheet,
            "sheet_template": sheet_template
        },
    )

# def createSheetTemplateView

# def createCharacterSheetView

# def deleteSheetTemplateView

# def deleteCharacterSheetView

# def deleteSheetTemplateView

# def deleteCharacterSheetView
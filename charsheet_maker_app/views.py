from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from .forms import SheetTemplateForm, CharacterSheetFormExceptSheetTemplate
from .forms import validate_sheet_template_form_input_content
from .forms import generate_character_sheet_form_inputs
from .forms import CharacterForm

from .models import SheetTemplate, CharacterSheet

class IndexView(LoginRequiredMixin, generic.ListView):

    login_url = '/accounts/login/'
    template_name = "charsheet_maker_app/sheet_template_list.html"
    context_object_name = "sheet_template_list"
    
    def get_queryset(self):

        return SheetTemplate.objects.filter(sheet_template_owner=self.request.user).order_by("-creation_date")

@login_required
def SheetTemplateDetailVIew(request, object_id):

    sheet_template = get_object_or_404(SheetTemplate, id=object_id)
    character_sheets_list = CharacterSheet.objects.filter(template=sheet_template)

    return render(
        request, 
        "charsheet_maker_app/sheet_template_detail.html", 
        {
            "sheet_template": sheet_template,
            "owner": sheet_template.sheet_template_owner,
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

@login_required
def SheetTemplateCreateView(request):
    
    if request.method == 'GET':
        
        form = SheetTemplateForm()
        return render(request, "charsheet_maker_app/sheet_template_form.html", {"form": form})

    else:

        form = SheetTemplateForm(request.POST)
        if form.is_valid():

            fields_error_messages = validate_sheet_template_form_input_content(form.cleaned_data)

            # Will contain contents validation errors 
            # and mantain the values the user tried to send;
            if len(fields_error_messages) != 0:
                return render(request, "charsheet_maker_app/sheet_template_form.html", 
                              {"form": form, "fields_error_messages": fields_error_messages})

            # Success cycle end. Go to templates page;
            instance = form.save(commit=False)
            instance.sheet_template_owner = request.user
            instance.save()
            return redirect(reverse("charsheet_maker_app:index"))

        # Will contain basic validation errors (from django built-in form), 
        # and mantain the values the user tried to send;
        return render(request, "charsheet_maker_app/sheet_template_form.html", {"form": form})

@login_required
def CharacterSheetCreateView(request, template_id):
    sheet_template = get_object_or_404(SheetTemplate, id=template_id, sheet_template_owner=request.user)
    if request.method == 'GET':
        form = CharacterForm(sheet_template, request.POST)
        if form.is_valid():
            # Cria o personagem
            character_data = form.cleaned_data
            character = sheet_template.create_character(
                name=character_data.pop("name"),
                **character_data
            )
            # Redireciona para a página do template ou lista de personagens
            return HttpResponseRedirect(reverse('view_template', args=[template_id]))
        # sheet_template = get_object_or_404(SheetTemplate, id=template_id)
        form = generate_character_sheet_form_inputs(template_object=sheet_template)
        return render(request, "charsheet_maker_app/character_sheet_form.html", 
                        {"sheet_template": sheet_template, 
                        "form": form})

        return HttpResponse("form created dynamically from sheet template")

    else:

        # form = generate_character_sheet_form_inputs(template_object=sheet_template)
        # if form.is_valid():

            # fields_error_messages = validate_character_sheet_form_input_content(, form.cleaned_data)

        return HttpResponse("added your sheet!!!")

        # Will contain basic validation errors (from django built-in form), 
        # and mantain the values the user tried to send;
        # return render(request, "charsheet_maker_app/character_sheet_form.html", 
        #             {"sheet_template": sheet_template, 
        #             "form": form})

@login_required
def SheetTemplateDeleteView(request, object_id):
    # Verifica se o usuário atual é o proprietário
    sheet_template = get_object_or_404(SheetTemplate, id=object_id, sheet_template_owner=request.user)

    if request.method == "POST":
        sheet_template.delete()
        # Redireciona para a lista de templates após a exclusão
        return redirect(reverse("charsheet_maker_app:index"))

    # Renderiza uma página de confirmação
    return render(
        request,
        "charsheet_maker_app/sheet_template_confirm_delete.html",
        {"sheet_template": sheet_template},
    )
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import reverse

from .models import SheetTemplate, CharacterSheet

from .forms import validate_sheet_template_form_input_content
from .forms import SheetTemplateForm

from .forms import CharacterSheetCreateForm
from .forms import CharacterSheetEditFormExceptItems

from .forms import CharacterSheetAddItemForm
from .forms import get_item_data_from_add_item_form

from .forms import CharacterSheetRemoveItemForm
from .forms import get_item_id_from_remove_item_form

class IndexView(LoginRequiredMixin, generic.ListView):

    login_url = '/accounts/login/'
    template_name = "charsheet_maker_app/sheet_template_list.html"
    context_object_name = "sheet_template_list"
    
    def get_queryset(self):

        return SheetTemplate.objects.filter(sheet_template_owner=self.request.user).order_by("-creation_date")

@login_required
def SheetTemplateDetailVIew(request, template_id):

    sheet_template = get_object_or_404(SheetTemplate, id=template_id)
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
def CharacterSheetDetailView(request, sheet_id):

    character_sheet = get_object_or_404(CharacterSheet, id=sheet_id)
    sheet_template = character_sheet.template

    if request.method == 'GET':

        form_without_items = CharacterSheetEditFormExceptItems(
            sheet_template_object=sheet_template, character_sheet_object=character_sheet
        )

    else:

        form_without_items = CharacterSheetEditFormExceptItems(
            sheet_template_object=sheet_template, character_sheet_object=None, data=request.POST
        )

        if form_without_items.is_valid():

            # Success. Edit Charsheet;

            character_sheet.name = form_without_items.cleaned_data["name"]
            character_sheet.experience = form_without_items.cleaned_data["experience"]
            character_sheet.level = form_without_items.cleaned_data["level"]
            character_sheet.gold = form_without_items.cleaned_data["gold"]

            character_sheet.char_class = form_without_items.cleaned_data["class"]
            character_sheet.race = form_without_items.cleaned_data["race"]

            for k, v in form_without_items.cleaned_data.items():
                if k[:11] == "background-":
                    character_sheet.background[k[11:]] = v
                elif k[:10] == "attribute-":
                    character_sheet.attributes[k[10:]] = v
                elif k[:5] == "stat-":
                    character_sheet.stats[k[5:]] = v

            character_sheet.save()

    add_item_forms = {
        "weapon": CharacterSheetAddItemForm(
            item_type="weapon", item_template=sheet_template.weapon_template
        ),
        "equipment": CharacterSheetAddItemForm(
            item_type="equipment", item_template=sheet_template.equipment_template
        ),
        "consumable": CharacterSheetAddItemForm(
            item_type="consumable", item_template=sheet_template.consumable_template
        ),
        "quest_item": CharacterSheetAddItemForm(
            item_type="quest_item", item_template=sheet_template.quest_item_template
        ),
    }

    return render(request, "charsheet_maker_app/character_sheet_detail.html", 
    context={"character_sheet": character_sheet,
             "sheet_template": sheet_template, 
             "form_without_items": form_without_items,
             "add_item_forms": add_item_forms,
             "item_sets": {
                "weapon": character_sheet.weapons,
                "equipment": character_sheet.equipments,
                "consumable": character_sheet.consumables,
                "quest_item": character_sheet.quest_items                 
             }})

@login_required
def SheetTemplateCreateView(request):
    
    if request.method == 'GET':
        
        form = SheetTemplateForm()
        return render(request, "charsheet_maker_app/sheet_template_create.html", 
                      {"form": form})

    else:

        form = SheetTemplateForm(request.POST)
        if form.is_valid():

            fields_error_messages = validate_sheet_template_form_input_content(
                form_cleaned_data=form.cleaned_data
            )

            # Will contain contents validation errors 
            # and mantain the values the user tried to send;
            if len(fields_error_messages) != 0:
                return render(request, "charsheet_maker_app/sheet_template_create.html", 
                              {"form": form, "fields_error_messages": fields_error_messages})

            # Success cycle end. Go to templates page;
            instance = form.save(commit=False)
            instance.sheet_template_owner = request.user
            instance.save()
            return redirect(reverse("charsheet_maker_app:index"))

        # Will contain basic validation errors (from django built-in form), 
        # and mantain the values the user tried to send;
        return render(request, "charsheet_maker_app/sheet_template_create.html", 
                      {"form": form})

@login_required
def CharacterSheetCreateView(request, template_id):

    sheet_template = get_object_or_404(SheetTemplate, id=template_id, sheet_template_owner=request.user)

    if request.method == 'GET':

        form = CharacterSheetCreateForm()
        return render(request, "charsheet_maker_app/character_sheet_create.html",
                      {"sheet_template": sheet_template,
                       "form": form})

    else:

        form = CharacterSheetCreateForm(request.POST)
        if form.is_valid():

            # Success. Create charsheet with default values, except for name,
            # and show charsheet list updated;

            background = {}
            for backgrd in sheet_template.background:
                background[backgrd] = ""

            attributes = {}
            for attr in sheet_template.attributes:
                attributes[attr] = 0

            stats = {}
            for key, default_value in sheet_template.stats.items():
                stats[key] = default_value

            CharacterSheet.objects.create(
                template=sheet_template,

                name=form.cleaned_data["name"],
                experience=0,
                level=0,
                gold=0,

                char_class=sheet_template.available_classes[0],
                race=sheet_template.available_races[0],
                background=background,
                attributes=attributes,

                stats=stats,

                weapons={},
                equipments={},
                consumables={},
                quest_items={},
            )

            return redirect(reverse("charsheet_maker_app:sheet_template_detail", args=(sheet_template.id,)))

        # Will contain basic validation errors (from django built-in form), 
        # and mantain the values the user tried to send;
        return render(request, "charsheet_maker_app/character_sheet_create.html", 
                      {"sheet_template": sheet_template,
                       "form": form})

@login_required
def CharacterSheetRemoveView(request, sheet_id):
    return HttpResponse("sheet removed!")

@login_required
def CharacterSheetAddItemView(request, sheet_id):

    character_sheet = get_object_or_404(CharacterSheet, id=sheet_id)
    sheet_template = character_sheet.template

    if request.POST["item_type"] == "weapon":

        form = CharacterSheetAddItemForm(item_type="weapon", 
            item_template=sheet_template.weapon_template, data=request.POST)
        new_item_data = get_item_data_from_add_item_form(form)
        if not (new_item_data is None):
        
            new_item_id = str(len(character_sheet.weapons))
            character_sheet.weapons[new_item_id] = new_item_data
            character_sheet.save()

    elif request.POST["item_type"] == "equipment":

        form = CharacterSheetAddItemForm(item_type="equipment",
            item_template=sheet_template.equipment_template, data=request.POST)
        new_item_data = get_item_data_from_add_item_form(form)
        if not (new_item_data is None):

            new_item_id = str(len(character_sheet.equipments))
            character_sheet.equipments[new_item_id] = new_item_data
            character_sheet.save()

    elif request.POST["item_type"] == "consumable":
        
        form = CharacterSheetAddItemForm(item_type="consumable",
            item_template=sheet_template.consumable_template, data=request.POST)
        new_item_data = get_item_data_from_add_item_form(form)
        if not (new_item_data is None):

            new_item_id = str(len(character_sheet.consumables))
            character_sheet.consumables[new_item_id] = new_item_data
            character_sheet.save()

    elif request.POST["item_type"] == "quest_item":
        
        form = CharacterSheetAddItemForm(item_type="quest_item",
            item_template=sheet_template.quest_item_template, data=request.POST)
        new_item_data = get_item_data_from_add_item_form(form)
        if not (new_item_data is None):

            new_item_id = str(len(character_sheet.quest_items))
            character_sheet.quest_items[new_item_id] = new_item_data
            character_sheet.save()

    else:
            
        return HttpResponseBadRequest()

    return redirect(reverse("charsheet_maker_app:character_sheet_detail", args=(sheet_id,)))

@login_required
def CharacterSheetRemoveItemView(request, sheet_id):
    
    character_sheet = get_object_or_404(CharacterSheet, id=sheet_id)

    print(request.body)

    if request.POST["item_type"] == "weapon":

        form = CharacterSheetRemoveItemForm(item_type="weapon", data=request.POST)
        item_id = get_item_id_from_remove_item_form(form)
        if not (item_id is None) and item_id in character_sheet.weapons:
            del character_sheet.weapons[item_id]
            character_sheet.save()

    elif request.POST["item_type"] == "equipment":

        form = CharacterSheetRemoveItemForm(item_type="equipment", data=request.POST)
        item_id = get_item_id_from_remove_item_form(form)
        if not (item_id is None) and item_id in character_sheet.equipments:
            del character_sheet.equipments[item_id]
            character_sheet.save()

    elif request.POST["item_type"] == "consumable":

        form = CharacterSheetRemoveItemForm(item_type="consumable", data=request.POST)
        item_id = get_item_id_from_remove_item_form(form)
        if not (item_id is None) and item_id in character_sheet.consumables:
            del character_sheet.consumables[item_id]
            character_sheet.save()

    elif request.POST["item_type"] == "quest_item":

        form = CharacterSheetRemoveItemForm(item_type="quest_item", data=request.POST)
        item_id = get_item_id_from_remove_item_form(form)
        if not (item_id is None) and item_id in character_sheet.quest_items:
            del character_sheet.quest_items[item_id]
            character_sheet.save()

    else:

        return HttpResponseBadRequest()
    
    return redirect(reverse("charsheet_maker_app:character_sheet_detail", args=(sheet_id,)))
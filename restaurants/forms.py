from django import forms

from hospital.models import Category, ComboMenu, ComposeIngredient, ComposePreparation, DetailsComboMenu, DetailsComposeIngredient, DetailsComposePreparation, Dish, DishPreparation, Hospital, Ingredient, Promotion, PromotionAction, PromotionRule, RecipeIngredient, StructureArticle, Type_patient
from rest_framework import serializers

class DishForm(forms.ModelForm):
    sync_version = forms.IntegerField(required=False)
    is_shared = forms.BooleanField(initial=False, required=False)  # Partagé entre structures
    category = forms.ModelChoiceField(required=False, queryset=Category.objects.all())
    name_language = forms.JSONField(required=False)
    preparation_time = forms.CharField(required=False)
    is_active = forms.BooleanField(initial=True, required=False)
    is_delivery = forms.BooleanField(initial=True, required=False)

    class Meta:
        model = Dish
        fields = ('sync_version','is_shared', 'preparation_time', 'name_language', 'is_active', 'is_delivery', 'category')

class DishPreparationForm(forms.ModelForm):
    sync_version = forms.IntegerField(required=False)
    is_shared = forms.BooleanField(initial=False, required=False)  # Partagé entre structures
    dish = forms.ModelChoiceField(required=False, queryset=Dish.objects.all())
    quantity = forms.CharField(required=False)

    class Meta:
        model = DishPreparation
        fields = ('sync_version', 'is_shared', 'dish', 'quantity')

class PromotionActionForm(forms.ModelForm):
    sync_version = forms.IntegerField(required=False)
    is_shared = forms.BooleanField(initial=False, required=False)  # Partagé entre structures
    promotion = forms.ModelChoiceField(required=False, queryset=Promotion.objects.all())
    action_type  = forms.CharField(required=False)
    value  = forms.CharField(required=False)

    class Meta:
        model = PromotionAction
        fields = ('sync_version','action_type', 'value', 'promotion')


class PromotionRuleForm(forms.ModelForm):
    sync_version = forms.IntegerField(required=False)
    is_shared = forms.BooleanField(initial=False, required=False)  # Partagé entre structures
    category = forms.ModelChoiceField(required=False, queryset=Category.objects.all())
    promotion = forms.ModelChoiceField(required=False, queryset=Promotion.objects.all())
    dish = forms.ModelChoiceField(required=False, queryset=Dish.objects.all())
    type_patient = forms.ModelChoiceField(required=False, queryset=Type_patient.objects.all())
    min_quantity   = forms.IntegerField(required=False)
    # modulo = forms.CharField(required=False)
    # modulo_equals  = forms.CharField(required=False)
    start_hour  = forms.CharField(required=False)
    end_hour   = forms.CharField(required=False)

    class Meta:
        model = PromotionRule
        fields = ('sync_version','start_hour', 'end_hour', 'promotion', 'min_quantity', 'dish', 'category', 'type_patient')


class PromotionForm(forms.ModelForm):
    sync_version = forms.IntegerField(required=False)
    is_shared = forms.BooleanField(initial=False, required=False)
    is_active = forms.BooleanField(initial=False, required=False)  # Partagé entre structures
    name_language = forms.JSONField(required=False)
    start_date  = forms.CharField(required=False)
    end_date  = forms.CharField(required=False)
    priority   = forms.CharField(required=False)
    cumulative    = forms.CharField(required=False)

    class Meta:
        model = Promotion
        fields = ('sync_version','is_active', 'name_language', 'start_date', 'end_date', 'priority', 'cumulative')

class IngredientForm(forms.ModelForm):
    sync_version = forms.IntegerField(required=False)
    threshold_min = forms.IntegerField(required=False)
    threshold_max = forms.IntegerField(required=False)
    name_language = forms.JSONField(required=False)
    unit = forms.CharField(required=True)
    stock_quantity = forms.FloatField(required=False)
    price_per_unit = forms.FloatField(required=False)
    is_delivery = forms.BooleanField(initial=True, required=False)

    class Meta:
        model = Ingredient
        fields = ('sync_version','name_language','threshold_min','threshold_max', 'unit', 'stock_quantity', 'price_per_unit', 'is_delivery')

class ComposeIngredientForm(forms.ModelForm):
    sync_version = forms.IntegerField(required=False)
    name_language = forms.JSONField(required=False)
    unit = forms.CharField(required=True)
    stock_quantity = forms.FloatField(required=False)
    price_per_unit = forms.FloatField(required=False)
    total_amount = forms.FloatField(required=False)
    is_shared = forms.BooleanField(initial=False, required=False)  # Partagé entre structures
    hospital = forms.ModelChoiceField(required=False, queryset=Hospital.objects.all())

    class Meta:
        model = ComposeIngredient
        fields = '__all__'
class ComboMenuForm(forms.ModelForm):
    sync_version = forms.IntegerField(required=False)
    name_language = forms.JSONField(required=False)
    is_shared = forms.BooleanField(initial=False, required=False)  # Partagé entre structures
    is_active = forms.BooleanField(initial=True, required=False)
    is_delivery = forms.BooleanField(initial=True, required=False)

    class Meta:
        model = ComboMenu
        fields = '__all__'
class ComposePreparationForm(forms.ModelForm):
    sync_version = forms.IntegerField(required=False)
    name_language = forms.JSONField(required=False)
    stock_quantity = forms.FloatField(required=False)
    total_amount = forms.DecimalField(
    required=False,
    max_digits=12,
    decimal_places=3
)
    is_shared = forms.BooleanField(initial=False, required=False)  # Partagé entre structures
    hospital = forms.ModelChoiceField(required=False, queryset=Hospital.objects.all())
    compose_ingredient = forms.ModelChoiceField(required=False, queryset=ComposeIngredient.objects.all())

    class Meta:
        model = ComposePreparation
        fields = '__all__'

class DetailsComposePreparationForm(forms.ModelForm):
    sync_version = forms.IntegerField(required=False)
    is_shared = forms.BooleanField(initial=False, required=False)  # Partagé entre structures
    hospital = forms.ModelChoiceField(required=False, queryset=Hospital.objects.all())
    ingredient = forms.ModelChoiceField(required=False, queryset=Ingredient.objects.all())
    compose_preparation = forms.ModelChoiceField(required=False, queryset=ComposePreparation.objects.all())

    class Meta:
        model = DetailsComposePreparation
        fields = '__all__'

class RecipeIngredientForm(forms.ModelForm):
    sync_version = forms.IntegerField(required=False)
    dish = forms.ModelChoiceField(queryset=Dish.objects.all(), required=True)
    item_uid = forms.CharField(required=True)
    quantity = forms.FloatField(required=True)

    class Meta:
        model = RecipeIngredient
        fields = ('sync_version','dish', 'quantity')

    def save(self, commit=True):
        instance = super().save(commit=False)

        uid = self.cleaned_data['item_uid']  # "ingredient-147"

        model_type, obj_id = uid.split('-')
        obj_id = int(obj_id)

        if model_type == "ingredient":
            instance.ingredient_id = obj_id
            instance.compose_ingredient = None

        elif model_type == "compose":
            instance.compose_ingredient_id = obj_id
            instance.ingredient = None

        if commit:
            instance.save()

        return instance
        
class DetailsComposeIngredientForm(forms.ModelForm):
    sync_version = forms.IntegerField(required=False)
    compose_ingredient = forms.ModelChoiceField(queryset=ComposeIngredient.objects.all(), required=True)
    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.all(), required=True)
    quantity = forms.FloatField(required=True)

    class Meta:
        model = DetailsComposeIngredient
        fields = ('sync_version','compose_ingredient', 'ingredient', 'quantity')
class DetailsComboMenuForm(forms.ModelForm):
    sync_version = forms.IntegerField(required=False)
    dish = forms.ModelChoiceField(queryset=Dish.objects.all(), required=True)
    quantity = forms.FloatField(required=True)

    class Meta:
        model = DetailsComboMenu
        fields = ('sync_version','dish', 'quantity')

class StructureArticleForm(forms.ModelForm):
    sync_version = forms.IntegerField(required=False)
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=False)
    price = forms.FloatField(required=True)
    is_active = forms.BooleanField(initial=True, required=False)
    item_uid = forms.CharField(required=True)

    class Meta:
        model = StructureArticle
        fields = ('sync_version','id','hospital', 'item_uid', 'price', 'is_active')
    

    def save(self, commit=True):
        instance = super().save(commit=False)

        uid = self.cleaned_data['item_uid']  # "ingredient-147"

        model_type, obj_id = uid.split('-')
        obj_id = int(obj_id)

        if model_type == "dish":
            instance.dish_id = obj_id
            instance.combo_menu = None

        elif model_type == "combo":
            instance.combo_menu_id = obj_id
            instance.dish = None

        if commit:
            instance.save()

        return instance

class DishPreparationForm(forms.ModelForm):
    sync_version = forms.IntegerField(required=False)
    dish = forms.ModelChoiceField(queryset=Dish.objects.all(), required=True)
    quantity = forms.IntegerField(min_value=1, required=True)

    class Meta:
        model = DishPreparation
        fields = ('sync_version','dish', 'quantity')

    # def clean(self):
    #     cleaned_data = super().clean()
    #     dish = cleaned_data.get('dish')
    #     quantity = cleaned_data.get('quantity')

    #     if dish and quantity:
    #         for ri in dish.recipe_ingredients.all():
    #             if ri.ingredient.stock_quantity < ri.quantity * quantity:
    #                 raise forms.ValidationError(
    #                     f"Stock insuffisant pour {ri.ingredient.name_language} "
    #                     f"({ri.ingredient.stock_quantity} disponible, "
    #                     f"{ri.quantity * quantity} nécessaire)"
    #                 )
    #     return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            instance.prepare()  # décrémente automatiquement le stock
        return instance
    


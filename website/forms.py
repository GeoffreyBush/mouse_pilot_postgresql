from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from website.constants import EARMARK_CHOICES_PAIRED

from .models import BreedingCage, Comment, CustomUser, Mouse, Project, Request, Strain


class ProjectMiceForm(forms.ModelForm):
    SEX_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]
    TRUE_OR_FALSE = [
        (False, "No"),
        (True, "Yes"),
    ]

    sex = forms.ChoiceField(
        choices=SEX_CHOICES, widget=forms.Select(attrs={"class": "form-select"})
    )
    dob = forms.DateField(
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
    )
    clippedDate = forms.DateField(
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
    )
    mother = forms.ModelChoiceField(queryset=Mouse.objects.all(), required=False, widget=forms.Select(attrs={"class": "form-select"}))
    father = forms.ModelChoiceField(queryset=Mouse.objects.all(), required=False, widget=forms.Select(attrs={"class": "form-select"}))
    project = forms.ModelChoiceField(queryset=Project.objects.all(), required=False, widget=forms.Select(attrs={"class": "form-select"}))
    genotyped = forms.ChoiceField(
        required=True, choices=TRUE_OR_FALSE, widget=forms.Select(attrs={"class": "form-select"})
    )
    earmark = forms.ChoiceField(choices=EARMARK_CHOICES_PAIRED, widget=forms.Select(attrs={"class": "form-select"}))
    genotyper = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(), required=False, widget=forms.Select(attrs={"class": "form-select"})
    )
    strain = forms.ModelChoiceField(queryset=Strain.objects.all(), required=False, widget=forms.Select(attrs={"class": "form-select"}))

    class Meta:
        model = Mouse
        fields = "__all__" 


class RepositoryMiceForm(forms.ModelForm):
    SEX_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]
    TRUE_OR_FALSE = [
        (False, "No"),
        (True, "Yes"),
    ]

    sex = forms.ChoiceField(
        choices=SEX_CHOICES, widget=forms.Select(attrs={"class": "form-select"})
    )
    dob = forms.DateField(
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
    )
    clippedDate = forms.DateField(
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
    )
    mother = forms.ModelChoiceField(queryset=Mouse.objects.all(), required=False, widget=forms.Select(attrs={"class": "form-select"}))
    father = forms.ModelChoiceField(queryset=Mouse.objects.all(), required=False, widget=forms.Select(attrs={"class": "form-select"}))
    project = forms.ModelChoiceField(queryset=Project.objects.all(), required=False, widget=forms.Select(attrs={"class": "form-select"}))
    genotyped = forms.ChoiceField(
        required=True, choices=TRUE_OR_FALSE, widget=forms.Select(attrs={"class": "form-select"})
    )
    earmark = forms.ChoiceField(choices=EARMARK_CHOICES_PAIRED, widget=forms.Select(attrs={"class": "form-select"}))
    genotyper = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(), required=False, widget=forms.Select(attrs={"class": "form-select"})
    )
    strain = forms.ModelChoiceField(queryset=Strain.objects.all(), required=False, widget=forms.Select(attrs={"class": "form-select"}))

    class Meta:
        model = Mouse
        fields = "__all__" 

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["comment_text"]
        labels = {"comment_text": ""}
        widgets = {
            "comment_text": forms.Textarea(attrs={"rows": 12, "cols": 20}),
        }


class CustomUserCreationForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username"}), label="Username"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email"}), label="Email"
    )
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")


class RequestForm(forms.ModelForm):

    # Override __init__() to filter mice by project
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop("project", None)
        super().__init__(*args, **kwargs)

        if self.project:
            self.fields["mice"].queryset = Mouse.objects.filter(project=self.project)
        else:
            self.fields["mice"].queryset = Mouse.objects.all()

    # Add checkbox for mice selection
    mice = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Request
        fields = ["mice", "task_type", "researcher", "new_message"]


class MouseSelectionForm(forms.ModelForm):

    # Override __init__() to filter mice by project
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop("project", None)
        super().__init__(*args, **kwargs)

        if self.project:
            self.fields["mice"].queryset = Mouse.objects.filter(project=self.project)
        else:
            self.fields["mice"].queryset = Mouse.objects.all()

    mice = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Mouse
        fields = ["id"]


class BreedingCageForm(forms.ModelForm):

    STATUS_CHOICE = [
        ("Empty", "Empty"),
        ("ParentsInside", "ParentsInside"),
        ("ParentsRemoved", "ParentsRemoved"),
    ]

    box_no = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "---"}), label="Box Number"
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICE, widget=forms.Select(), label="Status"
    )
    mother = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Female ID"}), label="Mother"
    )
    father = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Male ID"}), label="Father"
    )
    date_born = forms.DateField(
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        label="DBorn",
    )
    number_born = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "NBorn"}), label="NBorn"
    )
    cull_to = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "C/To"}), label="C/To"
    )
    date_wean = forms.DateField(
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        label="DWean",
    )
    number_wean = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "NWean"}), label="NWean"
    )
    pwl = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "NBorn - NWean"}), label="PWL"
    )

    class Meta:
        model = BreedingCage
        fields = "__all__"


class BreedingPairForm(forms.ModelForm):
    box_no = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "---"}), label="Box Number"
    )
    mother = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Female ID"}), label="Mother"
    )
    father = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Male ID"}), label="Father"
    )

    class Meta:
        model = BreedingCage
        fields = ["box_no", "mother", "father"]

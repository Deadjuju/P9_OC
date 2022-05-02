from django import forms

from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image', ]


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (0, "- 0"), (1, "- 1"), (2, "- 2"), (3, "- 3"), (4, "- 4"), (5, "- 5")
    ]
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=RATING_CHOICES)

    class Meta:
        model = models.Review
        fields = ["rating", "headline", "body", ]


class SubscriberForm(forms.ModelForm):
    followed_user = forms.CharField(max_length=256,
                                    widget=forms.TextInput(attrs={"placeholder": " Nom d'utilisateur "}))

    class Meta:
        model = models.UserFollows
        fields = ["followed_user", ]

    def clean(self):
        cleaned_data = super(SubscriberForm, self).clean()
        followed_user = cleaned_data.get('followed_user')
        if models.UserFollows.objects.filter(followed_user=followed_user).exists():
            raise forms.ValidationError('Category already exists')

    # def clean(self):
    #     cleaned_data = super(SubscriberForm, self).clean()
    #     followed_user = cleaned_data.get('followed_user')
    #     if models.UserFollows.objects.filter(followed_user=followed_user).exists():
    #         raise forms.ValidationError('Category already exists')


# class SubscriberForm(forms.Form):
#     followed_user = forms.CharField(max_length=256,
#                                     widget=forms.TextInput(attrs={"placeholder": " Nom d'utilisateur "}))
#     model = models.UserFollows
#
#     def save(self, user, followed_user):
#         # user_to_follow = self.cleaned_data["followed_user"]
#         new_follow = self.model.objects.create(user=user, followed_user=followed_user)
#         return new_follow
#
#
#     class Meta:
#         models = models.UserFollows
#         fields = ["followed_user", ]

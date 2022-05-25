from django import forms
from .models import Watchlist


class WatchlistForm(forms.ModelForm):

    class Meta:
        model = Watchlist
        fields = ('state', 'district', 'municipality', 'ward_no', 'property_type')
        widgets = {
            'state': forms.TextInput(attrs={'placeholder':'State'}),
            'district': forms.TextInput(attrs={'placeholder': 'District'}),
            'municipality': forms.TextInput(attrs={'placeholder': 'Municipality'}),
            'ward_no': forms.TextInput(attrs={'placeholder': 'Ward No.'}),
        }

    def __init__(self, *args, **kwargs):
        super(WatchlistForm, self).__init__(*args, **kwargs)
        self.fields['property_type'].empty_label = 'Select'
        self.fields['state'].label = False
        self.fields['district'].label = False
        self.fields['municipality'].label = False
        self.fields['ward_no'].label = False
        self.fields['property_type'].label = False

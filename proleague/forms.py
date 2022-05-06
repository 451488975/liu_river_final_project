from django import forms

from .models import Tournament, Match, Player, Team, Game, School


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = '__all__'

    def clean_tournament_name(self):
        return self.cleaned_data['tournament_name'].strip()


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = '__all__'

    def clean_game_name(self):
        return self.cleaned_data['game_name'].strip()

    def clean_genre(self):
        return self.cleaned_data['genre'].strip()


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = '__all__'

    def clean_team_name(self):
        return self.cleaned_data['team_name'].strip()

    def clean_acronym(self):
        return self.cleaned_data['acronym'].strip()


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = '__all__'

    def clean_match_type(self):
        return self.cleaned_data['match_type'].strip()

    def clean_video_link(self):
        return self.cleaned_data['video_link'].strip()


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'

    def clean_school_name(self):
        return self.cleaned_data['school_name'].strip()

    def clean_city(self):
        return self.cleaned_data['city'].strip()

    def clean_state(self):
        return self.cleaned_data['state'].strip()


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = '__all__'

    def clean_player_name(self):
        return self.cleaned_data['player_name'].strip()

    def clean_email(self):
        return self.cleaned_data['email'].strip()

    def clean_gamer_tag(self):
        return self.cleaned_data['gamer_tag'].strip()

    def clean_phone_number(self):
        return self.cleaned_data['phone_number'].strip()

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from itertools import chain

from .utils import PageLinksMixin
from .forms import TournamentForm, MatchForm, PlayerForm, TeamForm, GameForm, SchoolForm
from .models import Tournament, Match, Player, Team, Game, School


class TournamentList(ListView):
    model = Tournament


class TournamentDetail(DetailView):
    model = Tournament

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        tournament = self.get_object()
        team_list = tournament.teams.all()
        game = tournament.game
        context['team_list'] = team_list
        context['game'] = game
        return context


class TournamentCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = TournamentForm
    model = Tournament
    permission_required = 'proleague.add_tournament'


class TournamentUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = TournamentForm
    model = Tournament
    template_name = 'proleague/tournament_form_update.html'
    permission_required = 'proleague.change_tournament'


class TournamentDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Tournament
    success_url = reverse_lazy('proleague_tournament_list_urlpattern')
    permission_required = 'proleague.delete_tournament'

    def get(self, request, pk):
        tournament = get_object_or_404(Tournament, pk=pk)
        teams = tournament.teams.all()
        if teams.count() > 0:
            return render(
                request,
                'proleague/tournament_refuse_delete.html',
                {
                    'tournament': tournament,
                    'teams': teams,
                }
            )
        else:
            return render(
                request,
                'proleague/tournament_confirm_delete.html',
                {'tournament': tournament}
            )


class MatchList(PageLinksMixin, ListView):
    paginate_by = 25
    model = Match


class MatchDetail(DetailView):
    model = Match

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        match = self.get_object()
        team_a = match.team_a
        team_b = match.team_b
        context['team_a'] = team_a
        context['team_b'] = team_b
        return context


class MatchCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = MatchForm
    model = Match
    permission_required = 'proleague.add_match'


class MatchUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = MatchForm
    model = Match
    template_name = 'proleague/match_form_update.html'
    permission_required = 'proleague.change_match'


class MatchDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Tournament
    success_url = reverse_lazy('proleague_match_list_urlpattern')
    permission_required = 'proleague.delete_match'


class GameList(ListView):
    model = Game


class GameDetail(DetailView):
    model = Game

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        game = self.get_object()
        tournament_list = game.tournaments.all()
        context['tournament_list'] = tournament_list
        return context


class GameCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = GameForm
    model = Game
    permission_required = 'proleague.add_game'


class GameUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = GameForm
    model = Game
    template_name = 'proleague/game_form_update.html'
    permission_required = 'proleague.change_game'


class GameDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Game
    success_url = reverse_lazy('proleague_game_list_urlpattern')
    permission_required = 'proleague.delete_game'

    def get(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        tournaments = game.tournaments.all()
        if tournaments.count() > 0:
            return render(
                request,
                'proleague/game_refuse_delete.html',
                {
                    'game': game,
                    'tournaments': tournaments,
                }
            )
        else:
            return render(
                request,
                'proleague/game_confirm_delete.html',
                {'game': game}
            )


class TeamList(PageLinksMixin, ListView):
    paginate_by = 25
    model = Team


class TeamDetail(DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        team = self.get_object()
        match_a = team.match_a.all()
        match_b = team.match_b.all()
        match_list = list(chain(match_a, match_b))
        player_list = team.players.all()
        tournament = team.tournament
        position = team.position
        context['match_list'] = match_list
        context['player_list'] = player_list
        context['tournament'] = tournament
        context['position'] = position
        return context


class TeamCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = TeamForm
    model = Team
    permission_required = 'proleague.add_team'


class TeamUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = TeamForm
    model = Team
    template_name = 'proleague/team_form_update.html'
    permission_required = 'proleague.change_team'


class TeamDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Team
    success_url = reverse_lazy('proleague_team_list_urlpattern')
    permission_required = 'proleague.delete_team'

    def get(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        match_a = team.match_a.all()
        match_b = team.match_b.all()
        matches = list(chain(match_a, match_b))
        players = team.players.all()
        if len(matches) > 0:
            return render(
                request,
                'proleague/team_refuse_delete_matches.html',
                {
                    'team': team,
                    'matches': matches,
                }
            )
        elif players.count() > 0:
            return render(
                request,
                'proleague/team_refuse_delete_players.html',
                {
                    'team': team,
                    'players': players,
                }
            )
        else:
            return render(
                request,
                'proleague/team_confirm_delete.html',
                {'team': team}
            )


class SchoolList(ListView):
    model = School


class SchoolDetail(DetailView):
    model = School

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        school = self.get_object()
        player_list = school.players.all()
        context['player_list'] = player_list
        return context


class SchoolCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = SchoolForm
    model = School
    permission_required = 'proleague.add_school'


class SchoolUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = SchoolForm
    model = School
    template_name = 'proleague/school_form_update.html'
    permission_required = 'proleague.change_school'


class SchoolDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = School
    success_url = reverse_lazy('proleague_school_list_urlpattern')
    permission_required = 'proleague.delete_school'

    def get(self, request, pk):
        school = get_object_or_404(School, pk=pk)
        players = school.players.all()
        if players.count() > 0:
            return render(
                request,
                'proleague/school_refuse_delete.html',
                {
                    'school': school,
                    'players': players,
                }
            )
        else:
            return render(
                request,
                'proleague/school_confirm_delete.html',
                {'school': school}
            )


class PlayerList(PageLinksMixin, ListView):
    paginate_by = 25
    model = Player


class PlayerDetail(DetailView):
    model = Player

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        player = self.get_object()
        school = player.school
        team = player.team
        context['school'] = school
        context['team'] = team
        return context


class PlayerCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PlayerForm
    model = Player
    permission_required = 'proleague.add_player'


class PlayerUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PlayerForm
    model = Player
    template_name = 'proleague/player_form_update.html'
    permission_required = 'proleague.change_player'


class PlayerDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Player
    success_url = reverse_lazy('proleague_player_list_urlpattern')
    permission_required = 'proleague.delete_player'

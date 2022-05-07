from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from itertools import chain

from .utils import PageLinksMixin
from .forms import TournamentForm, MatchForm, PlayerForm, TeamForm, GameForm, SchoolForm
from .models import Tournament, Match, Player, Team, Game, School


class TournamentList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Tournament
    permission_required = 'proleague.view_tournament'


class TournamentDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Tournament
    permission_required = 'proleague.view_tournament'

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


class MatchList(LoginRequiredMixin, PermissionRequiredMixin, PageLinksMixin, ListView):
    paginate_by = 25
    model = Match
    permission_required = 'proleague.view_match'


class MatchDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Match
    permission_required = 'proleague.view_match'

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
    model = Match
    success_url = reverse_lazy('proleague_match_list_urlpattern')
    permission_required = 'proleague.delete_match'


class MatchSearch(LoginRequiredMixin, PermissionRequiredMixin, View):
    page_kwarg = 'page'
    paginate_by = 25
    template_name = 'proleague/match_search_result.html'
    permission_required = 'proleague.view_match'

    def get(self, request):
        keyword = request.GET.get('match_search')
        match_list = Match.objects.filter(
            Q(match_type__icontains=keyword) |
            Q(team_a__team_name__icontains=keyword) |
            Q(team_b__team_name__icontains=keyword) |
            Q(team_a__tournament__tournament_name__icontains=keyword)
        )
        paginator = Paginator(
            match_list,
            self.paginate_by
        )
        page_number = request.GET.get(
            self.page_kwarg
        )
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        if page.has_previous():
            prev_url = "?match_search={kwd}&{pkw}={n}".format(
                kwd=keyword,
                pkw=self.page_kwarg,
                n=page.previous_page_number()
            )
        else:
            prev_url = None
        if page.has_next():
            next_url = "?match_search={kwd}&{pkw}={n}".format(
                kwd=keyword,
                pkw=self.page_kwarg,
                n=page.next_page_number()
            )
        else:
            next_url = None
        context = {
            'is_paginated': page.has_other_pages(),
            'next_page_url': next_url,
            'paginator': paginator,
            'previous_page_url': prev_url,
            'match_list': page,
            'kwd': keyword
        }
        return render(
            request, self.template_name, context
        )


class GameList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Game
    permission_required = 'proleague.view_game'


class GameDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Game
    permission_required = 'proleague.view_game'

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


class TeamList(LoginRequiredMixin, PermissionRequiredMixin, PageLinksMixin, ListView):
    paginate_by = 25
    model = Team
    permission_required = 'proleague.view_team'


class TeamDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Team
    permission_required = 'proleague.view_team'

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


class TeamSearch(LoginRequiredMixin, PermissionRequiredMixin, View):
    page_kwarg = 'page'
    paginate_by = 25
    template_name = 'proleague/team_search_result.html'
    permission_required = 'proleague.view_team'

    def get(self, request):
        keyword = request.GET.get('team_search')
        team_list = Team.objects.filter(
            Q(team_name__icontains=keyword) |
            Q(acronym__icontains=keyword)
        ).distinct()
        paginator = Paginator(
            team_list,
            self.paginate_by
        )
        page_number = request.GET.get(
            self.page_kwarg
        )
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        if page.has_previous():
            prev_url = "?team_search={kwd}&{pkw}={n}".format(
                kwd=keyword,
                pkw=self.page_kwarg,
                n=page.previous_page_number()
            )
        else:
            prev_url = None
        if page.has_next():
            next_url = "?team_search={kwd}&{pkw}={n}".format(
                kwd=keyword,
                pkw=self.page_kwarg,
                n=page.next_page_number()
            )
        else:
            next_url = None
        context = {
            'is_paginated': page.has_other_pages(),
            'next_page_url': next_url,
            'paginator': paginator,
            'previous_page_url': prev_url,
            'team_list': page,
            'kwd': keyword
        }
        return render(
            request, self.template_name, context
        )


class SchoolList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = School
    permission_required = 'proleague.view_team'


class SchoolDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = School
    permission_required = 'proleague.view_team'

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


class PlayerList(LoginRequiredMixin, PermissionRequiredMixin, PageLinksMixin, ListView):
    paginate_by = 25
    model = Player
    permission_required = 'proleague.view_player'


class PlayerDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Player
    permission_required = 'proleague.view_player'

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


class PlayerSearch(LoginRequiredMixin, PermissionRequiredMixin, View):
    page_kwarg = 'page'
    paginate_by = 25
    template_name = 'proleague/player_search_result.html'
    permission_required = 'proleague.view_player'

    def get(self, request):
        keyword = request.GET.get('player_search')
        player_list = Player.objects.filter(
            Q(player_name__icontains=keyword) |
            Q(gamer_tag__icontains=keyword)
        ).distinct()
        paginator = Paginator(
            player_list,
            self.paginate_by
        )
        page_number = request.GET.get(
            self.page_kwarg
        )
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        if page.has_previous():
            prev_url = "?player_search={kwd}&{pkw}={n}".format(
                kwd=keyword,
                pkw=self.page_kwarg,
                n=page.previous_page_number()
            )
        else:
            prev_url = None
        if page.has_next():
            next_url = "?player_search={kwd}&{pkw}={n}".format(
                kwd=keyword,
                pkw=self.page_kwarg,
                n=page.next_page_number()
            )
        else:
            next_url = None
        context = {
            'is_paginated': page.has_other_pages(),
            'next_page_url': next_url,
            'paginator': paginator,
            'previous_page_url': prev_url,
            'player_list': page,
            'kwd': keyword
        }
        return render(
            request, self.template_name, context
        )


class SignUp(FormView):
    template_name = 'proleague/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('about_urlpattern')

    def form_valid(self, form):
        # save the new user first
        form.save()
        # get the username and password
        username = self.request.POST['username']
        password = self.request.POST['password1']
        # authenticate user then login
        user = authenticate(username=username, password=password)
        login(self.request, user)
        group = Group.objects.get(name='pl_user')
        user.groups.add(group)
        return HttpResponseRedirect(self.get_success_url())
#
#
# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             group = Group.objects.get(name='pl_user')
#
#             return redirect('login_urlpattern')
#     else:
#         form = UserCreationForm()
#     return render(
#         request,
#         'proleague/signup.html',
#         {
#             'form': form
#         }
#     )

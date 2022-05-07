from django.urls import path

from .views import (
    TournamentList, TournamentCreate, TournamentDelete, TournamentDetail, TournamentUpdate,
    GameList, GameCreate, GameDelete, GameDetail, GameUpdate,
    PlayerList, PlayerCreate, PlayerDelete, PlayerDetail, PlayerUpdate, PlayerSearch,
    MatchList, MatchCreate, MatchDelete, MatchDetail, MatchUpdate, MatchSearch,
    TeamList, TeamCreate, TeamDelete, TeamDetail, TeamUpdate, TeamSearch,
    SchoolList, SchoolCreate, SchoolDelete, SchoolDetail, SchoolUpdate
)


urlpatterns = [
    path(
        'tournament/',
        TournamentList.as_view(),
        name='proleague_tournament_list_urlpattern'
    ),

    path(
        'tournament/<int:pk>/',
        TournamentDetail.as_view(),
        name='proleague_tournament_detail_urlpattern'
    ),

    path(
        'tournament/create/',
        TournamentCreate.as_view(),
        name='proleague_tournament_create_urlpattern'
    ),

    path(
        'tournament/<int:pk>/update/',
        TournamentUpdate.as_view(),
        name='proleague_tournament_update_urlpattern'
    ),

    path(
        'tournament/<int:pk>/delete/',
        TournamentDelete.as_view(),
        name='proleague_tournament_delete_urlpattern'
    ),

    path(
        'game/',
        GameList.as_view(),
        name='proleague_game_list_urlpattern'
    ),

    path(
        'game/<int:pk>/',
        GameDetail.as_view(),
        name='proleague_game_detail_urlpattern'
    ),

    path(
        'game/create/',
        GameCreate.as_view(),
        name='proleague_game_create_urlpattern'
    ),

    path(
        'game/<int:pk>/update/',
        GameUpdate.as_view(),
        name='proleague_game_update_urlpattern'
    ),

    path(
        'game/<int:pk>/delete/',
        GameDelete.as_view(),
        name='proleague_game_delete_urlpattern'
    ),

    path(
        'player/',
        PlayerList.as_view(),
        name='proleague_player_list_urlpattern'
    ),

    path(
        'player/<int:pk>/',
        PlayerDetail.as_view(),
        name='proleague_player_detail_urlpattern'
    ),

    path(
        'player/create/',
        PlayerCreate.as_view(),
        name='proleague_player_create_urlpattern'
    ),

    path(
        'player/<int:pk>/update/',
        PlayerUpdate.as_view(),
        name='proleague_player_update_urlpattern'
    ),

    path(
        'player/<int:pk>/delete/',
        PlayerDelete.as_view(),
        name='proleague_player_delete_urlpattern'
    ),

    path(
        'player/search/',
        PlayerSearch.as_view(),
        name='proleague_player_search_urlpattern'
    ),

    path(
        'match/',
        MatchList.as_view(),
        name='proleague_match_list_urlpattern'
    ),

    path(
        'match/<int:pk>/',
        MatchDetail.as_view(),
        name='proleague_match_detail_urlpattern'
    ),

    path(
        'match/create/',
        MatchCreate.as_view(),
        name='proleague_match_create_urlpattern'
    ),

    path(
        'match/<int:pk>/update/',
        MatchUpdate.as_view(),
        name='proleague_match_update_urlpattern'
    ),

    path(
        'match/<int:pk>/delete/',
        MatchDelete.as_view(),
        name='proleague_match_delete_urlpattern'
    ),

    path(
        'match/search/',
        MatchSearch.as_view(),
        name='proleague_match_search_urlpattern'
    ),

    path(
        'team/',
        TeamList.as_view(),
        name='proleague_team_list_urlpattern'
    ),

    path(
        'team/<int:pk>/',
        TeamDetail.as_view(),
        name='proleague_team_detail_urlpattern'
    ),

    path(
        'team/create/',
        TeamCreate.as_view(),
        name='proleague_team_create_urlpattern'
    ),

    path(
        'team/<int:pk>/update/',
        TeamUpdate.as_view(),
        name='proleague_team_update_urlpattern'
    ),

    path(
        'team/<int:pk>/delete/',
        TeamDelete.as_view(),
        name='proleague_team_delete_urlpattern'
    ),

    path(
        'team/search/',
        TeamSearch.as_view(),
        name='proleague_team_search_urlpattern'
    ),

    path(
        'school/',
        SchoolList.as_view(),
        name='proleague_school_list_urlpattern'
    ),

    path(
        'school/<int:pk>/',
        SchoolDetail.as_view(),
        name='proleague_school_detail_urlpattern'
    ),

    path(
        'school/create/',
        SchoolCreate.as_view(),
        name='proleague_school_create_urlpattern'
    ),

    path(
        'school/<int:pk>/update/',
        SchoolUpdate.as_view(),
        name='proleague_school_update_urlpattern'
    ),

    path(
        'school/<int:pk>/delete/',
        SchoolDelete.as_view(),
        name='proleague_school_delete_urlpattern'
    ),
]

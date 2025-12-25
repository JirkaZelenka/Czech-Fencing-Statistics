from dash.dependencies import Input, Output
import dash
import pandas as pd

from apps.layout import eliminations_figure

def register_callbacks(
    app, runner,
    df_clubs, df_duels, df_events, df_fencers, df_tournaments,
    df_tournament_results, df_duels_prep, df_tournament_results_prep
):
    
    
    @app.callback(
        Output('fencers-table', 'data'),
        Output('output-fencers-filtered-number', 'children'),
        Output('filter-fencers-name', 'options'),
        Output('filter-fencers-club', 'options'),
        Output('filter-fencers-country', 'options'),
        Output('filter-fencers-gender', 'options'),
        Output('filter-fencers-birthyear', 'options'),

        Input('filter-fencers-name', 'value'),
        Input('filter-fencers-club', 'value'),
        Input('filter-fencers-country', 'value'),
        Input('filter-fencers-gender', 'value'),
        Input('filter-fencers-birthyear', 'value'),
    )
    def refresh_fencers(
        selected_names, selected_clubs, selected_countries,
        selected_genders, selected_birthyears
    ):
        
        #TODO: rozmyslet zda tu dám prep funkci bokem
        data = pd.merge(
            df_fencers, df_clubs[['id', 'name', "website"]],
            left_on='club_id', right_on='id', how='left',
            suffixes=('', '_club')
        )
        # Rename club name column if it exists (suffix applied only if there's a conflict)
        if 'name_club' in data.columns:
            data = data.rename(columns={'name_club': 'club_name'})
        elif 'name' in data.columns and 'name' in df_clubs.columns:
            # If no conflict, the club name might be in a different column - check if we need to rename
            # For now, assume club name is already correctly named or handle separately
            pass
        
        # Apply filters
        if selected_names:
            data = data[data['name'].isin(selected_names)]
        if selected_clubs:
            data = data[data['club_name'].isin(selected_clubs)]
        if selected_countries:
            data = data[data['country'].isin(selected_countries)]
        if selected_genders:
            data = data[data['gender'].isin(selected_genders)]
        if selected_birthyears:
            data = data[data['birthyear'].isin(selected_birthyears)]

        #? bohužel neexistuje link na fencera, jen na klub (vlastní URL)   
        #data['name_url'] = data['name'].apply(lambda x: f"[{x}](https://www.czechfencing.cz/)")
        def create_club_url(row):
            if pd.notna(row['website']) and row['website']:
                return f"[{row['club_name']}]({row['website']})"
            return f"[{row['club_name']}](https://www.czechfencing.cz/)"
        
        data['name_url'] = data.apply(create_club_url, axis=1)
         
        def make_options(series):
            return [{"label": v, "value": v} for v in sorted(series.dropna().unique())]

        names_opts = make_options(data["name"])
        clubs_opts = make_options(data["club_name"])
        countries_opts = make_options(data["country"])
        genders_opts = make_options(data["gender"])
        birthyears_opts = make_options(data["birthyear"])

        data = data.sort_values(by='name', ascending=True)
        data = data.to_dict('records')
            
        message_count_fencers = f"{len(data)} records"
            
        return (data,
                message_count_fencers,
                names_opts,
                clubs_opts,
                countries_opts,
                genders_opts,
                birthyears_opts
               )
        
    @app.callback(
        Output('filter-fencers-name', 'value'),
        Output('filter-fencers-club', 'value'),
        Output('filter-fencers-country', 'value'),
        Output('filter-fencers-gender', 'value'),
        Output('filter-fencers-birthyear', 'value'),
        Input('reset-fencers-filters-button', 'n_clicks'),
        prevent_initial_call=True  # so it doesn't fire on page load
    )
    def reset_fencers_filters(n_clicks):
        if n_clicks:
            # Returning None clears multi-select dropdowns
            return None, None, None, None, None
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        
    
    @app.callback(
        Output('clubs-table', 'data'),
        Output('output-clubs-filtered-number', 'children'),
        Output('filter-clubs-name', 'options'),
        Output('filter-clubs-city', 'options'),

        Input('filter-clubs-name', 'value'),
        Input('filter-clubs-city', 'value'),
    )
    def refresh_clubs(selected_names, selected_cities):
        
        data = df_clubs
        
        # Apply filters
        if selected_names:
            data = data[data['name'].isin(selected_names)]
        if selected_cities:
            data = data[data['city'].isin(selected_cities)]

        data['name_url'] = data.apply(lambda row: f"[{row['name']}]({row['website']})", axis=1)
            
        def make_options(series):
            return [{"label": v, "value": v} for v in sorted(series.dropna().unique())]

        clubs_opts = make_options(data["name"])
        cities_opts = make_options(data["city"])

        data = data.sort_values(by='name', ascending=True)
        data = data.to_dict('records')
            
        message_count_clubs = f"{len(data)} records"
            
        return (data,
                message_count_clubs,
                clubs_opts,
                cities_opts
               )    
        
    @app.callback(
        Output('filter-clubs-name', 'value'),
        Output('filter-clubs-city', 'value'),
        Input('reset-clubs-filters-button', 'n_clicks'),
        prevent_initial_call=True  # so it doesn't fire on page load
    )
    def reset_clubs_filters(n_clicks):
        if n_clicks:
            # Returning None clears multi-select dropdowns
            return None, None
        return dash.no_update, dash.no_update
                  
    
    @app.callback(
        #? data = DF, children = whatever?, options = list, value = number?
        #? zároven u reetu, kdy vracím empty filter, tak None je zjevně value a ne option
        Output('duels-table', 'data'),
        Output('output-duels-filtered-number', 'children'),
        #Input('refresh-duels-button', 'n_clicks'),
        Output('filter-duels-tournament', 'options'),
        Output('filter-duels-date', 'options'),
        Output('filter-duels-winner', 'options'),
        Output('filter-duels-winner-club', 'options'),
        Output('filter-duels-loser', 'options'),
        Output('filter-duels-loser-club', 'options'),
        Output('filter-duels-fight-lvl', 'options'),
        Output('filter-duels-gender', 'options'),

        Input('filter-duels-tournament', 'value'),
        Input('filter-duels-date', 'value'),
        Input('filter-duels-winner', 'value'),
        Input("filter-duels-winner-club", "value"),
        Input('filter-duels-loser', 'value'),
        Input("filter-duels-loser-club", "value"),
        Input("filter-duels-fight-lvl", "value"),
        Input("filter-duels-gender", "value")
    )
    def refresh_duels(
        selected_tournaments, selected_dates, selected_winners,
        selected_winner_clubs, selected_losers, selected_loser_clubs,
        selected_fight_lvl, selected_gender
    ):

        #? ale stále, df_duels_prep jde na filtry, ale tady to přepočíává znova??        
        data = df_duels_prep
            
        # Apply filters
        if selected_tournaments:
            data = data[data['name_tournament'].isin(selected_tournaments)]
        if selected_dates:
            data = data[data['date'].isin(selected_dates)]
        if selected_winners:
            data = data[data['name_fencer_winner'].isin(selected_winners)]
        if selected_winner_clubs:
            data = data[data['name_club_winner'].isin(selected_winner_clubs)]
        if selected_losers:
            data = data[data['name_fencer_loser'].isin(selected_losers)]
        if selected_loser_clubs:
            data = data[data['name_club_loser'].isin(selected_loser_clubs)]
        if selected_fight_lvl:
            data = data[data['type'].isin(selected_fight_lvl)]
        if selected_gender:
            data = data[data['gender'].isin(selected_gender)]

        def make_options(series):
            return [{"label": v, "value": v} for v in sorted(series.dropna().unique())]

        tournament_opts = make_options(data["name_tournament"])
        date_opts = make_options(data["date"])
        winner_opts = make_options(data["name_fencer_winner"])
        winner_club_opts = make_options(data["name_club_winner"])
        loser_opts = make_options(data["name_fencer_loser"])
        loser_club_opts = make_options(data["name_club_loser"])
        fight_lvl_opts = make_options(data["type"])
        gender_opts = make_options(data["gender"])

        #data = data.sort_values(by='date')
        data = data.to_dict('records')
            
        message_count_duels = f"{len(data)} records"
        
        return (data,
                message_count_duels,
                tournament_opts,
                date_opts,
                winner_opts,
                winner_club_opts,
                loser_opts,
                loser_club_opts,
                fight_lvl_opts,
                gender_opts
               )
        
    @app.callback(
        Output('filter-duels-tournament', 'value'),
        Output('filter-duels-date', 'value'),
        Output('filter-duels-winner', 'value'),
        Output('filter-duels-winner-club', 'value'),
        Output('filter-duels-loser', 'value'),
        Output('filter-duels-loser-club', 'value'),
        Output('filter-duels-fight-lvl', 'value'),
        Output('filter-duels-gender', 'value'),
        Input('reset-duels-filters-button', 'n_clicks'),
        prevent_initial_call=True  # so it doesn't fire on page load
    )
    def reset_duels_filters(n_clicks):
        if n_clicks:
            # Returning None clears multi-select dropdowns
            return None, None, None, None, None, None, None, None
        return (
            dash.no_update, dash.no_update, dash.no_update, dash.no_update,
            dash.no_update, dash.no_update, dash.no_update, dash.no_update
        )


    @app.callback(
        Output('tournament-results-table', 'data'),
        Output('output-tournament-results-filtered-number', 'children'),
        Output('filter-tournament-results-name', 'options'),
        Output('filter-tournament-results-date', 'options'),
        Output('filter-tournament-results-fencer', 'options'),
        Output('filter-tournament-results-club', 'options'),
        Output('filter-tournament-results-final-rank', 'options'),
        Output('filter-tournament-results-percentile', 'options'),

        Input('filter-tournament-results-name', 'value'),
        Input('filter-tournament-results-date', 'value'),
        Input('filter-tournament-results-fencer', 'value'),
        Input('filter-tournament-results-club', 'value'),
        Input('filter-tournament-results-final-rank', 'value'),
        Input('filter-tournament-results-percentile', 'value'),
    )
    def refresh_tournament_results(
        selected_names, selected_dates, selected_fencers,
        selected_clubs, selected_final_ranks, selected_percentiles
    ):

        #TODO: asi potřebuju plus clubs, events
        data = df_tournament_results_prep.copy()
        
        #TODO: move this to prep in runner?
        data["final_rank"] = pd.to_numeric(data["final_rank"], errors='coerce')
        data["ts"] = pd.to_numeric(data["ts"], errors='coerce')
        data["tr"] = pd.to_numeric(data["tr"], errors='coerce')
        data["score_index"] = data["ts"]-data["tr"]
            
        # Apply filters
        #TODO:
        if selected_names:
            data = data[data['name'].isin(selected_names)]
        #TODO:
        if selected_dates:
            data = data[data['date'].isin(selected_dates)]
        #TODO:
        if selected_fencers:
            data = data[data['fencer_name_to_check'].isin(selected_fencers)]
        #TODO:
        if selected_clubs:
            data = data[data['club_name_to_check'].isin(selected_clubs)]
        if selected_final_ranks:
            data = data[data['final_rank'].isin(selected_final_ranks)]
        if selected_percentiles:
            data = data[data['percentile'].isin(selected_percentiles)]

        def make_options(series):
            return [{"label": v, "value": v} for v in sorted(series.dropna().unique())]

        #TODO: replace event_id and created_at with real values
        name_opts = make_options(data["name"])
        date_opts = make_options(data["date"])
        fencer_opts = make_options(data["fencer_name_to_check"])
        club_opts = make_options(data["club_name_to_check"])
        final_rank_opts = make_options(data["final_rank"])
        percentile_opts = make_options(data["percentile"])

        #data = data.sort_values(by='date')
        data = data.to_dict('records')
            
        message_count_tournament_results = f"{len(data)} records"
        
        return (data,
                message_count_tournament_results,
                name_opts,
                date_opts,
                fencer_opts,
                club_opts,
                final_rank_opts,
                percentile_opts
               )
        
    @app.callback(
        Output('filter-tournament-results-name', 'value'),
        Output('filter-tournament-results-date', 'value'),
        Output('filter-tournament-results-fencer', 'value'),
        Output('filter-tournament-results-club', 'value'),
        Output('filter-tournament-results-final-rank', 'value'),
        Output('filter-tournament-results-percentile', 'value'),
        Input('reset-tournament-results-filters-button', 'n_clicks'),
        prevent_initial_call=True  # so it doesn't fire on page load
    )
    def reset_tournament_results_filters(n_clicks):
        if n_clicks:
            # Returning None clears multi-select dropdowns
            return None, None, None, None, None, None
        return (
            dash.no_update, dash.no_update, dash.no_update,
            dash.no_update, dash.no_update, dash.no_update
        )
          
        
    @app.callback(
        Output('tournaments-table', 'data'),
        Output('output-tournaments-filtered-number', 'children'),
        Output('filter-tournaments-name', 'options'),
        Output('filter-tournaments-date', 'options'),
        Output('filter-tournaments-discipline', 'options'),
        Output('filter-tournaments-type', 'options'),
        Output('filter-tournaments-gender', 'options'),
        Output('filter-tournaments-age-category', 'options'),
        
        Input('filter-tournaments-name', 'value'),
        Input('filter-tournaments-date', 'value'),
        Input('filter-tournaments-discipline', 'value'),
        Input('filter-tournaments-type', 'value'),
        Input('filter-tournaments-gender', 'value'),
        Input('filter-tournaments-age-category', 'value'),
    )
    def refresh_tournaments(
        selected_names, selected_dates, selected_disciplines,
        selected_types, selected_genders, selected_age_categories
    ):

        data = df_events
            
        # Apply filters
        if selected_names:
            data = data[data['name'].isin(selected_names)]
        if selected_dates:
            data = data[data['date'].isin(selected_dates)]
        if selected_disciplines:
            data = data[data['discipline'].isin(selected_disciplines)]
        if selected_types:
            data = data[data['type_id'].isin(selected_types)]
        if selected_genders:
            data = data[data['gender'].isin(selected_genders)]
        if selected_age_categories:
            data = data[data['age_category'].isin(selected_age_categories)]


        def make_options(series):
            return [{"label": v, "value": v} for v in sorted(series.dropna().unique())]

        name_opts = make_options(data["name"])
        date_opts = make_options(data["date"])
        discipline_opts = make_options(data["discipline"])
        type_opts = make_options(data["type_id"])
        gender_opts = make_options(data["gender"])
        age_category_opts = make_options(data["age_category"])


        #data = data.sort_values(by='date')
        data = data.to_dict('records')
            
        message_count_tournaments = f"{len(data)} records"
        
        return (data,
                message_count_tournaments,
                name_opts,
                date_opts,
                discipline_opts,
                type_opts,
                gender_opts,
                age_category_opts
               )
             
    @app.callback(
        Output('filter-tournaments-name', 'value'),
        Output('filter-tournaments-date', 'value'),
        Output('filter-tournaments-discipline', 'value'),
        Output('filter-tournaments-type', 'value'),
        Output('filter-tournaments-gender', 'value'),
        Output('filter-tournaments-age-category', 'value'),
        Input('reset-tournaments-filters-button', 'n_clicks'),
        prevent_initial_call=True  # so it doesn't fire on page load
    )
    def reset_tournaments_filters(n_clicks):
        if n_clicks:
            # Returning None clears multi-select dropdowns
            return None, None, None, None, None, None
        return (
            dash.no_update, dash.no_update, dash.no_update,
            dash.no_update, dash.no_update, dash.no_update
        )
                  

    @app.callback(
        Output('bracket-graph', 'figure'),
        [Input('player-search', 'value'),
        Input('bracket-graph', 'clickData')]
    )
    def update_figure(player_name, click_data):        
        # Prioritize dropdown if selected
        if player_name:
            return eliminations_figure(df_duels, highlight_player=player_name)
        elif click_data and click_data['points']:
            clicked_name = click_data['points'][0]['customdata']
            return eliminations_figure(df_duels, highlight_player=clicked_name)
        return eliminations_figure(df_duels)
    
    
    #? this one belongs to callback below, but cannot be decorated by callback
    #? but can be reused for second fencer stats easily
    def single_fencer_stats(fencer_name: str, df):
        
        if not fencer_name:
            return "-", "-", "-", "-", "-", "-"
        
        fencer_duels = df[
            (df['name_fencer_winner'] == fencer_name) |
            (df['name_fencer_loser'] == fencer_name)
        ]
        won_duels =  df[df['name_fencer_winner'] == fencer_name]
        lost_duels =  df[df['name_fencer_loser'] == fencer_name]

        if fencer_duels.empty:
            return {
                "total_duels": "-",
                "wins": "-",
                "losses": "-",
                "win_rate": "-",
                "avg_score": "-",
                "total_tournaments": "-"
            }
        
        total_duels = len(fencer_duels)
        wins = len(fencer_duels[fencer_duels['name_fencer_winner'] == fencer_name])
        losses = len(fencer_duels[fencer_duels['name_fencer_loser'] == fencer_name])
        win_rate = (wins / total_duels) * 100 if total_duels > 0 else 0
                
        won_score = won_duels["winner_score"].sum()
        lost_score = lost_duels["loser_score"].sum()   
        avg_score = (won_score + lost_score)/ len(fencer_duels)
            
        total_tournaments = fencer_duels['event_id'].nunique()
        
        return {
                "total_duels": total_duels,
                "wins": wins,
                "losses": losses,
                "win_rate": round(win_rate, 2),
                "avg_score": round(avg_score, 1),
                "total_tournaments": total_tournaments
            }
        
    @app.callback(
        Output("stat-total-duels-pool-first", "children"),
        Output("stat-total-duels-elim-first", "children"),
        Output("stat-total-duels-total-first", "children"),
        Output("stat-wins-pool-first", "children"),
        Output("stat-wins-elim-first", "children"),
        Output("stat-wins-total-first", "children"),
        Output("stat-losses-pool-first", "children"),
        Output("stat-losses-elim-first", "children"),
        Output("stat-losses-total-first", "children"),
        Output("stat-winrate-pool-first", "children"),
        Output("stat-winrate-elim-first", "children"),
        Output("stat-winrate-total-first", "children"),
        Output("stat-avg-score-pool-first", "children"),
        Output("stat-avg-score-elim-first", "children"),
        Output("stat-avg-score-total-first", "children"),
        Output("stat-tournaments-pool-first", "children"),
        Output("stat-tournaments-elim-first", "children"),
        Output("stat-tournaments-total-first", "children"),

        Input("filter-fencer-name-first", "value")
    )
    def update_stats_first(fencer_name: str):
        if not fencer_name:
            return ["-"] * 18  # all 18 outputs

        df = df_duels_prep.copy()

        stats_pools = single_fencer_stats(fencer_name, df[df["type"]=="Pool"])
        stats_elims = single_fencer_stats(fencer_name, df[df["type"]!="Pool"])
        stats_total = single_fencer_stats(fencer_name, df)

        def safe(stat, key):
            return stat[key] if stat else "-"

        return (
            safe(stats_pools, "total_duels"),
            safe(stats_elims, "total_duels"),
            safe(stats_total, "total_duels"),
            safe(stats_pools, "wins"),
            safe(stats_elims, "wins"),
            safe(stats_total, "wins"),
            safe(stats_pools, "losses"),
            safe(stats_elims, "losses"),
            safe(stats_total, "losses"),
            f"{safe(stats_pools, 'win_rate')}%",
            f"{safe(stats_elims, 'win_rate')}%",
            f"{safe(stats_total, 'win_rate')}%",
            safe(stats_pools, "avg_score"),
            safe(stats_elims, "avg_score"),
            safe(stats_total, "avg_score"),
            safe(stats_pools, "total_tournaments"),
            safe(stats_elims, "total_tournaments"),
            safe(stats_total, "total_tournaments"),
        )
        
        
    @app.callback(
        Output("stat-total-duels-pool-second", "children"),
        Output("stat-total-duels-elim-second", "children"),
        Output("stat-total-duels-total-second", "children"),
        Output("stat-wins-pool-second", "children"),
        Output("stat-wins-elim-second", "children"),
        Output("stat-wins-total-second", "children"),
        Output("stat-losses-pool-second", "children"),
        Output("stat-losses-elim-second", "children"),
        Output("stat-losses-total-second", "children"),
        Output("stat-winrate-pool-second", "children"),
        Output("stat-winrate-elim-second", "children"),
        Output("stat-winrate-total-second", "children"),
        Output("stat-avg-score-pool-second", "children"),
        Output("stat-avg-score-elim-second", "children"),
        Output("stat-avg-score-total-second", "children"),
        Output("stat-tournaments-pool-second", "children"),
        Output("stat-tournaments-elim-second", "children"),
        Output("stat-tournaments-total-second", "children"),

        Input("filter-fencer-name-second", "value")
    )
    def update_stats_second(fencer_name: str):
        if not fencer_name:
            return ["-"] * 18  # all 18 outputs

        df = df_duels_prep.copy()

        stats_pools = single_fencer_stats(fencer_name, df[df["type"]=="Pool"])
        stats_elims = single_fencer_stats(fencer_name, df[df["type"]!="Pool"])
        stats_total = single_fencer_stats(fencer_name, df)

        def safe(stat, key):
            return stat[key] if stat else "-"

        return (
            safe(stats_pools, "total_duels"),
            safe(stats_elims, "total_duels"),
            safe(stats_total, "total_duels"),
            safe(stats_pools, "wins"),
            safe(stats_elims, "wins"),
            safe(stats_total, "wins"),
            safe(stats_pools, "losses"),
            safe(stats_elims, "losses"),
            safe(stats_total, "losses"),
            f"{safe(stats_pools, 'win_rate')}%",
            f"{safe(stats_elims, 'win_rate')}%",
            f"{safe(stats_total, 'win_rate')}%",
            safe(stats_pools, "avg_score"),
            safe(stats_elims, "avg_score"),
            safe(stats_total, "avg_score"),
            safe(stats_pools, "total_tournaments"),
            safe(stats_elims, "total_tournaments"),
            safe(stats_total, "total_tournaments"),
        )
        
    
    @app.callback(
        Output("duels-common-table", "data"),
        Input("filter-fencer-name-first", "value"),
        Input("filter-fencer-name-second", "value"),
    )
    #? no table if not both filled or same person
    def update_common_duels(fencer1, fencer2):
        if not fencer1 or not fencer2 or fencer1 == fencer2:
            return []  

        df = df_duels_prep.copy()

        common_duels = df[
            ((df["name_fencer_winner"] == fencer1) & (df["name_fencer_loser"] == fencer2)) |
            ((df["name_fencer_winner"] == fencer2) & (df["name_fencer_loser"] == fencer1))
        ]

        # optional: sort by date
        if "date" in common_duels.columns:
            common_duels = common_duels.sort_values("date", ascending=False)
        elif "event_date" in common_duels.columns:
            common_duels = common_duels.sort_values("event_date", ascending=False)
        
        return common_duels.to_dict("records")
        

from dash.dependencies import Input, Output, State
import dash
import pandas as pd

from apps.layout import eliminations_figure

def register_callbacks(
    app, runner,
    df_clubs_v1, df_duels_v1, df_events_v1, df_fencers_v1, df_tournaments_v1, df_tournament_results_v1,
    df_duels_prep_v1, df_tournament_results_prep_v1,
    df_clubs_v2, df_duels_v2, df_events_v2, df_fencers_v2, df_tournaments_v2, df_tournament_results_v2,
    df_duels_prep_v2, df_tournament_results_prep_v2
):
    
    def get_data_for_version(version):
        """Helper to get data based on version"""
        if version == 'v2':
            return {
                'clubs': df_clubs_v2,
                'duels': df_duels_v2,
                'events': df_events_v2,
                'fencers': df_fencers_v2,
                'tournaments': df_tournaments_v2,
                'tournament_results': df_tournament_results_v2,
                'duels_prep': df_duels_prep_v2,
                'tournament_results_prep': df_tournament_results_prep_v2
            }
        else:
            return {
                'clubs': df_clubs_v1,
                'duels': df_duels_v1,
                'events': df_events_v1,
                'fencers': df_fencers_v1,
                'tournaments': df_tournaments_v1,
                'tournament_results': df_tournament_results_v1,
                'duels_prep': df_duels_prep_v1,
                'tournament_results_prep': df_tournament_results_prep_v1
            }
    
    
    @app.callback(
        Output('fencers-table', 'data'),
        Output('fencers-table', 'columns'),
        Output('output-fencers-filtered-number', 'children'),
        Output('filter-fencers-name', 'options'),
        Output('filter-fencers-club', 'options'),
        Output('filter-fencers-country', 'options'),
        Output('filter-fencers-gender', 'options'),
        Output('filter-fencers-birthyear', 'options'),
        Output('filter-fencers-birthyear-container', 'style'),
        Output('filter-fencers-gender-container', 'style'),

        Input('filter-fencers-name', 'value'),
        Input('filter-fencers-club', 'value'),
        Input('filter-fencers-country', 'value'),
        Input('filter-fencers-gender', 'value'),
        Input('filter-fencers-birthyear', 'value'),
        Input('app-version', 'data'),
    )
    def refresh_fencers(
        selected_names, selected_clubs, selected_countries,
        selected_genders, selected_birthyears, version
    ):
        data_dict = get_data_for_version(version)
        df_fencers = data_dict['fencers']
        df_clubs = data_dict['clubs']
        
        #TODO: rozmyslet zda tu dám prep funkci bokem
        if version == 'v2':
            # V2: clubs not available as separate table, use club_name from fencers
            data = df_fencers.copy()
            if 'club_name' not in data.columns:
                data['club_name'] = None
            data['website'] = None
        elif not df_clubs.empty and 'id' in df_clubs.columns and 'club_id' in df_fencers.columns:
            data = pd.merge(
                df_fencers, df_clubs[['id', 'name', "website"]],
                left_on='club_id', right_on='id', how='left',
                suffixes=('', '_club')
            )
        else:
            data = df_fencers.copy()
            data['club_name'] = data.get('club_name', None)
            data['website'] = None
        # Rename club name column if it exists (suffix applied only if there's a conflict)
        if 'name_club' in data.columns:
            data = data.rename(columns={'name_club': 'club_name'})
        elif 'name' in data.columns and 'name' in df_clubs.columns:
            # If no conflict, the club name might be in a different column - check if we need to rename
            # For now, assume club name is already correctly named or handle separately
            pass
        
        # Apply filters to get filtered data for the table
        filtered_data = data.copy()
        if selected_names:
            filtered_data = filtered_data[filtered_data['name'].isin(selected_names)]
        if selected_clubs:
            filtered_data = filtered_data[filtered_data['club_name'].isin(selected_clubs)]
        if selected_countries:
            filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]
        if selected_genders:
            filtered_data = filtered_data[filtered_data['gender'].isin(selected_genders)]
        if selected_birthyears:
            filtered_data = filtered_data[filtered_data['birthyear'].isin(selected_birthyears)]

        #? bohužel neexistuje link na fencera, jen na klub (vlastní URL)   
        #data['name_url'] = data['name'].apply(lambda x: f"[{x}](https://www.czechfencing.cz/)")")
        def create_club_url(row):
            if version == 'v2':
                # V2: just show club name, no link
                return row.get('club_name', '') if pd.notna(row.get('club_name')) else ''
            elif pd.notna(row.get('website')) and row.get('website'):
                return f"[{row.get('club_name', '')}]({row.get('website', '')})"
            else:
                return f"[{row.get('club_name', '')}](https://www.czechfencing.cz/)"
        
        filtered_data['name_url'] = filtered_data.apply(create_club_url, axis=1)
         
        def make_options(series, is_date=False, is_numeric=False):
            unique_vals = series.dropna().unique()
            if is_date:
                # Sort dates chronologically (newest first)
                try:
                    # Try to parse as dates and sort
                    sorted_vals = sorted(unique_vals, key=lambda x: pd.to_datetime(x, errors='coerce'), reverse=True)
                    # Filter out any that couldn't be parsed (will be at the end)
                    valid_dates = [v for v in sorted_vals if pd.notna(pd.to_datetime(v, errors='coerce'))]
                    invalid_dates = [v for v in sorted_vals if pd.isna(pd.to_datetime(v, errors='coerce'))]
                    return [{"label": v, "value": v} for v in valid_dates + sorted(invalid_dates)]
                except Exception:
                    # Fallback to alphabetical if date parsing fails
                    return [{"label": v, "value": v} for v in sorted(unique_vals)]
            elif is_numeric:
                # Sort numerically (largest first)
                try:
                    sorted_vals = sorted(unique_vals, key=lambda x: pd.to_numeric(x, errors='coerce'), reverse=True)
                    # Filter out any that couldn't be parsed (will be at the end)
                    valid_nums = [v for v in sorted_vals if pd.notna(pd.to_numeric(v, errors='coerce'))]
                    invalid_nums = [v for v in sorted_vals if pd.isna(pd.to_numeric(v, errors='coerce'))]
                    return [{"label": v, "value": v} for v in valid_nums + sorted(invalid_nums)]
                except Exception:
                    # Fallback to alphabetical if numeric parsing fails
                    return [{"label": v, "value": v} for v in sorted(unique_vals)]
            else:
                # Sort alphabetically
                return [{"label": v, "value": v} for v in sorted(unique_vals)]

        # Generate options from data filtered by OTHER filters (interdependent filtering)
        # This allows adding more values to widen the selection
        # For names: filter by clubs, countries, genders, birthyears (but not names)
        data_for_names = data.copy()
        if selected_clubs:
            data_for_names = data_for_names[data_for_names['club_name'].isin(selected_clubs)]
        if selected_countries:
            data_for_names = data_for_names[data_for_names['country'].isin(selected_countries)]
        if selected_genders:
            data_for_names = data_for_names[data_for_names['gender'].isin(selected_genders)]
        if selected_birthyears:
            data_for_names = data_for_names[data_for_names['birthyear'].isin(selected_birthyears)]
        names_opts = make_options(data_for_names["name"])
        
        # For clubs: filter by names, countries, genders, birthyears (but not clubs)
        data_for_clubs = data.copy()
        if selected_names:
            data_for_clubs = data_for_clubs[data_for_clubs['name'].isin(selected_names)]
        if selected_countries:
            data_for_clubs = data_for_clubs[data_for_clubs['country'].isin(selected_countries)]
        if selected_genders:
            data_for_clubs = data_for_clubs[data_for_clubs['gender'].isin(selected_genders)]
        if selected_birthyears:
            data_for_clubs = data_for_clubs[data_for_clubs['birthyear'].isin(selected_birthyears)]
        clubs_opts = make_options(data_for_clubs["club_name"])
        
        # For countries: filter by names, clubs, genders, birthyears (but not countries)
        data_for_countries = data.copy()
        if selected_names:
            data_for_countries = data_for_countries[data_for_countries['name'].isin(selected_names)]
        if selected_clubs:
            data_for_countries = data_for_countries[data_for_countries['club_name'].isin(selected_clubs)]
        if selected_genders:
            data_for_countries = data_for_countries[data_for_countries['gender'].isin(selected_genders)]
        if selected_birthyears:
            data_for_countries = data_for_countries[data_for_countries['birthyear'].isin(selected_birthyears)]
        countries_opts = make_options(data_for_countries["country"])
        
        # For genders: filter by names, clubs, countries, birthyears (but not genders)
        data_for_genders = data.copy()
        if selected_names:
            data_for_genders = data_for_genders[data_for_genders['name'].isin(selected_names)]
        if selected_clubs:
            data_for_genders = data_for_genders[data_for_genders['club_name'].isin(selected_clubs)]
        if selected_countries:
            data_for_genders = data_for_genders[data_for_genders['country'].isin(selected_countries)]
        if selected_birthyears:
            data_for_genders = data_for_genders[data_for_genders['birthyear'].isin(selected_birthyears)]
        genders_opts = make_options(data_for_genders["gender"])
        
        # For birthyears: filter by names, clubs, countries, genders (but not birthyears)
        # V2: birthyear not available
        if version == 'v2':
            birthyears_opts = []
        else:
            data_for_birthyears = data.copy()
            if selected_names:
                data_for_birthyears = data_for_birthyears[data_for_birthyears['name'].isin(selected_names)]
            if selected_clubs:
                data_for_birthyears = data_for_birthyears[data_for_birthyears['club_name'].isin(selected_clubs)]
            if selected_countries:
                data_for_birthyears = data_for_birthyears[data_for_birthyears['country'].isin(selected_countries)]
            if selected_genders:
                data_for_birthyears = data_for_birthyears[data_for_birthyears['gender'].isin(selected_genders)]
            birthyears_opts = make_options(data_for_birthyears["birthyear"], is_numeric=True)

        filtered_data = filtered_data.sort_values(by='name', ascending=True)
        
        # Set table columns based on version
        if version == 'v2':
            table_columns = [
                {"name": "Name", "id": "name"},
                {"name": "Club", "id": "name_url"},
                {"name": "Country", "id": "country"},
            ]
            birthyear_container_style = {'display': 'none'}  # Hide birthyear filter in V2
            gender_container_style = {'display': 'none'}  # Hide gender filter in V2
        else:
            table_columns = [
                {"name": "Name", "id": "name"},
                {"name": "Club", "id": "name_url", "presentation":"markdown"},
                {"name": "Country", "id": "country"},
                {"name": "Sex", "id": "gender"},
                {"name": "Birthyear", "id": "birthyear"},
            ]
            birthyear_container_style = {'display': 'block'}
            gender_container_style = {'display': 'block'}
        
        filtered_data = filtered_data.to_dict('records')
            
        message_count_fencers = f"{len(filtered_data)} records"
            
        return (filtered_data,
                table_columns,
                message_count_fencers,
                names_opts,
                clubs_opts,
                countries_opts,
                genders_opts,
                birthyears_opts,
                birthyear_container_style,
                gender_container_style
               )
        
    @app.callback(
        Output('filter-fencers-name', 'value'),
        Output('filter-fencers-club', 'value'),
        Output('filter-fencers-country', 'value'),
        Output('filter-fencers-gender', 'value'),
        Output('filter-fencers-birthyear', 'value'),
        Input('reset-fencers-filters-button', 'n_clicks'),
        State('app-version', 'data'),
        prevent_initial_call=True  # so it doesn't fire on page load
    )
    def reset_fencers_filters(n_clicks, version):
        if n_clicks:
            # Returning None clears multi-select dropdowns
            return None, None, None, None, None
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        
    
    @app.callback(
        Output('clubs-table', 'data'),
        Output('clubs-table', 'columns'),
        Output('output-clubs-filtered-number', 'children'),
        Output('filter-clubs-name', 'options'),
        Output('filter-clubs-city', 'options'),
        Output('filter-clubs-city-container', 'style'),

        Input('filter-clubs-name', 'value'),
        Input('filter-clubs-city', 'value'),
        Input('app-version', 'data'),
    )
    def refresh_clubs(selected_names, selected_cities, version):
        data_dict = get_data_for_version(version)
        
        if version == 'v2':
            # V2: Extract clubs from duels (winner and loser clubs)
            df_duels = data_dict['duels_prep']
            clubs_data = set()
            
            if not df_duels.empty:
                if 'name_club_winner' in df_duels.columns:
                    clubs_data.update(df_duels['name_club_winner'].dropna().unique())
                if 'name_club_loser' in df_duels.columns:
                    clubs_data.update(df_duels['name_club_loser'].dropna().unique())
            
            # Create clubs dataframe for V2
            if clubs_data:
                data = pd.DataFrame({
                    'id': [f"club_{i}" for i in range(len(clubs_data))],
                    'name': sorted([c for c in clubs_data if c]),
                    'city': None,
                    'registration_number': None,
                    'website': None
                })
            else:
                data = pd.DataFrame(columns=['id', 'name', 'city', 'registration_number', 'website'])
        else:
            data = data_dict['clubs']
        
        # Apply filters
        filtered_data = data.copy()
        if selected_names:
            filtered_data = filtered_data[filtered_data['name'].isin(selected_names)]
        if selected_cities and version != 'v2':  # City filter not applicable in V2
            filtered_data = filtered_data[filtered_data['city'].isin(selected_cities)]

        # Create name_url - V2 doesn't have website
        if version == 'v2':
            filtered_data['name_url'] = filtered_data['name']
        else:
            filtered_data['name_url'] = filtered_data.apply(
                lambda row: f"[{row['name']}]({row['website']})" if pd.notna(row.get('website')) and row.get('website') else row['name'],
                axis=1
            )
            
        def make_options(series, is_date=False, is_numeric=False):
            unique_vals = series.dropna().unique()
            if is_date:
                # Sort dates chronologically (newest first)
                try:
                    # Try to parse as dates and sort
                    sorted_vals = sorted(unique_vals, key=lambda x: pd.to_datetime(x, errors='coerce'), reverse=True)
                    # Filter out any that couldn't be parsed (will be at the end)
                    valid_dates = [v for v in sorted_vals if pd.notna(pd.to_datetime(v, errors='coerce'))]
                    invalid_dates = [v for v in sorted_vals if pd.isna(pd.to_datetime(v, errors='coerce'))]
                    return [{"label": v, "value": v} for v in valid_dates + sorted(invalid_dates)]
                except Exception:
                    # Fallback to alphabetical if date parsing fails
                    return [{"label": v, "value": v} for v in sorted(unique_vals)]
            elif is_numeric:
                # Sort numerically (largest first)
                try:
                    sorted_vals = sorted(unique_vals, key=lambda x: pd.to_numeric(x, errors='coerce'), reverse=True)
                    # Filter out any that couldn't be parsed (will be at the end)
                    valid_nums = [v for v in sorted_vals if pd.notna(pd.to_numeric(v, errors='coerce'))]
                    invalid_nums = [v for v in sorted_vals if pd.isna(pd.to_numeric(v, errors='coerce'))]
                    return [{"label": v, "value": v} for v in valid_nums + sorted(invalid_nums)]
                except Exception:
                    # Fallback to alphabetical if numeric parsing fails
                    return [{"label": v, "value": v} for v in sorted(unique_vals)]
            else:
                # Sort alphabetically
                return [{"label": v, "value": v} for v in sorted(unique_vals)]

        # Generate options from data filtered by OTHER filters (interdependent filtering)
        # For names: filter by cities (but not names)
        data_for_names = data.copy()
        if selected_cities:
            data_for_names = data_for_names[data_for_names['city'].isin(selected_cities)]
        clubs_opts = make_options(data_for_names["name"])
        
        # For cities: filter by names (but not cities) - only for V1
        if version == 'v2':
            cities_opts = []  # No city data in V2
        else:
            data_for_cities = data.copy()
            if selected_names:
                data_for_cities = data_for_cities[data_for_cities['name'].isin(selected_names)]
            cities_opts = make_options(data_for_cities["city"])

        filtered_data = filtered_data.sort_values(by='name', ascending=True)
        
        # For V2, only show name column (no city, registration_number)
        if version == 'v2':
            display_data = filtered_data[['name']].copy()
        else:
            display_data = filtered_data[['name_url', 'city', 'registration_number']].copy()
            display_data = display_data.rename(columns={'name_url': 'name'})
        
        display_data = display_data.to_dict('records')
        
        # Set table columns based on version
        if version == 'v2':
            table_columns = [
                {"name": "Name", "id": "name"},
            ]
            city_container_style = {'display': 'none'}  # Hide city filter in V2
        else:
            table_columns = [
                {"name": "Name", "id": "name_url", "presentation":"markdown"},
                {"name": "City", "id": "city"},
                {"name": "Registration number", "id": "registration_number"},
            ]
            city_container_style = {'display': 'block'}
            
        message_count_clubs = f"{len(filtered_data)} records"
            
        return (display_data,
                table_columns,
                message_count_clubs,
                clubs_opts,
                cities_opts,
                city_container_style
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
        Output('duels-table', 'columns'),
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
        Output('filter-duels-gender-container', 'style'),

        Input('filter-duels-tournament', 'value'),
        Input('filter-duels-date', 'value'),
        Input('filter-duels-winner', 'value'),
        Input("filter-duels-winner-club", "value"),
        Input('filter-duels-loser', 'value'),
        Input("filter-duels-loser-club", "value"),
        Input("filter-duels-fight-lvl", "value"),
        Input("filter-duels-gender", "value"),
        Input('app-version', 'data')
    )
    def refresh_duels(
        selected_tournaments, selected_dates, selected_winners,
        selected_winner_clubs, selected_losers, selected_loser_clubs,
        selected_fight_lvl, selected_gender, version
    ):
        data_dict = get_data_for_version(version)
        data = data_dict['duels_prep']
            
        # Apply filters to get filtered data for the table
        filtered_data = data.copy()
        if selected_tournaments:
            filtered_data = filtered_data[filtered_data['name_tournament'].isin(selected_tournaments)]
        if selected_dates:
            filtered_data = filtered_data[filtered_data['date'].isin(selected_dates)]
        if selected_winners:
            filtered_data = filtered_data[filtered_data['name_fencer_winner'].isin(selected_winners)]
        if selected_winner_clubs:
            filtered_data = filtered_data[filtered_data['name_club_winner'].isin(selected_winner_clubs)]
        if selected_losers:
            filtered_data = filtered_data[filtered_data['name_fencer_loser'].isin(selected_losers)]
        if selected_loser_clubs:
            filtered_data = filtered_data[filtered_data['name_club_loser'].isin(selected_loser_clubs)]
        if selected_fight_lvl:
            filtered_data = filtered_data[filtered_data['type'].isin(selected_fight_lvl)]
        if selected_gender and version != 'v2':  # Gender not available in V2
            filtered_data = filtered_data[filtered_data['gender'].isin(selected_gender)]

        def make_options(series, is_date=False, is_numeric=False):
            unique_vals = series.dropna().unique()
            if is_date:
                # Sort dates chronologically (newest first)
                try:
                    # Try to parse as dates and sort
                    sorted_vals = sorted(unique_vals, key=lambda x: pd.to_datetime(x, errors='coerce'), reverse=True)
                    # Filter out any that couldn't be parsed (will be at the end)
                    valid_dates = [v for v in sorted_vals if pd.notna(pd.to_datetime(v, errors='coerce'))]
                    invalid_dates = [v for v in sorted_vals if pd.isna(pd.to_datetime(v, errors='coerce'))]
                    return [{"label": v, "value": v} for v in valid_dates + sorted(invalid_dates)]
                except Exception:
                    # Fallback to alphabetical if date parsing fails
                    return [{"label": v, "value": v} for v in sorted(unique_vals)]
            elif is_numeric:
                # Sort numerically (largest first)
                try:
                    sorted_vals = sorted(unique_vals, key=lambda x: pd.to_numeric(x, errors='coerce'), reverse=True)
                    # Filter out any that couldn't be parsed (will be at the end)
                    valid_nums = [v for v in sorted_vals if pd.notna(pd.to_numeric(v, errors='coerce'))]
                    invalid_nums = [v for v in sorted_vals if pd.isna(pd.to_numeric(v, errors='coerce'))]
                    return [{"label": v, "value": v} for v in valid_nums + sorted(invalid_nums)]
                except Exception:
                    # Fallback to alphabetical if numeric parsing fails
                    return [{"label": v, "value": v} for v in sorted(unique_vals)]
            else:
                # Sort alphabetically
                return [{"label": v, "value": v} for v in sorted(unique_vals)]

        # Helper function to apply all filters except one
        def apply_filters_except(data_df, exclude_filter):
            result = data_df.copy()
            if exclude_filter != 'tournament' and selected_tournaments:
                result = result[result['name_tournament'].isin(selected_tournaments)]
            if exclude_filter != 'date' and selected_dates:
                result = result[result['date'].isin(selected_dates)]
            if exclude_filter != 'winner' and selected_winners:
                result = result[result['name_fencer_winner'].isin(selected_winners)]
            if exclude_filter != 'winner_club' and selected_winner_clubs:
                result = result[result['name_club_winner'].isin(selected_winner_clubs)]
            if exclude_filter != 'loser' and selected_losers:
                result = result[result['name_fencer_loser'].isin(selected_losers)]
            if exclude_filter != 'loser_club' and selected_loser_clubs:
                result = result[result['name_club_loser'].isin(selected_loser_clubs)]
            if exclude_filter != 'fight_lvl' and selected_fight_lvl:
                result = result[result['type'].isin(selected_fight_lvl)]
            if exclude_filter != 'gender' and selected_gender and version != 'v2':
                result = result[result['gender'].isin(selected_gender)]
            return result

        # Generate options from data filtered by OTHER filters (interdependent filtering)
        tournament_opts = make_options(apply_filters_except(data, 'tournament')["name_tournament"])
        date_opts = make_options(apply_filters_except(data, 'date')["date"], is_date=True)
        winner_opts = make_options(apply_filters_except(data, 'winner')["name_fencer_winner"])
        winner_club_opts = make_options(apply_filters_except(data, 'winner_club')["name_club_winner"])
        loser_opts = make_options(apply_filters_except(data, 'loser')["name_fencer_loser"])
        loser_club_opts = make_options(apply_filters_except(data, 'loser_club')["name_club_loser"])
        fight_lvl_opts = make_options(apply_filters_except(data, 'fight_lvl')["type"])
        
        if version == 'v2':
            gender_opts = []
            gender_container_style = {'display': 'none'}
        else:
            gender_opts = make_options(apply_filters_except(data, 'gender')["gender"])
            gender_container_style = {'display': 'block'}

        # Set table columns based on version
        if version == 'v2':
            table_columns = [
                {"name": "Tournament", "id": "tournament_url", "presentation":"markdown"},
                {"name": "Date", "id": "date"},
                {"name": "Winner", "id": "name_fencer_winner"},
                {"name": "Winner Club", "id": "name_club_winner"},
                {"name": "Loser", "id": "name_fencer_loser"},
                {"name": "Loser Club", "id": "name_club_loser"},
                {"name": "Fight LVL", "id": "type"},
                {"name": "Winner Score", "id": "winner_score"},
                {"name": "Loser Score", "id": "loser_score"},
            ]
        else:
            table_columns = [
                {"name": "Tournament", "id": "tournament_url", "presentation":"markdown"},
                {"name": "Date", "id": "date"},
                {"name": "Winner", "id": "name_fencer_winner"},
                {"name": "Winner Club", "id": "name_club_winner"},
                {"name": "Loser", "id": "name_fencer_loser"},
                {"name": "Loser Club", "id": "name_club_loser"},
                {"name": "Fight LVL", "id": "type"},
                {"name": "Gender", "id": "gender"},
                {"name": "Winner Score", "id": "winner_score"},
                {"name": "Loser Score", "id": "loser_score"},
            ]

        #data = filtered_data.sort_values(by='date')
        filtered_data = filtered_data.to_dict('records')
            
        message_count_duels = f"{len(filtered_data)} records"
        
        return (filtered_data,
                table_columns,
                message_count_duels,
                tournament_opts,
                date_opts,
                winner_opts,
                winner_club_opts,
                loser_opts,
                loser_club_opts,
                fight_lvl_opts,
                gender_opts,
                gender_container_style
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
        Input('app-version', 'data'),
    )
    def refresh_tournament_results(
        selected_names, selected_dates, selected_fencers,
        selected_clubs, selected_final_ranks, selected_percentiles, version
    ):
        data_dict = get_data_for_version(version)
        data = data_dict['tournament_results_prep'].copy()
        
        #TODO: move this to prep in runner?
        data["final_rank"] = pd.to_numeric(data["final_rank"], errors='coerce')
        data["ts"] = pd.to_numeric(data["ts"], errors='coerce')
        data["tr"] = pd.to_numeric(data["tr"], errors='coerce')
        data["score_index"] = data["ts"]-data["tr"]
            
        # Apply filters to get filtered data for the table
        filtered_data = data.copy()
        #TODO:
        if selected_names:
            filtered_data = filtered_data[filtered_data['name'].isin(selected_names)]
        #TODO:
        if selected_dates:
            filtered_data = filtered_data[filtered_data['date'].isin(selected_dates)]
        #TODO:
        if selected_fencers:
            filtered_data = filtered_data[filtered_data['fencer_name_to_check'].isin(selected_fencers)]
        #TODO:
        if selected_clubs:
            filtered_data = filtered_data[filtered_data['club_name_to_check'].isin(selected_clubs)]
        if selected_final_ranks:
            filtered_data = filtered_data[filtered_data['final_rank'].isin(selected_final_ranks)]
        if selected_percentiles:
            filtered_data = filtered_data[filtered_data['percentile'].isin(selected_percentiles)]

        def make_options(series, is_date=False, is_numeric=False):
            unique_vals = series.dropna().unique()
            if is_date:
                # Sort dates chronologically (newest first)
                try:
                    # Try to parse as dates and sort
                    sorted_vals = sorted(unique_vals, key=lambda x: pd.to_datetime(x, errors='coerce'), reverse=True)
                    # Filter out any that couldn't be parsed (will be at the end)
                    valid_dates = [v for v in sorted_vals if pd.notna(pd.to_datetime(v, errors='coerce'))]
                    invalid_dates = [v for v in sorted_vals if pd.isna(pd.to_datetime(v, errors='coerce'))]
                    return [{"label": v, "value": v} for v in valid_dates + sorted(invalid_dates)]
                except Exception:
                    # Fallback to alphabetical if date parsing fails
                    return [{"label": v, "value": v} for v in sorted(unique_vals)]
            elif is_numeric:
                # Sort numerically (largest first)
                try:
                    sorted_vals = sorted(unique_vals, key=lambda x: pd.to_numeric(x, errors='coerce'), reverse=True)
                    # Filter out any that couldn't be parsed (will be at the end)
                    valid_nums = [v for v in sorted_vals if pd.notna(pd.to_numeric(v, errors='coerce'))]
                    invalid_nums = [v for v in sorted_vals if pd.isna(pd.to_numeric(v, errors='coerce'))]
                    return [{"label": v, "value": v} for v in valid_nums + sorted(invalid_nums)]
                except Exception:
                    # Fallback to alphabetical if numeric parsing fails
                    return [{"label": v, "value": v} for v in sorted(unique_vals)]
            else:
                # Sort alphabetically
                return [{"label": v, "value": v} for v in sorted(unique_vals)]

        # Helper function to apply all filters except one
        def apply_filters_except(data_df, exclude_filter):
            result = data_df.copy()
            if exclude_filter != 'name' and selected_names:
                result = result[result['name'].isin(selected_names)]
            if exclude_filter != 'date' and selected_dates:
                result = result[result['date'].isin(selected_dates)]
            if exclude_filter != 'fencer' and selected_fencers:
                result = result[result['fencer_name_to_check'].isin(selected_fencers)]
            if exclude_filter != 'club' and selected_clubs:
                result = result[result['club_name_to_check'].isin(selected_clubs)]
            if exclude_filter != 'final_rank' and selected_final_ranks:
                result = result[result['final_rank'].isin(selected_final_ranks)]
            if exclude_filter != 'percentile' and selected_percentiles:
                result = result[result['percentile'].isin(selected_percentiles)]
            return result

        #TODO: replace event_id and created_at with real values
        # Generate options from data filtered by OTHER filters (interdependent filtering)
        name_opts = make_options(apply_filters_except(data, 'name')["name"])
        date_opts = make_options(apply_filters_except(data, 'date')["date"], is_date=True)
        fencer_opts = make_options(apply_filters_except(data, 'fencer')["fencer_name_to_check"])
        club_opts = make_options(apply_filters_except(data, 'club')["club_name_to_check"])
        final_rank_opts = make_options(apply_filters_except(data, 'final_rank')["final_rank"])
        percentile_opts = make_options(apply_filters_except(data, 'percentile')["percentile"])

        #data = filtered_data.sort_values(by='date')
        filtered_data = filtered_data.to_dict('records')
            
        message_count_tournament_results = f"{len(filtered_data)} records"
        
        return (filtered_data,
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
        Output('tournaments-table', 'columns'),
        Output('output-tournaments-filtered-number', 'children'),
        Output('filter-tournaments-name', 'options'),
        Output('filter-tournaments-date', 'options'),
        Output('filter-tournaments-discipline', 'options'),
        Output('filter-tournaments-type', 'options'),
        Output('filter-tournaments-gender', 'options'),
        Output('filter-tournaments-age-category', 'options'),
        Output('filter-tournaments-discipline-type-container', 'style'),
        Output('filter-tournaments-gender-age-container', 'style'),
        
        Input('filter-tournaments-name', 'value'),
        Input('filter-tournaments-date', 'value'),
        Input('filter-tournaments-discipline', 'value'),
        Input('filter-tournaments-type', 'value'),
        Input('filter-tournaments-gender', 'value'),
        Input('filter-tournaments-age-category', 'value'),
        Input('app-version', 'data'),
    )
    def refresh_tournaments(
        selected_names, selected_dates, selected_disciplines,
        selected_types, selected_genders, selected_age_categories, version
    ):
        data_dict = get_data_for_version(version)
        data = data_dict['events']
            
        # Apply filters to get filtered data for the table
        filtered_data = data.copy()
        if selected_names:
            # V2: use 'name' or 'event_name' depending on version
            if version == 'v2' and 'event_name' in filtered_data.columns:
                # Filter by event_name (tournament name) or name (competition name)
                mask = (filtered_data['event_name'].isin(selected_names) if 'event_name' in filtered_data.columns else False) | \
                       (filtered_data['name'].isin(selected_names))
                filtered_data = filtered_data[mask]
            else:
                filtered_data = filtered_data[filtered_data['name'].isin(selected_names)]
        if selected_dates:
            filtered_data = filtered_data[filtered_data['date'].isin(selected_dates)]
        if version != 'v2':  # These filters not available in V2
            if selected_disciplines:
                filtered_data = filtered_data[filtered_data['discipline'].isin(selected_disciplines)]
            if selected_types:
                filtered_data = filtered_data[filtered_data['type_id'].isin(selected_types)]
            if selected_genders:
                filtered_data = filtered_data[filtered_data['gender'].isin(selected_genders)]
            if selected_age_categories:
                filtered_data = filtered_data[filtered_data['age_category'].isin(selected_age_categories)]


        def make_options(series, is_date=False, is_numeric=False):
            unique_vals = series.dropna().unique()
            if is_date:
                # Sort dates chronologically (newest first)
                try:
                    # Try to parse as dates and sort
                    sorted_vals = sorted(unique_vals, key=lambda x: pd.to_datetime(x, errors='coerce'), reverse=True)
                    # Filter out any that couldn't be parsed (will be at the end)
                    valid_dates = [v for v in sorted_vals if pd.notna(pd.to_datetime(v, errors='coerce'))]
                    invalid_dates = [v for v in sorted_vals if pd.isna(pd.to_datetime(v, errors='coerce'))]
                    return [{"label": v, "value": v} for v in valid_dates + sorted(invalid_dates)]
                except Exception:
                    # Fallback to alphabetical if date parsing fails
                    return [{"label": v, "value": v} for v in sorted(unique_vals)]
            elif is_numeric:
                # Sort numerically (largest first)
                try:
                    sorted_vals = sorted(unique_vals, key=lambda x: pd.to_numeric(x, errors='coerce'), reverse=True)
                    # Filter out any that couldn't be parsed (will be at the end)
                    valid_nums = [v for v in sorted_vals if pd.notna(pd.to_numeric(v, errors='coerce'))]
                    invalid_nums = [v for v in sorted_vals if pd.isna(pd.to_numeric(v, errors='coerce'))]
                    return [{"label": v, "value": v} for v in valid_nums + sorted(invalid_nums)]
                except Exception:
                    # Fallback to alphabetical if numeric parsing fails
                    return [{"label": v, "value": v} for v in sorted(unique_vals)]
            else:
                # Sort alphabetically
                return [{"label": v, "value": v} for v in sorted(unique_vals)]

        # Helper function to apply all filters except one
        def apply_filters_except(data_df, exclude_filter):
            result = data_df.copy()
            if exclude_filter != 'name' and selected_names:
                if version == 'v2' and 'event_name' in result.columns:
                    mask = (result['event_name'].isin(selected_names)) | (result['name'].isin(selected_names))
                    result = result[mask]
                else:
                    result = result[result['name'].isin(selected_names)]
            if exclude_filter != 'date' and selected_dates:
                result = result[result['date'].isin(selected_dates)]
            if version != 'v2':
                if exclude_filter != 'discipline' and selected_disciplines:
                    result = result[result['discipline'].isin(selected_disciplines)]
                if exclude_filter != 'type' and selected_types:
                    result = result[result['type_id'].isin(selected_types)]
                if exclude_filter != 'gender' and selected_genders:
                    result = result[result['gender'].isin(selected_genders)]
                if exclude_filter != 'age_category' and selected_age_categories:
                    result = result[result['age_category'].isin(selected_age_categories)]
            return result

        # Generate options from data filtered by OTHER filters (interdependent filtering)
        if version == 'v2' and 'event_name' in data.columns:
            # For V2, combine event_name and name for options
            name_series = data['event_name'].fillna('') + ' - ' + data['name'].fillna('')
            name_opts = make_options(name_series)
        else:
            name_opts = make_options(apply_filters_except(data, 'name')["name"])
        
        date_opts = make_options(apply_filters_except(data, 'date')["date"], is_date=True)
        
        if version == 'v2':
            discipline_opts = []
            type_opts = []
            gender_opts = []
            age_category_opts = []
            discipline_container_style = {'display': 'none'}
            gender_age_container_style = {'display': 'none'}
        else:
            discipline_opts = make_options(apply_filters_except(data, 'discipline')["discipline"])
            type_opts = make_options(apply_filters_except(data, 'type')["type_id"])
            gender_opts = make_options(apply_filters_except(data, 'gender')["gender"])
            age_category_opts = make_options(apply_filters_except(data, 'age_category')["age_category"])
            discipline_container_style = {'display': 'block'}
            gender_age_container_style = {'display': 'block'}

        # Set table columns based on version
        if version == 'v2':
            # For V2, show tournament name and competition name
            if 'event_name' in filtered_data.columns:
                filtered_data['display_name'] = filtered_data['event_name'] + ' - ' + filtered_data['name']
            else:
                filtered_data['display_name'] = filtered_data['name']
            
            table_columns = [
                {"name": "Name", "id": "display_name"},
                {"name": "Date", "id": "date"},
            ]
            # Only keep display_name and date for output
            display_data = filtered_data[['display_name', 'date']].copy()
        else:
            table_columns = [
                {"name": "Name", "id": "name", "presentation":"markdown"},
                {"name": "Date", "id": "date"},
                {"name": "Discipline", "id": "discipline"},
                {"name": "Type", "id": "type_id"},
                {"name": "Gender", "id": "gender"},
                {"name": "Age category", "id": "age_category"}
            ]
            display_data = filtered_data.copy()

        display_data = display_data.to_dict('records')
            
        message_count_tournaments = f"{len(filtered_data)} records"
        
        return (display_data,
                table_columns,
                message_count_tournaments,
                name_opts,
                date_opts,
                discipline_opts,
                type_opts,
                gender_opts,
                age_category_opts,
                discipline_container_style,
                gender_age_container_style
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
        Input('bracket-graph', 'clickData'),
        Input('app-version', 'data')]
    )
    def update_figure(player_name, click_data, version):        
        data_dict = get_data_for_version(version)
        df_duels = data_dict['duels']
        
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

        Input("filter-fencer-name-first", "value"),
        Input('app-version', 'data')
    )
    def update_stats_first(fencer_name: str, version):
        if not fencer_name:
            return ["-"] * 18  # all 18 outputs

        data_dict = get_data_for_version(version)
        df = data_dict['duels_prep'].copy()

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

        Input("filter-fencer-name-second", "value"),
        Input('app-version', 'data')
    )
    def update_stats_second(fencer_name: str, version):
        if not fencer_name:
            return ["-"] * 18  # all 18 outputs

        data_dict = get_data_for_version(version)
        df = data_dict['duels_prep'].copy()

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
        Output("filter-fencer-name-second", "options"),
        Output("filter-fencer-name-second", "value"),
        Input("filter-fencer-name-first", "value"),
        Input("filter-fencer-name-second", "value"),
        Input('app-version', 'data')
    )
    def update_second_fencer_options(first_fencer, current_second_fencer, version):
        """Update second fencer filter to show only fencers who have mutual fights with first fencer"""
        data_dict = get_data_for_version(version)
        
        if not first_fencer:
            # If no first fencer selected, show all players
            df = data_dict['duels_prep'].copy()
            df["name_fencer_winner"].fillna("UNKNOWN", inplace=True)
            df["name_fencer_loser"].fillna("UNKNOWN", inplace=True)
            all_players = sorted(set(
                df["name_fencer_winner"].tolist() +
                df["name_fencer_loser"].tolist()
            ))
            options = [{'label': p, 'value': p} for p in all_players]
            # Keep current selection if it's still valid
            if current_second_fencer and current_second_fencer in [opt['value'] for opt in options]:
                return options, current_second_fencer
            return options, None
        
        # Find all fencers who have mutual fights with the first fencer
        df = data_dict['duels_prep'].copy()
        df["name_fencer_winner"].fillna("UNKNOWN", inplace=True)
        df["name_fencer_loser"].fillna("UNKNOWN", inplace=True)
        
        # Get all duels involving the first fencer
        fencer_duels = df[
            (df['name_fencer_winner'] == first_fencer) |
            (df['name_fencer_loser'] == first_fencer)
        ]
        
        # Extract opponents (both winners and losers who fought the first fencer)
        opponents = set()
        for _, row in fencer_duels.iterrows():
            if row['name_fencer_winner'] == first_fencer:
                opponents.add(row['name_fencer_loser'])
            else:
                opponents.add(row['name_fencer_winner'])
        
        # Remove the first fencer from the list if present
        opponents.discard(first_fencer)
        
        # Sort and create options
        sorted_opponents = sorted(opponents)
        options = [{'label': p, 'value': p} for p in sorted_opponents]
        
        # If current selection is not in the new options, clear it
        if current_second_fencer and current_second_fencer not in opponents:
            return options, None
        
        return options, current_second_fencer
    
    @app.callback(
        Output("duels-common-table", "data"),
        Input("filter-fencer-name-first", "value"),
        Input("filter-fencer-name-second", "value"),
        Input('app-version', 'data')
    )
    #? no table if not both filled or same person
    def update_common_duels(fencer1, fencer2, version):
        if not fencer1 or not fencer2 or fencer1 == fencer2:
            return []  

        data_dict = get_data_for_version(version)
        df = data_dict['duels_prep'].copy()

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
        

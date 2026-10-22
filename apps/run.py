import pandas as pd
from typing import Optional
import os
import json
from tqdm import tqdm

from apps.data_manager import DataManager
from apps.utils import Utilities
from config import Config

# from utils.logger import logger_scraping

class Runner:
    
    def __init__(self) -> None: 
        self.cf = Config()   
        self.data_manager = DataManager()
        self.utils = Utilities()
  
        
    def data_prep(self):
        
        df_clubs = self.data_manager.get_all_data("clubs")
        df_duels = self.data_manager.get_all_data("duels")
        
        #TODO: tyto obecné úpravy by mohly být jinde..ale v main taky nechci.
        df_events = self.data_manager.get_all_data("events")
        df_events['date'] = pd.to_datetime(df_events['date']).dt.strftime('%Y-%m-%d')
        
        df_fencers = self.data_manager.get_all_data("fencers")
        df_tournaments = self.data_manager.get_all_data("tournaments")
        df_tournament_results = self.data_manager.get_all_data("tournament_results")
        
        return df_clubs, df_duels, df_events, df_fencers, df_tournaments, df_tournament_results
    
    
    def df_duels_prep(self, df_duels, df_events, df_fencers, df_clubs, df_tournaments) -> pd.DataFrame:
        
        #? Extra data pro filtry na stránkách
        #? některé sloupce, jako tournament_id, beru jen kvůli dalíšmu joinu
        df = df_duels.copy()
                    
        df = pd.merge(df, df_events[['id', "name", "date", "tournament_id", "gender"]], left_on='event_id', right_on='id', how='left', suffixes=('', '_event'))
        #? musím to dělat nadvakrát, obojí, abych si pokaždý označil W a L?
        df = pd.merge(df, df_fencers[['id', "name", "club_id"]], left_on='winner_id', right_on='id', how='left', suffixes=('', '_fencer_winner'))
        df = pd.merge(df, df_fencers[['id', "name", "club_id"]], left_on='loser_id', right_on='id', how='left', suffixes=('', '_fencer_loser'))
        df = pd.merge(df, df_clubs[['id', "name"]], left_on='club_id', right_on='id', how='left', suffixes=('', '_club_winner'))
        df = pd.merge(df, df_clubs[['id', "name"]], left_on='club_id_fencer_loser', right_on='id', how='left', suffixes=('', '_club_loser'))
        #? tento vyloženě jen kvůli jménu a linku na turnaj
        df = pd.merge(df, df_tournaments[['id', 'name', "f_id"]], left_on='tournament_id', right_on='id', how='left', suffixes=('', '_tournament'))

        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

        df['tournament_url'] = df.apply(
            lambda row: f"[{row['name_tournament']}](https://www.czechfencing.cz/portal/tournaments/detail/{row['f_id']})" if pd.notna(row['f_id']) and row['f_id'] else  f"[{row['f_id']}](https://www.czechfencing.cz/)",
            axis=1
                    )
        
        return df
    
    
    def df_tournament_results_prep(self, df_tournament_results, df_events, df_tournaments) -> pd.DataFrame:
        
        #? Extra data pro filtry na stránkách
        #? některé sloupce, jako tournament_id, beru jen kvůli dalíšmu joinu
        df = df_tournament_results.copy()
                            
        df = pd.merge(df, df_events[['id', "tournament_id", "date"]], left_on='event_id', right_on='id', how='left', suffixes=('', '_event'))
        
        #? tento vyloženě jen kvůli jménu a linku na turnaj
        df = pd.merge(df, df_tournaments[['id', 'name', "f_id"]], left_on='tournament_id', right_on='id', how='left', suffixes=('', '_tournament'))

        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

        df['tournament_url'] = df.apply(
            lambda row: f"[{row['name']}](https://www.czechfencing.cz/portal/tournaments/detail/{row['f_id']})" if pd.notna(row['f_id']) and row['f_id'] else  f"[{row['f_id']}](https://www.czechfencing.cz/)",
            axis=1
                    )
        
        return df
    
    # V2: Excel data loading from FIE files
    def data_prep_v2(self, excel_dir: str = "C:\\Users\\jirka\\Downloads"):
        """
        Load data from Excel files (FIE/FencingTimeLive data 2019-2025)
        Returns dataframes in same structure as data_prep() for compatibility
        """
        events = []
        event_details = []
        event_links = []
        pool_matches = []
        total_results = []
        elimination_matches = []
        
        date_ranges = [
            ["2025-01-01", "2025-06-30"], 
            ["2024-07-01", "2024-12-31"],
            ["2024-01-01", "2024-06-30"],
            ["2023-07-01", "2023-12-31"],
            ["2023-01-01", "2023-06-30"],
            ["2022-07-01", "2022-12-31"],
            ["2022-01-01", "2022-06-30"],
            ["2021-07-01", "2021-12-31"],
            ["2020-07-01", "2020-12-31"], 
            ["2020-01-01", "2020-06-30"],
            ["2019-07-01", "2019-12-31"],
            ["2019-01-01", "2019-06-30"],
        ]
        
        for dates in date_ranges:
            try:
                events_file = f"{excel_dir}\\events_{dates[0]}_to_{dates[1]}.xlsx"
                if os.path.exists(events_file):
                    df_events = pd.read_excel(events_file)
                    events.append(df_events)
                
                event_details_file = f"{excel_dir}\\event_details_{dates[0]}_to_{dates[1]}.xlsx"
                if os.path.exists(event_details_file):
                    df_event_details = pd.read_excel(event_details_file)
                    event_details.append(df_event_details)
                
                event_links_file = f"{excel_dir}\\event_links_{dates[0]}_to_{dates[1]}.xlsx"
                if os.path.exists(event_links_file):
                    df_event_links = pd.read_excel(event_links_file)
                    event_links.append(df_event_links)
                
                pool_matches_file = f"{excel_dir}\\pool_matches_{dates[0]}_to_{dates[1]}.xlsx"
                if os.path.exists(pool_matches_file):
                    df_pool_matches = pd.read_excel(pool_matches_file)
                    pool_matches.append(df_pool_matches)
                
                total_results_file = f"{excel_dir}\\total_results_{dates[0]}_to_{dates[1]}.xlsx"
                if os.path.exists(total_results_file):
                    df_total_results = pd.read_excel(total_results_file)
                    total_results.append(df_total_results)
                
                elimination_matches_file = f"{excel_dir}\\elimination_matches_{dates[0]}_to_{dates[1]}.xlsx"
                if os.path.exists(elimination_matches_file):
                    df_elimination_matches = pd.read_excel(elimination_matches_file)
                    elimination_matches.append(df_elimination_matches)
            except Exception as e:
                print(f"Warning: Could not load files for {dates[0]} to {dates[1]}: {e}")
                continue
        
        # Combine all dataframes
        df_events_all = pd.concat(events, ignore_index=True) if events else pd.DataFrame()
        df_event_details_all = pd.concat(event_details, ignore_index=True) if event_details else pd.DataFrame()
        df_event_links_all = pd.concat(event_links, ignore_index=True) if event_links else pd.DataFrame()
        df_pool_matches_all = pd.concat(pool_matches, ignore_index=True) if pool_matches else pd.DataFrame()
        df_total_results_all = pd.concat(total_results, ignore_index=True) if total_results else pd.DataFrame()
        df_elimination_matches_all = pd.concat(elimination_matches, ignore_index=True) if elimination_matches else pd.DataFrame()
        
        # Map to V1 structure
        # First, merge events with event_details to get full event information
        if not df_events_all.empty and not df_event_details_all.empty:
            # Merge events (event_id, event_name, date) with event_details (event_id, name, event_detail_id)
            df_events_merged = pd.merge(
                df_event_details_all[['event_id', 'name', 'event_detail_id', 'link']],
                df_events_all[['event_id', 'event_name', 'date']],
                on='event_id',
                how='left'
            )
        else:
            df_events_merged = pd.DataFrame()
        
        # Clubs: extract unique club names from pool_matches, elimination_matches, and total_results
        club_names = set()
        
        # From total_results
        if not df_total_results_all.empty and 'club1' in df_total_results_all.columns:
            club_names.update(df_total_results_all['club1'].dropna().unique())
        
        # From pool_matches - we'll need to get clubs from fencer names via total_results
        # (pool_matches only has names, not clubs directly)
        
        # Create clubs dataframe
        if club_names:
            df_clubs_v2 = pd.DataFrame({
                'id': [f"club_{i}" for i in range(len(club_names))],
                'name': sorted([c for c in club_names if c]),
                'city': None,
                'registration_number': None,
                'website': None
            })
        else:
            df_clubs_v2 = pd.DataFrame(columns=['id', 'name', 'city', 'registration_number', 'website'])
        
        # Create club name to ID mapping
        club_name_to_id = dict(zip(df_clubs_v2['name'], df_clubs_v2['id'])) if not df_clubs_v2.empty else {}
        
        # Fencers: extract from total_results
        if not df_total_results_all.empty:
            fencers_data = []
            seen_fencers = set()
            for _, row in df_total_results_all.iterrows():
                fencer_name = row.get('fencer_name', 'Unknown')
                if fencer_name not in seen_fencers:
                    fencers_data.append({
                        'id': f"fie_{row.get('fencer_result_id', 'unknown')}",
                        'name': fencer_name,
                        'country': row.get('country', 'Unknown'),
                        'gender': None,  # Not available in FIE data
                        'birthyear': None,  # Not available in FIE data
                        'club_id': club_name_to_id.get(row.get('club1'), None),
                        'club_name': row.get('club1', None)
                    })
                    seen_fencers.add(fencer_name)
            df_fencers_v2 = pd.DataFrame(fencers_data)
        else:
            df_fencers_v2 = pd.DataFrame(columns=['id', 'name', 'country', 'gender', 'birthyear', 'club_id', 'club_name'])
        
        # Tournaments: from events (these are the main tournaments)
        if not df_events_all.empty:
            df_tournaments_v2 = pd.DataFrame({
                'id': df_events_all['event_id'],
                'name': df_events_all['event_name'],
                'f_id': df_events_all['event_id'],
                'date': df_events_all['date']
            }).drop_duplicates(subset=['id'])
        else:
            df_tournaments_v2 = pd.DataFrame(columns=['id', 'name', 'f_id', 'date'])
        
        # Events: from event_details merged with events (these are the individual competitions within tournaments)
        if not df_events_merged.empty:
            df_events_v2 = pd.DataFrame({
                'id': df_events_merged['event_detail_id'],
                'name': df_events_merged['name'],  # Event detail name (e.g., "Kord senioři")
                'event_name': df_events_merged['event_name'],  # Tournament name
                'date': pd.to_datetime(df_events_merged['date'], errors='coerce').dt.strftime('%Y-%m-%d'),
                'tournament_id': df_events_merged['event_id'],
                'gender': None,  # Not directly available
                'discipline': None,
                'age_category': None,
                'type_id': None,
                'link': df_events_merged.get('link', None)
            })
        else:
            df_events_v2 = pd.DataFrame(columns=['id', 'name', 'event_name', 'date', 'tournament_id', 'gender', 'discipline', 'age_category', 'type_id', 'link'])
        
        # Duels: from pool_matches and elimination_matches
        duels_data = []
        
        # Create mapping from fencer names to clubs (from total_results)
        fencer_to_club = {}
        if not df_total_results_all.empty:
            for _, row in df_total_results_all.iterrows():
                fencer_name = row.get('fencer_name')
                club_name = row.get('club1')
                if fencer_name and club_name:
                    fencer_to_club[fencer_name] = club_name
        
        # Pool matches
        if not df_pool_matches_all.empty:
            for _, row in df_pool_matches_all.iterrows():
                right_score = int(row.get('right_score', 0)) if str(row.get('right_score', '0')).isdigit() else 0
                left_score = int(row.get('left_score', 0)) if str(row.get('left_score', '0')).isdigit() else 0
                
                if right_score > left_score:
                    winner_name = row.get('right_name')
                    loser_name = row.get('left_name')
                else:
                    winner_name = row.get('left_name')
                    loser_name = row.get('right_name')
                
                duels_data.append({
                    'id': f"pool_{row.get('event_detail_id', '')}_{row.get('pool_id', '')}_{len(duels_data)}",
                    'event_id': row.get('event_detail_id'),
                    'winner_id': None,
                    'loser_id': None,
                    'winner_name': winner_name,
                    'loser_name': loser_name,
                    'winner_club': fencer_to_club.get(winner_name, None),
                    'loser_club': fencer_to_club.get(loser_name, None),
                    'type': 'Pool',
                    'winner_score': max(right_score, left_score),
                    'loser_score': min(right_score, left_score)
                })
        
        # Elimination matches - determine proper elimination levels
        if not df_elimination_matches_all.empty:
            # First, determine the number of competitors per round_col per event
            # Group by event_detail_id and round_col to count unique competitors
            elimination_round_sizes = {}
            
            for event_detail_id in df_elimination_matches_all['event_detail_id'].unique():
                event_eliminations = df_elimination_matches_all[
                    df_elimination_matches_all['event_detail_id'] == event_detail_id
                ]
                
                for round_col in event_eliminations['round_col'].unique():
                    round_matches = event_eliminations[
                        event_eliminations['round_col'] == round_col
                    ]
                    
                    # Count unique competitors in this round
                    competitors = set()
                    for _, match in round_matches.iterrows():
                        if match.get('player1'):
                            competitors.add(match.get('player1'))
                        if match.get('player2'):
                            competitors.add(match.get('player2'))
                    
                    num_competitors = len(competitors)
                    key = (event_detail_id, round_col)
                    elimination_round_sizes[key] = num_competitors
            
            # Now process elimination matches with proper level names
            for _, row in df_elimination_matches_all.iterrows():
                if row.get('winner_name') and row.get('player1') and row.get('player2'):
                    winner_name = row.get('winner_name')
                    loser_name = row.get('player2') if winner_name == row.get('player1') else row.get('player1')
                    
                    # Parse score if available
                    score_str = row.get('score', '')
                    winner_score = None
                    loser_score = None
                    if score_str and '-' in str(score_str):
                        try:
                            parts = str(score_str).split('-')
                            if len(parts) == 2:
                                winner_score = int(parts[0].strip())
                                loser_score = int(parts[1].strip())
                        except:
                            pass
                    
                    # Determine elimination level based on number of competitors
                    event_detail_id = row.get('event_detail_id')
                    round_col = row.get('round_col')
                    key = (event_detail_id, round_col)
                    
                    num_competitors = elimination_round_sizes.get(key, 0)
                    
                    # Map number of competitors to elimination level
                    # Final = 2, Semifinal = 4, Quarterfinal = 8, etc.
                    if num_competitors == 2:
                        elim_level = "Eliminace_2"  # Final
                    elif num_competitors == 4:
                        elim_level = "Eliminace_4"  # Semifinal
                    elif num_competitors == 8:
                        elim_level = "Eliminace_8"  # Quarterfinal
                    elif num_competitors == 16:
                        elim_level = "Eliminace_16"  # Round of 16
                    elif num_competitors == 32:
                        elim_level = "Eliminace_32"  # Round of 32
                    elif num_competitors == 64:
                        elim_level = "Eliminace_64"  # Round of 64
                    else:
                        # Fallback: use round_col if we can't determine
                        elim_level = f"Eliminace_{num_competitors}" if num_competitors > 0 else f"Eliminace_{round_col}"
                    
                    duels_data.append({
                        'id': f"elim_{event_detail_id}_{round_col}_{len(duels_data)}",
                        'event_id': event_detail_id,
                        'winner_id': None,
                        'loser_id': None,
                        'winner_name': winner_name,
                        'loser_name': loser_name,
                        'winner_club': fencer_to_club.get(winner_name, None),
                        'loser_club': fencer_to_club.get(loser_name, None),
                        'type': elim_level,
                        'winner_score': winner_score,
                        'loser_score': loser_score
                    })
        
        df_duels_v2 = pd.DataFrame(duels_data) if duels_data else pd.DataFrame(columns=['id', 'event_id', 'winner_id', 'loser_id', 'winner_name', 'loser_name', 'winner_club', 'loser_club', 'type', 'winner_score', 'loser_score'])
        
        # Tournament results: from total_results
        if not df_total_results_all.empty:
            df_tournament_results_v2 = pd.DataFrame({
                'id': df_total_results_all['fencer_result_id'],
                'event_id': df_total_results_all['event_detail_id'],
                'fencer_id': None,
                'fencer_name_to_check': df_total_results_all['fencer_name'],
                'club_name_to_check': df_total_results_all['club1'],
                'final_rank': df_total_results_all['position'],
                'percentile': None,  # Not available in FIE data
                'victories': df_total_results_all.get('victories', None),
                'victories_perc': df_total_results_all.get('v_to_m', None),
                'ts': df_total_results_all.get('ts', None),
                'tr': df_total_results_all.get('tr', None)
            })
        else:
            df_tournament_results_v2 = pd.DataFrame(columns=['id', 'event_id', 'fencer_id', 'fencer_name_to_check', 'club_name_to_check', 'final_rank', 'percentile', 'victories', 'victories_perc', 'ts', 'tr'])
        
        return df_clubs_v2, df_duels_v2, df_events_v2, df_fencers_v2, df_tournaments_v2, df_tournament_results_v2
    
    def df_duels_prep_v2(self, df_duels, df_events, df_fencers, df_clubs, df_tournaments) -> pd.DataFrame:
        """V2 version of df_duels_prep - adapted for Excel data structure"""
        df = df_duels.copy()
        
        # Merge event info (event_details merged with events)
        if not df_events.empty and 'id' in df_events.columns:
            # Prepare event columns - rename to avoid conflicts
            event_cols = df_events[['id', "name", "date", "tournament_id"]].copy()
            if 'event_name' in df_events.columns:
                event_cols['event_name'] = df_events['event_name']
            if 'link' in df_events.columns:
                event_cols['link'] = df_events['link']
            
            # Rename 'name' to 'name_event' to avoid conflict with tournament name
            event_cols = event_cols.rename(columns={'name': 'name_event'})
            
            df = pd.merge(df, event_cols, 
                         left_on='event_id', right_on='id', how='left', suffixes=('', '_event'))
        
        # For V2, we use names directly since we don't have proper IDs
        if 'winner_name' in df.columns:
            df['name_fencer_winner'] = df['winner_name']
        if 'loser_name' in df.columns:
            df['name_fencer_loser'] = df['loser_name']
        
        # Use club names from duels data if available
        if 'winner_club' in df.columns:
            df['name_club_winner'] = df['winner_club']
        else:
            df['name_club_winner'] = None
            
        if 'loser_club' in df.columns:
            df['name_club_loser'] = df['loser_club']
        else:
            df['name_club_loser'] = None
        
        # Merge tournament info
        if not df_tournaments.empty and 'id' in df_tournaments.columns:
            df = pd.merge(df, df_tournaments[['id', 'name', "f_id"]], 
                         left_on='tournament_id', right_on='id', how='left', suffixes=('', '_tournament'))
            
            # Create tournament name - combine tournament name with event detail name for V2
            if 'name_tournament' not in df.columns:
                if 'event_name' in df.columns and 'name_event' in df.columns:
                    # V2: Combine tournament name (event_name) with competition name (name_event)
                    df['name_tournament'] = df['event_name'].fillna('') + ' - ' + df['name_event'].fillna('')
                elif 'event_name' in df.columns:
                    df['name_tournament'] = df['event_name']
                elif 'name' in df.columns:
                    # V1: Use tournament name
                    df['name_tournament'] = df['name']
                else:
                    df['name_tournament'] = ''
        
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')
        else:
            df['date'] = None
        
        # Create tournament URL - use link from events if available
        if 'link' in df.columns:
            df['tournament_url'] = df.apply(
                lambda row: f"[{row.get('name_tournament', 'Tournament')}]({row.get('link', 'https://www.fencingtimelive.com/')})" 
                if pd.notna(row.get('link')) else f"[{row.get('name_tournament', 'Tournament')}](https://www.fencingtimelive.com/tournaments/eventSchedule/{row.get('f_id', '')})",
                axis=1
            )
        else:
            df['tournament_url'] = df.apply(
                lambda row: f"[{row.get('name_tournament', 'Tournament')}](https://www.fencingtimelive.com/tournaments/eventSchedule/{row.get('f_id', '')})" 
                if pd.notna(row.get('f_id')) and row.get('f_id') else f"[{row.get('name_tournament', 'Tournament')}](https://www.fencingtimelive.com/)",
                axis=1
            )
        
        df['gender'] = None  # Not available in V2
        
        return df
    
    def df_tournament_results_prep_v2(self, df_tournament_results, df_events, df_tournaments) -> pd.DataFrame:
        """V2 version of df_tournament_results_prep - adapted for Excel data structure"""
        df = df_tournament_results.copy()
        
        # Merge event info (event_details merged with events)
        if not df_events.empty and 'id' in df_events.columns:
            merge_cols = ['id', "tournament_id", "date"]
            if 'event_name' in df_events.columns:
                merge_cols.append('event_name')
            if 'name' in df_events.columns:
                merge_cols.append('name')
            if 'link' in df_events.columns:
                merge_cols.append('link')
            df = pd.merge(df, df_events[merge_cols], 
                         left_on='event_id', right_on='id', how='left', suffixes=('', '_event'))
        
        # Merge tournament info
        if not df_tournaments.empty and 'id' in df_tournaments.columns:
            df = pd.merge(df, df_tournaments[['id', 'name', "f_id"]], 
                         left_on='tournament_id', right_on='id', how='left', suffixes=('', '_tournament'))
        
        # Create tournament name - combine event_name and event detail name
        if 'event_name' in df.columns and 'name' in df.columns:
            df['name'] = df['event_name'] + ' - ' + df['name']
        elif 'event_name' in df.columns:
            df['name'] = df['event_name']
        elif 'name' not in df.columns:
            df['name'] = ''
        
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')
        else:
            df['date'] = None
        
        # Create tournament URL - use link from events if available
        if 'link' in df.columns:
            df['tournament_url'] = df.apply(
                lambda row: f"[{row.get('name', 'Tournament')}]({row.get('link', 'https://www.fencingtimelive.com/')})" 
                if pd.notna(row.get('link')) else f"[{row.get('name', 'Tournament')}](https://www.fencingtimelive.com/tournaments/eventSchedule/{row.get('f_id', '')})",
                axis=1
            )
        else:
            df['tournament_url'] = df.apply(
                lambda row: f"[{row.get('name', 'Tournament')}](https://www.fencingtimelive.com/tournaments/eventSchedule/{row.get('f_id', '')})" 
                if pd.notna(row.get('f_id')) and row.get('f_id') else f"[{row.get('name', 'Tournament')}](https://www.fencingtimelive.com/)",
                axis=1
            )
        
        return df
    

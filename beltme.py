import glob
import pandas as pd
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
# Import calls dataframe
calls_df = pd.read_csv('calls.csv')

# Find indices to start
participants_indices = calls_df[calls_df['text'] == 'Company Participants'].index.tolist()
guest_indices = calls_df[calls_df['text'] == 'Conference Call Participants'].index.tolist()
operator_indices = calls_df[calls_df['text'] == 'Operator'].index.tolist()
abrupt_start = calls_df[calls_df['text'].str.contains('Call Started Abruptly')].index.tolist()

# Indices of call participants
paired_indices = []
for part_idx in participants_indices:
    next_operator_idx = next(op_idx for op_idx in operator_indices if op_idx > part_idx)
    next_abrupt_idx = next(ab_idx for ab_idx in abrupt_start if ab_idx > part_idx)
    if next_abrupt_idx < next_operator_idx:
        paired_indices.append((part_idx + 1, next_abrupt_idx))
    else:
        paired_indices.append((part_idx + 1, next_operator_idx))

# Extract names
participant_list = ['Operator', 'Unidentified Analyst']
for start_idx, end_idx in paired_indices:
    participant_list.extend(calls_df['text'][start_idx:end_idx][calls_df['text'][start_idx:end_idx].index.isin(guest_indices) == False].tolist())

# Drop off job title
participant_list = [re.sub(r'\s*-\s*.*', '', part).strip() for part in participant_list]

# Remove duplicates
participant_list = list(dict.fromkeys(participant_list))

# Find similar names with fuzzywuzzy
def find_similar_names(name, name_list, threshold=90):
    similar_names = process.extract(name, name_list, scorer=fuzz.token_sort_ratio)
    return [n for n, score in similar_names if score >= threshold]

# Group similar names
unique_names = []
for name in participant_list:
    if not any(fuzz.token_sort_ratio(name, unique_name) >= 90 for unique_name in unique_names):
        unique_names.append(name)

# Find indices of each participant
participant_indices = {}
for participant in unique_names:
    similar_names = find_similar_names(participant, participant_list)
    indices = []
    for name in similar_names:
        indices.extend(calls_df[calls_df['text'] == name].index.tolist())
    participant_indices[participant] = sorted(indices)

# Create new dataframe
named_df = pd.DataFrame(columns=['name', 'text', 'original_index', 'ticker', 'quarter', 'year'])

# Pair participants with their statements
for participant, indices in participant_indices.items():
    for idx in indices:
        next_idx = next((i for i in sorted(sum(participant_indices.values(), [])) if i > idx), len(calls_df))
        statement = calls_df['text'][idx + 1:next_idx][calls_df['text'][idx + 1:next_idx].index.isin(participant_indices[participant]) == False].tolist()
        statement = ' '.join(statement).strip()
        if len(statement) > 0:
            ticker = calls_df.at[idx, 'ticker']
            quarter = calls_df.at[idx, 'quarter']
            year = calls_df.at[idx, 'year']
            named_df = pd.concat([named_df, pd.DataFrame([{'name': participant, 'text': statement, 'original_index': idx, 'ticker': ticker, 'quarter': quarter, 'year': year}])], ignore_index=True)

# Sort named_df by original_index to maintain the order of calls_df
named_df = named_df.sort_values(by='original_index').reset_index(drop=True)
named_df = named_df.drop(columns=['original_index'])

# Save named_df to CSV
named_df.to_csv('named_statements.csv', index=False)
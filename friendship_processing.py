import pandas as pd
import numpy as np

def rename_columns(df):
    df = df.rename(columns={
        'Would I be comfortable with speaking with this person on the phone?': 'Phone Comfort',
        'Would I be comfortable going for a meal with this person?': 'In-Person Comfort',
        'Would I be comfortable openly telling them about how I feel?': 'Emotional Comfort',
        'Everytime I see this person, am I subconciously trying to be the centre of attention?': 'Attention Seeking Result',
        'Would I be comfortable with them for a favour?': 'Favour Comfort',
        'How often am I in contact with them?': 'Contact Frequency',
    })
    return df 

def CalculateFriendshipScore(df):
    df['Friendship Score'] = (
        (df['Phone Comfort'] * 0.25) +
        (df['In-Person Comfort'] * 0.32) +
        (df['Emotional Comfort'] * 0.45) +
        (df['Attention Seeking Result'] * -0.3) +
        (df['Favour Comfort'] * 0.3) +
        (df['Contact Frequency'] * 0.25)
    ) / 6
    df['Friendship Score'] = df['Friendship Score'].round(2)
    
    return df

def calculate_group_associations(df):
    # Print column names to verify the correct name
    #print("Available columns:", df.columns.tolist())
    
    # Make sure the column exists before processing
    if 'Friend Group / Known Associations' not in df.columns:
        print("Warning: 'Friend Group / Known Associations' column not found")
        df['Group Count'] = 0
        return df
        
    #Calculate how many groups each person is associated with
    df['Group Count'] = df['Friend Group / Known Associations'].apply(lambda x: len(x.split(', ')) if pd.notnull(x) else 0)
    
    #Convert the 'Friend Group / Known Associations' column to a list of groups
    df['Friend Group / Known Associations'] = df['Friend Group / Known Associations'].apply(lambda x: x.split(', ') if pd.notnull(x) else [])
    return df

def main():
    friends_df = pd.read_csv('Data/friendship_graded.csv')
    #print(friends_df.head())
    #print(friends_df.columns)
    friends_df = rename_columns(friends_df)
    #print(friends_df.columns)
    
    friends_processed = CalculateFriendshipScore(friends_df)
    
    
    #print(friends_processed.head())
    
    connections_df = pd.read_csv('Data/social_connections.csv')
    connections_df['Friendship Score'] = friends_processed['Friendship Score']
    connections_df = calculate_group_associations(connections_df)
    connections_df.to_csv('Data/processed_social_connections.csv', index=False)
    #print(connections_df.head())
    
if __name__ == "__main__":
    main()
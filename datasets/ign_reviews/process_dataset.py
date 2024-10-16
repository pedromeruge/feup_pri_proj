import pandas as pd

def main():
    process_dataset('ign_reviews/ign_reviews.csv', 'ign_reviews/parsed_ign_reviews.csv')

#just change title names
def process_dataset(dataset_path_in, dataset_path_out):

    games = pd.read_csv(dataset_path_in)
    
    games.rename(columns= {
        'Game Title': 'name',
        'Review Text': 'ign_review_text',
        'Score': 'ign_score'
    }, inplace=True)

    # remove entries that don't have name, or don't have review and score
    condition = games['name'].notnull() & (games['ign_review_text'].notnull() | games['ign_score'].notnull())
    games_filtered = games[condition]

    # check dropped entries
    dropped_count = len(games) - len(games_filtered)
    if dropped_count > 0:
        print(f"Dropped {dropped_count} entries due to missing fields.")

    games_filtered.to_csv(dataset_path_out, index=False)

    print(f"Obtained {len(games_filtered)} entries") 
    
    # NOTE: there were no invalid entries
    
main()
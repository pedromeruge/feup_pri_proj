import first_dataset.process_dataset as first_DS
import giantbomb_related.scrape_giantbomb_data as giantbomb_DS
import giantbomb_related.process_dataset as giantbomb_process
import giantbomb_related.merge_datasets as giantbomb_merge
# import ign_reviews.scrape_ign_review_links as ign_links
# import ign_reviews.scrape_ign_reviews as ign_reviews
import ign_reviews.merge_datasets as ign_merge
import final_dataset_processing.process_dataset as final_processing
import traceback

def main():
    try:
        first_ds_output_path = 'first_dataset/parsed_games.json'
        temp_snd_ds_output_path = 'giantbomb_related/scraped_info.json'
        final_snd_ds_output_path = 'giantbomb_related/parsed_giantbomb_info.json'
        giantbomb_merged_ds_output_path = 'giantbomb_related/merged_games_1.json'
        ign_reviews_path = 'ign_reviews/parsed_ign_reviews.csv'
        temp_merged_ds_output_path = 'ign_reviews/merged_games_2.json'
        final_merged_ds_output_path = 'merged_games_final.json'

        first_DS.process_dataset(first_ds_output_path)
        # giantbomb_DS.scrape(first_ds_output_path, temp_snd_ds_output_path)
        # giantbomb_process.process_dataset(temp_snd_ds_output_path,final_snd_ds_output_path)
        giantbomb_merge.merge_initial_dataset_with_giantbomb(first_ds_output_path, final_snd_ds_output_path, "name", giantbomb_merged_ds_output_path)
        
        ## add the ign scraping function calls here
        ## ...
        ign_merge.merge_curr_dataset_with_ign_review(giantbomb_merged_ds_output_path, ign_reviews_path, "name", temp_merged_ds_output_path)

        final_processing.process_dataset(temp_merged_ds_output_path, final_merged_ds_output_path)

    except Exception as e:
        print(e)
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
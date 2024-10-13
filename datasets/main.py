import first_dataset.process_dataset as first_DS
import giantbomb_related.scrape_giantbomb_data as giantbomb_DS
import common.merge_datasets as Common

def main():
    try:
        first_ds_output_path = 'first_dataset/parsed_games.json'
        snd_ds_output_path = 'giantbomb_related/scraped_info.json'
        merged_ds_output_path = 'merged_games.json'

        # first_DS.process_dataset(first_ds_output_path)
        # giantbomb_DS.scrape(first_ds_output_path, snd_ds_output_path)
        Common.merge_datasets(first_ds_output_path, snd_ds_output_path, "name", merged_ds_output_path)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
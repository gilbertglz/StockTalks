import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup as bs
import json
import requests


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Define the subreddit to scrape
    subreddit_name = 'stocks'
    # StockMarket
    # Specify the number of posts to scrape
    num_posts = 50

    # Make a GET request to the Reddit API
    url = f'https://www.reddit.com/r/{subreddit_name}/top.json?sort=new&limit={num_posts}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    # Process the JSON response
    data = response.json()
    posts = data['data']['children']
    lists = []
    for post in posts:
        lists.append(post['data'])
    # print(posts[0]['data'])
    # Extract the titles from the posts

    # Create a DataFrame from the titles
    colRemoves = ['subreddit', 'approved_at_utc', 'is_video', 'media', 'num_crossposts', 'created_utc',
                  'subreddit_subscribers', 'url', 'stickied', 'parent_whitelist_status', 'permalink',
                  'author_flair_text_color', 'author_patreon_flair', 'mod_reports', 'contest_mode', 'whitelist_status',
                  'send_replies', 'num_comments', 'discussion_type', 'author', 'report_reasons', 'is_robot_indexable',
                  'id', 'link_flair_background_color', 'removal_reason', 'mod_reason_by', 'author_is_blocked',
                  'subreddit_id', 'distinguished', 'num_reports', 'removed_by', 'visited', 'treatment_tags',
                  'author_flair_text', 'locked', 'spoiler', 'can_gild', 'link_flair_template_id', 'media_only',
                  'awarders', 'all_awardings', 'over_18', 'pinned', 'is_crosspostable', 'no_follow', 'archived',
                  'view_count', 'banned_at_utc', 'suggested_sort', 'likes', 'selftext_html', 'allow_live_comments',
                  'domain', 'author_flair_type', 'banned_by', 'removed_by_category', 'wls', 'link_flair_type',
                  'created', 'mod_note', 'is_self', 'content_categories', 'gildings', 'author_flair_richtext',
                  'author_flair_css_class', 'edited', 'thumbnail', 'author_premium', 'is_created_from_ads_ui',
                  'approved_by', 'author_flair_background_color', 'author_flair_template_id', 'author_fullname',
                  'can_mod_post', 'category', 'clicked', 'hidden', 'user_reports', 'total_awards_received',
                  'top_awarded_type', 'subreddit_name_prefixed', 'subreddit_type', 'gilded', 'hide_score', 'is_meta',
                  'is_original_content', 'is_reddit_media_domain', 'link_flair_css_class', 'link_flair_richtext',
                  'media_embed', 'secure_media_embed', 'secure_media', 'saved', 'quarantine', 'pwls', 'name',
                  'mod_reason_title', 'link_flair_text_color', 'score']
    df = pd.DataFrame(lists)
    df = df.drop(colRemoves, axis='columns')
    df = df.sort_index(axis='columns', ascending=False)
    print(df)

    # print(df.columns.values)
    # Print the DataFrame
    # print(df)
    # Process and print the titles of the scraped posts
    # for post in posts:
    #     title = post['data']['title']
    #     print(title)

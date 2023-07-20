import pandas as pd
import requests
import re
import re

import pandas as pd
import requests


def redditScrape():
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)

    # Define the subreddit to scrape
    subreddit_name = ['stocks', 'StockMarket']
    num_posts = 45
    lists = []
    for name in subreddit_name:
        # Make a GET request to the Reddit API
        url = f'https://www.reddit.com/r/{name}/new.json?sort=new&limit={num_posts}&t=week'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)

        # Process the JSON response
        data = response.json()
        posts = data['data']['children']

        for post in posts:
            lists.append(post['data'])

    columns_to_remove = ['approved_at_utc', 'is_video', 'media', 'num_crossposts', 'created_utc',
                         'subreddit_subscribers', 'url', 'stickied', 'parent_whitelist_status', 'permalink',
                         'author_flair_text_color', 'author_patreon_flair', 'mod_reports', 'contest_mode',
                         'whitelist_status',
                         'send_replies', 'num_comments', 'discussion_type', 'author', 'report_reasons',
                         'is_robot_indexable',
                         'id', 'link_flair_background_color', 'removal_reason', 'mod_reason_by', 'author_is_blocked',
                         'subreddit_id', 'distinguished', 'num_reports', 'removed_by', 'visited', 'treatment_tags',
                         'author_flair_text', 'locked', 'spoiler', 'can_gild', 'link_flair_template_id', 'media_only',
                         'awarders', 'all_awardings', 'over_18', 'pinned', 'is_crosspostable', 'no_follow', 'archived',
                         'view_count', 'banned_at_utc', 'suggested_sort', 'likes', 'selftext_html',
                         'allow_live_comments',
                         'domain', 'author_flair_type', 'banned_by', 'removed_by_category', 'wls', 'link_flair_type',
                         'created', 'mod_note', 'is_self', 'content_categories', 'gildings', 'author_flair_richtext',
                         'author_flair_css_class', 'edited', 'thumbnail', 'author_premium', 'is_created_from_ads_ui',
                         'approved_by', 'author_flair_background_color', 'author_flair_template_id', 'author_fullname',
                         'can_mod_post', 'category', 'clicked', 'hidden', 'user_reports', 'total_awards_received',
                         'top_awarded_type', 'subreddit_name_prefixed', 'subreddit_type', 'gilded', 'hide_score',
                         'is_meta',
                         'is_original_content', 'is_reddit_media_domain', 'link_flair_css_class', 'link_flair_richtext',
                         'media_embed', 'secure_media_embed', 'secure_media', 'saved', 'quarantine', 'pwls', 'name',
                         'mod_reason_title', 'link_flair_text_color', 'score', 'url_overridden_by_dest', 'gallery_data',
                         'is_gallery', 'thumbnail_height', 'media_metadata', 'preview', 'thumbnail_width', 'downs',
                         'post_hint']
    # Create a DataFrame from the scrape
    df = pd.DataFrame(lists)
    # Remove Columns not needed
    df = df.drop(columns_to_remove, axis='columns')
    # Move text column to end
    columnToMove = df.pop('selftext')
    df = df.sort_index(axis='columns', ascending=True)
    df['selftext'] = columnToMove
    df['Stock'] = df['title'].apply(extract_stock_tickers)
    companyNamesSymbols = {}
    companyNameFull = []
    companySymbols = []
    for stockCompany in df['Stock']:
        companyRow = stockCompany.split(',')
        companyNameFull = [company.strip() for company in companyRow]
        # print(companyNameFull)
        updatedStockSymbol = []

        # pass to yf to check for ticker
        for singleCompany in companyNameFull:
            if singleCompany in companyNamesSymbols:
                singleCompany = companyNamesSymbols[singleCompany]
            elif singleCompany.strip() != "":
                companyNamesSymbols[singleCompany] = find_company_ticker(singleCompany)
                singleCompany = companyNamesSymbols[singleCompany]
            updatedStockSymbol.append(singleCompany)
        updatedStockSymbol = [item for item in updatedStockSymbol if item.strip() != ""]
        companyRow = ','.join(updatedStockSymbol)
        companySymbols.append(companyRow)
    df['Symbols'] = companySymbols
    print(df.to_string)
    exportToCSV(df)
def extract_stock_tickers(text):
    regex_pattern = r'\b[A-Z$][A-Za-z0-9]+\b'  # Regex pattern to match uppercase letters (potential ticker symbols)
    matches = re.findall(regex_pattern, text)
    return ', '.join(matches)
def find_company_ticker(company):
    url = f'https://query2.finance.yahoo.com/v1/finance/search?q={company}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    data = response.json()
    if len(data['quotes']) > 0:
        if data['quotes'][0]['quoteType'] not in ['EQUITY']:
            return ""
        else:
            return data['quotes'][0]['symbol']
    else:
        return ""
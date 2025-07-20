from pytrends.request import TrendReq

def get_trending_topics():
    """
    Gets trending MikroTik topics from Google Trends.
    """
    print("Scanning for trending topics...")
    pytrends = TrendReq(hl='en-US', tz=360)

    # Get related queries for "MikroTik"
    pytrends.build_payload(kw_list=['MikroTik'])
    related_queries = pytrends.related_queries()

    # Extract rising queries
    if 'rising' in related_queries['MikroTik']:
        rising_topics = related_queries['MikroTik']['rising']['query'].tolist()
        print(f"Found rising topics: {rising_topics}")
        return rising_topics
    else:
        print("No rising topics found. Using default topics.")
        return ["MikroTik setup", "MikroTik firewall", "MikroTik VPN"]

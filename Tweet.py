from dotenv import load_dotenv
import os
import tweepy

EXPANSIONS = {
    "expansions": [
        "author_id",
        "referenced_tweets.id",
        "referenced_tweets.id.author_id",
        "entities.mentions.username",
        "attachments.poll_ids",
        "attachments.media_keys",
        "in_reply_to_user_id",
        "geo.place_id",
    ],
    "media_fields": [
        "alt_text",
        "duration_ms",
        "height",
        "media_key",
        "non_public_metrics",
        "organic_metrics",
        "preview_image_url",
        "promoted_metrics",
        "public_metrics",
        "type",
        "url",
        "variants",
        "width",
    ],
    "place_fields": [
        "contained_within",
        "country",
        "country_code",
        "full_name",
        "geo",
        "id",
        "name",
        "place_type",
    ],
    "poll_fields": [
        "duration_minutes",
        "end_datetime",
        "id",
        "options",
        "voting_status",
    ],
    "safe_tweet_fields": [
        "attachments",
        "author_id",
        "context_annotations",
        "conversation_id",
        "created_at",
        "entities",
        "geo",
        "id",
        "in_reply_to_user_id",
        "lang",
        "possibly_sensitive",
        "public_metrics",
        "referenced_tweets",
        "reply_settings",
        "source",
        "text",
        "withheld",
    ],
    "user_fields": [
        "created_at",
        "description",
        "entities",
        "id",
        "location",
        "name",
        "pinned_tweet_id",
        "profile_image_url",
        "protected",
        "public_metrics",
        "url",
        "username",
        "verified",
        "withheld",
    ],
}

tweet_fields = [
    "attachments",
    "author_id",
    "context_annotations",
    "conversation_id",
    "created_at",
    "entities",
    "geo",
    "id",
    "in_reply_to_user_id",
    "lang",
    "non_public_metrics",
    "organic_metrics",
    "possibly_sensitive",
    "promoted_metrics",
    "public_metrics",
    "referenced_tweets",
    "reply_settings",
    "source",
    "text",
    "withheld",
]


class Tweet:
    def __init__(self, tweet_link: str) -> None:
        load_dotenv()
        self.client = tweepy.Client(os.getenv("BEARER_TOKEN"))
        self.tweet_link = tweet_link
        print("xxxxxxxxxxxxxxxxxxx", tweet_link)
        self.tweet_id = int(tweet_link.split("/")[-1])
        self.get_tweet()

    def get_tweet(self) -> None:
        self.tweet = self.client.get_tweet(
            self.tweet_id,
            expansions=EXPANSIONS["expansions"],
            media_fields=EXPANSIONS["media_fields"],
            place_fields=EXPANSIONS["place_fields"],
            poll_fields=EXPANSIONS["poll_fields"],
            user_fields=EXPANSIONS["user_fields"],
            tweet_fields=EXPANSIONS["safe_tweet_fields"],
        )


if __name__ == "__main__":
    t = Tweet("https://twitter.com/CuteYuriBot/status/1564629701515149317")
    print(t.tweet)

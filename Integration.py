from Database import UserModel, TweetModel, MediaModel, engine
from sqlalchemy.orm import sessionmaker
from Tweet import Tweet
from ImageDownloader import get_avatar, get_media

Session = sessionmaker(bind=engine)
session = Session()


def fetch_tweet(url: str, force: bool = False) -> dict:
    tweet = Tweet(url)
    mapper(tweet, force)
    x = session.query(TweetModel).get(tweet.tweet_id)
    d = dict()
    d["url"] = x.url
    d["text"] = x.text
    d["reply_count"] = x.reply_count
    d["retweet_count"] = x.retweet_count
    d["like_count"] = x.like_count
    d["quote_count"] = x.quote_count
    d["created_at"] = x.created_at
    d["source"] = x.source
    d["author_image"] = x.user.profile_image_local[1:]
    d["author_url"] = x.user.url[1:]
    d["author_name"] = x.user.name
    d["author_handle"] = x.user.handle
    d["medias"] = [i.local_url[1:] for i in x.medias]
    return d


def mapper(tweet: Tweet, force: bool = False) -> None:
    users = tweet.tweet.includes["users"]
    for user in users:
        u = session.query(UserModel).get(user.id)
        if not u:
            u = UserModel(
                user_id=user.id,
                handle=user.username,
                name=user.name,
                created_at=user.created_at,
                description=user.description,
                verified=user.verified,
                protected=user.protected,
                location=user.location,
                profile_image_url=user.profile_image_url,
                followers_count=user.public_metrics["followers_count"],
                following_count=user.public_metrics["following_count"],
                tweet_count=user.public_metrics["tweet_count"],
                url=f"https://twitter.com/{user.username}",
            )
            u.profile_image_local = get_avatar(user.profile_image_url, user.id)
            session.add(u)
            session.commit()
        elif force:
            # update user
            pass
        else:
            pass

    obj = tweet.tweet.data
    t = session.query(TweetModel).get(obj.id)
    if not t:
        t = TweetModel(
            tweet_id=obj.id,
            text=obj.text,
            author_id=obj.author_id,
            created_at=obj.created_at,
            top_tweet_id=obj.conversation_id,
            possibly_sensitive=obj.possibly_sensitive,
            source=obj.source,
            retweet_count=obj.public_metrics["retweet_count"],
            like_count=obj.public_metrics["like_count"],
            reply_count=obj.public_metrics["reply_count"],
            quote_count=obj.public_metrics["quote_count"],
            url=tweet.tweet_link,
        )
        session.add(t)
        session.commit()
    elif force:
        # update user
        pass
    else:
        pass

    if "media" in tweet.tweet.includes:
        medias = tweet.tweet.includes["media"]
        for media in medias:
            m = session.query(MediaModel).get(media.media_key)
            if not m:
                m = MediaModel(
                    media_id=media.media_key,
                    type=media.type,
                    url=media.url,
                    height=media.height,
                    width=media.width,
                    alt_text=media.alt_text,
                    tweet_id=obj.id,
                )
                m.local_url = get_media(media.url, media.media_key)
                session.add(m)
                session.commit()
            elif force:
                # update user
                pass
            else:
                pass


if __name__ == "__main__":
    x = fetch_tweet("https://twitter.com/itstimetogetgay/status/1564839530858954753")

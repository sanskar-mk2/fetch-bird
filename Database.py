from Tweet import Tweet
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    create_engine,
)

Base = declarative_base()
engine = create_engine("sqlite:///test.db", echo=True)
connection = engine.connect()


class TweetModel(Base):
    __tablename__ = "tweets"
    tweet_id = Column(Integer, primary_key=True)
    text = Column(String(512))
    author_id = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(DateTime)
    top_tweet_id = Column(Integer)
    possibly_sensitive = Column(Boolean)
    source = Column(String(256))
    retweet_count = Column(Integer)
    like_count = Column(Integer)
    reply_count = Column(Integer)
    quote_count = Column(Integer)
    medias = relationship("MediaModel", back_populates="tweet")
    user = relationship("UserModel", back_populates="tweets")
    url = Column(String(512))

    def __repr__(self) -> str:
        return f"{self.tweet_id} {self.text}"


class MediaModel(Base):
    __tablename__ = "medias"
    media_id = Column(String(256), primary_key=True)
    type = Column(String(32))
    url = Column(String(256))
    local_url = Column(String(256))
    height = Column(Integer)
    width = Column(Integer)
    alt_text = Column(String(1024), nullable=True)
    tweet_id = Column(Integer, ForeignKey("tweets.tweet_id"))
    tweet = relationship("TweetModel", back_populates="medias")

    def __repr__(self) -> str:
        return f"{self.url} alt=\"{self.alt_text or ''}\""


class UserModel(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    name = Column(String(512))
    handle = Column(String(256))
    created_at = Column(DateTime)
    description = Column(String(1024), nullable=True)
    verified = Column(Boolean)
    protected = Column(Boolean)
    location = Column(String(256), nullable=True)
    profile_image_url = Column(String(512), nullable=True)
    profile_image_local = Column(String(512), nullable=True)
    followers_count = Column(Integer)
    following_count = Column(Integer)
    tweet_count = Column(Integer)
    url = Column(String(512))
    tweets = relationship("TweetModel", back_populates="user")

    def __repr__(self) -> str:
        return f"@{self.handle} {self.url}"


Base.metadata.create_all(engine)

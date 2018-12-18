from random import choice
from typing import List

from pydantic import BaseModel

from fastapi import Cookie, Depends, FastAPI

app = FastAPI()


class InterestsTracker(BaseModel):
    track_code: str
    interests: List[str]


fake_tracked_users_db = {
    "Foo": {"track_code": "Foo", "interests": ["sports", "movies"]},
    "Bar": {"track_code": "Bar", "interests": ["food", "shows"]},
    "Baz": {"track_code": "Baz", "interests": ["gaming", "virtual reality"]},
}


async def get_tracked_interests(track_code: str = Cookie(None)):
    if track_code in fake_tracked_users_db:
        track_dict = fake_tracked_users_db[track_code]
        track = InterestsTracker(**track_dict)
        return track
    return None


class ComplexTracker:
    def __init__(self, tracker: InterestsTracker = Depends(get_tracked_interests)):
        self.tracker = tracker

    def random_interest(self):
        """
        Get a random interest from the tracked ones for the current user.
        If the user doesn't have tracked interests, return a random one from the ones available.
        """
        if self.tracker.interests:
            return choice(self.tracker.interests)
        return choice(
            ["sports", "movies", "food", "shows", "gaming", "virtual reality"]
        )


@app.get("/suggested-category")
async def read_suggested_category(tracker: ComplexTracker = Depends(None)):
    response = {"category": tracker.random_interest()}
    return response

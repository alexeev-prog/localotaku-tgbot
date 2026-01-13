from dataclasses import dataclass


@dataclass
class Genre:
    id: int
    name: str


@dataclass
class OriginalMangaAuthor:
    id: int
    name: str


@dataclass
class AnimeStudio:
    id: int
    name: str


@dataclass
class Anime:
    id: int
    title: str
    title_english: str | None
    title_japanese: str | None
    image_url: str
    synopsis: str | None
    score: float | None
    episodes: int | None
    seasons: int | None
    films: int | None
    status: str
    genres: list[Genre]
    studios: list[AnimeStudio]
    manga_authors: list[OriginalMangaAuthor]
    year: int | None
    season: str | None

    @property
    def display_title(self) -> str:
        return self.title_english or self.title_japanese or self.title

    def get_genres_string(self) -> str:
        return ", ".join([genre.name for genre in self.genres])

    def get_seasons_string(self) -> str:
        if self.seasons == 1:
            return "1 Сезон"
        elif self.seasons > 1 and self.seasons < 5:
            return f"{self.seasons} Сезона"
        else:
            return f"{self.seasons} Сезонов"

    def get_films_string(self) -> str:
        if self.films == 0:
            return "Нет фильмов"
        elif self.films == 1:
            return "1 Фильм"
        elif self.films > 1 and self.films < 5:
            return f"{self.films} Фильма"
        else:
            return f"{self.films} Фильмов"

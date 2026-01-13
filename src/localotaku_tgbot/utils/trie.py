from typing import Dict, List, Optional, Set
import unicodedata
import re

from localotaku_tgbot.entites.core import Anime


class TrieNode:
    __slots__ = ("children", "is_end_of_word", "anime_ids")

    def __init__(self) -> None:
        self.children: Dict[str, TrieNode] = {}
        self.is_end_of_word: bool = False
        self.anime_ids: Set[int] = set()


class AnimeTrie:
    def __init__(self) -> None:
        self._root = TrieNode()
        self._anime_by_id: Dict[int, Anime] = {}
        self._genre_trie = TrieNode()
        self._studio_trie = TrieNode()

    def _normalize_text(self, text: str) -> str:
        normalized = unicodedata.normalize("NFKD", text)
        normalized = "".join(c for c in normalized if not unicodedata.combining(c))
        normalized = normalized.lower().strip()
        normalized = re.sub(r"[^\w\s-]", "", normalized)
        normalized = re.sub(r"\s+", " ", normalized)
        return normalized

    def _add_to_trie(self, trie_root: TrieNode, text: str, anime_id: int) -> None:
        node = trie_root
        normalized_text = self._normalize_text(text)

        for char in normalized_text:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.anime_ids.add(anime_id)

        node.is_end_of_word = True
        node.anime_ids.add(anime_id)

    def _search_in_trie(self, trie_root: TrieNode, prefix: str) -> Set[int]:
        node = trie_root
        normalized_prefix = self._normalize_text(prefix)

        for char in normalized_prefix:
            if char not in node.children:
                return set()
            node = node.children[char]

        return node.anime_ids

    def add_anime(self, anime: Anime) -> None:
        if anime.id in self._anime_by_id:
            return

        self._anime_by_id[anime.id] = anime

        titles = {
            anime.title,
            anime.display_title,
            anime.title_english or "",
            anime.title_japanese or "",
        }

        for title in titles:
            if title.strip():
                self._add_to_trie(self._root, title, anime.id)

        for genre in anime.genres:
            self._add_to_trie(self._genre_trie, genre.name, anime.id)

        for studio in anime.studios:
            self._add_to_trie(self._studio_trie, studio.name, anime.id)

    def search_by_title(self, prefix: str, limit: Optional[int] = None) -> List[Anime]:
        anime_ids = self._search_in_trie(self._root, prefix)
        results = [self._anime_by_id[anime_id] for anime_id in sorted(anime_ids)]

        if limit:
            results = results[:limit]

        return results

    def search_by_genre(self, genre_prefix: str) -> List[Anime]:
        anime_ids = self._search_in_trie(self._genre_trie, genre_prefix)
        return [self._anime_by_id[anime_id] for anime_id in sorted(anime_ids)]

    def search_by_studio(self, studio_prefix: str) -> List[Anime]:
        anime_ids = self._search_in_trie(self._studio_trie, studio_prefix)
        return [self._anime_by_id[anime_id] for anime_id in sorted(anime_ids)]

    def advanced_search(
        self,
        title_prefix: Optional[str] = None,
        genre_prefix: Optional[str] = None,
        studio_prefix: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Anime]:
        result_ids: Optional[Set[int]] = None

        if title_prefix:
            result_ids = self._search_in_trie(self._root, title_prefix)

        if genre_prefix:
            genre_ids = self._search_in_trie(self._genre_trie, genre_prefix)
            result_ids = (
                genre_ids if result_ids is None else result_ids.intersection(genre_ids)
            )

        if studio_prefix:
            studio_ids = self._search_in_trie(self._studio_trie, studio_prefix)
            result_ids = (
                studio_ids
                if result_ids is None
                else result_ids.intersection(studio_ids)
            )

        if result_ids is None:
            result_ids = set(self._anime_by_id.keys())

        results = [self._anime_by_id[anime_id] for anime_id in sorted(result_ids)]

        if limit:
            results = results[:limit]

        return results

    def get_all_anime(self) -> List[Anime]:
        return sorted(self._anime_by_id.values(), key=lambda a: a.display_title.lower())

    def remove_anime(self, anime_id: int) -> bool:
        if anime_id not in self._anime_by_id:
            return False

        del self._anime_by_id[anime_id]

        return True

    def clear(self) -> None:
        self._root = TrieNode()
        self._genre_trie = TrieNode()
        self._studio_trie = TrieNode()
        self._anime_by_id.clear()

    @property
    def total_anime(self) -> int:
        return len(self._anime_by_id)

    def get_suggestions(self, prefix: str, max_suggestions: int = 10) -> List[str]:
        suggestions = set()
        node = self._root
        normalized_prefix = self._normalize_text(prefix)

        for char in normalized_prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        stack = [(node, normalized_prefix)]

        while stack and len(suggestions) < max_suggestions:
            current_node, current_word = stack.pop()

            if current_node.is_end_of_word:
                for anime_id in current_node.anime_ids:
                    if anime_id in self._anime_by_id:
                        anime = self._anime_by_id[anime_id]
                        suggestions.add(anime.display_title)
                        if len(suggestions) >= max_suggestions:
                            break

            for char, child_node in current_node.children.items():
                stack.append((child_node, current_word + char))

        return sorted(list(suggestions))

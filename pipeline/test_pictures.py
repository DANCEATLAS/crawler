"""Offline checks for the picture search of 24 November 2026: a picture found near a dance is kept only when a reader
says it shows the dance; a source that could not be reached is not written down as an empty one."""
import datetime as dt
import json
import unittest
from unittest.mock import Mock, patch

from . import common, pictures, sources
from .common import jload
from .test_foundation import TemporaryProject, record


def image(n, **more):
    return dict({"title": f"File:Picture {n}.jpg", "url": f"https://upload.example.org/{n}.jpg", "thumb": f"https://upload.example.org/thumb/{n}.jpg",
                 "width": 1200, "height": 800, "license": "CC BY-SA 4.0", "license_url": "https://creativecommons.org/licenses/by-sa/4.0",
                 "artist": "A photographer", "description": f"picture {n}", "source_page": f"https://commons.example.org/{n}",
                 "attribution": "A photographer / Wikimedia Commons / CC BY-SA 4.0", "categories": "Dances; People"}, **more)


class Places:
    """The places a picture is looked for, as pipeline/sources.py offers them."""

    def __init__(self, category=(), articles=None, search=(), links=None, down=()):
        self.category, self.articles, self.search, self.links, self.down, self.asked = list(category), articles or {}, list(search), links or {}, set(down), []

    def _reach(self, place):
        self.asked.append(place)
        if place.split(":")[0] in self.down:
            raise OSError("the source cannot be reached")

    def wikidata_entity(self, qid):
        return {"claims": {"commons_category": ["The dance"]}}

    def wikidata_sitelinks(self, qid):
        self._reach("links")
        return self.links

    def commons_category_images(self, category):
        self._reach("category:" + category)
        return self.category

    def wiki_images_in(self, lang, title):
        self._reach(f"article:{lang}:{title}")
        return self.articles.get(lang, [])

    def commons_images_search(self, name):
        self._reach("search:" + name)
        return self.search


def dance(slug="a", qid="Q1", images=None, aliases=()):
    rec = record(slug)
    rec["wikidata_qid"], rec["profile"]["aliases"] = qid, list(aliases)
    if images is not None:
        rec["images"] = images
    return rec


class CandidateTests(unittest.TestCase):
    def test_the_surest_place_first_and_every_picture_says_where_it_was_found(self):
        places = Places(category=[image(1)], articles={"es": [image(2), image(1)], "zz": [image(4)]}, search=[image(3)],
                        links={"en": "The dance", "zz": "Dance zz", "es": "El baile"})
        found, down = pictures.candidates(dance(aliases=["Other name"]), places)
        self.assertEqual(([f["url"][-5:] for f in found], down), (["1.jpg", "2.jpg", "4.jpg", "3.jpg"], 0))      # no picture twice
        self.assertEqual([f["found_in"].split()[1] for f in found], ["Commons", "article", "article", "search"])
        self.assertNotIn("article:en:The dance", places.asked)                                                   # research already looked there
        self.assertEqual([a for a in places.asked if a.startswith("search")], ["search:a", "search:Other name"])

    def test_a_place_that_cannot_be_reached_is_counted_and_the_others_are_still_asked(self):
        places = Places(category=[image(1)], search=[image(3)], links={"es": "El baile"}, down=("category", "article"))
        found, down = pictures.candidates(dance(), places)
        self.assertEqual(([f["url"][-5:] for f in found], down), (["3.jpg"], 2))

    def test_a_dance_without_a_wikidata_item_is_searched_by_name_only(self):
        places = Places(search=[image(3)])
        found, down = pictures.candidates(dance(qid=None), places)
        self.assertEqual((len(found), down, places.asked), (1, 0, ["search:a"]))


class StageTests(TemporaryProject):
    def project(self, recs):
        self.save("pipeline_state/research_index.json", {r["slug"]: {"status": "researched"} for r in recs})
        for r in recs:
            self.save(f"research_results/{r['slug']}.json", r)

    def night(self, places, answers, budget=60, served=True, today=dt.date(2026, 11, 24)):
        llm = Mock(enabled=True, unserved=0, why={})

        def one(system, user, **kw):
            answer = answers.pop(0)
            if answer is None and not served:
                llm.unserved += 1
            return answer
        llm.json.side_effect = one
        look = pictures.candidates                                   # the real search, over the places of this test
        with patch.object(common, "LLM", return_value=llm), patch.object(pictures, "candidates", side_effect=lambda rec: look(rec, places)):
            result = pictures.run(budget=budget, today=today)
        return result, llm

    def test_a_kept_picture_is_written_into_the_record_and_the_reader_s_field_is_not_stored(self):
        self.project([dance("a"), dance("b", images=[image(9)])])
        places = Places(category=[image(1), image(2)])
        result, llm = self.night(places, [{"pictures": [{"n": 1, "verdict": "no"}, {"n": 2, "verdict": "yes"}]}])
        rec = jload("research_results/a.json")
        self.assertEqual([i["url"] for i in rec["images"]], ["https://upload.example.org/2.jpg"])
        self.assertNotIn("categories", rec["images"][0])
        self.assertEqual(rec["images"][0]["found_in"], "the Commons category of its Wikidata item")
        self.assertEqual(jload("pipeline_state/research_index.json")["a"]["images"], 1)
        self.assertEqual(llm.json.call_count, 1)                                         # the dance that has a picture is not asked about
        asked = json.loads(llm.json.call_args.args[1])
        self.assertEqual((asked["dance"]["name"], asked["pictures"][0]["categories"]), ("a", "Dances; People"))
        self.assertEqual({k: result["counters"].get(k) for k in ("searched", "pictures_kept", "pictures_left_out", "profiles_given_a_picture")},
                         {"searched": 1, "pictures_kept": 1, "pictures_left_out": 1, "profiles_given_a_picture": 1})

    def test_nothing_found_or_nothing_kept_is_remembered_and_looked_for_again_after_a_while(self):
        self.project([dance("a"), dance("b")])
        result, _ = self.night(Places(), [])
        self.assertEqual((result["counters"]["nothing_found"], sorted(jload("pipeline_state/picture_finds.json"))), (2, ["a", "b"]))
        again, llm = self.night(Places(category=[image(1)]), [], today=dt.date(2026, 12, 20))
        self.assertEqual((again["counters"].get("searched"), llm.json.call_count), (None, 0))                # 26 days later: not yet
        later, llm = self.night(Places(category=[image(1)]), [{"pictures": [{"n": 1, "verdict": "unsure"}]}] * 2, today=dt.date(2027, 1, 15))
        self.assertEqual((later["counters"]["searched"], later["counters"]["nothing_kept"]), (2, 2))

    def test_a_source_that_was_down_is_not_written_down_as_nothing_there(self):
        self.project([dance("a")])
        result, _ = self.night(Places(down=("category", "search", "links")), [])
        self.assertEqual((result["counters"]["search_incomplete"], result["counters"]["places_not_reached"]), (1, 3))
        self.assertIsNone(jload("pipeline_state/picture_finds.json", None))                                  # tried again on the next run

    def test_pictures_kept_once_are_put_back_when_research_writes_the_record_anew(self):
        self.project([dance("a")])
        self.night(Places(category=[image(1)]), [{"pictures": [{"n": 1, "verdict": "yes"}]}])
        self.save("research_results/a.json", dance("a"))                                                    # a deepening found no picture in the article
        result, llm = self.night(Places(), [])
        self.assertEqual((result["counters"]["put_back"], llm.json.call_count), (1, 0))
        self.assertEqual(jload("research_results/a.json")["images"][0]["url"], "https://upload.example.org/1.jpg")

    def test_the_dance_a_picture_would_bring_to_the_line_is_looked_for_first(self):
        self.project([dance("a"), dance("b"), dance("c")])
        self.save("pipeline_state/active_ready.json", {"profiles": {"a": {"state": "building", "missing": ["picture", "mistakes"]},
                                                                      "c": {"state": "building", "missing": ["picture"]}}})
        result, llm = self.night(Places(category=[image(1)]), [{"pictures": [{"n": 1, "verdict": "yes"}]}] * 2, budget=2)
        self.assertEqual([json.loads(c.args[1])["dance"]["name"] for c in llm.json.call_args_list], ["c", "a"])
        self.assertEqual(result["counters"]["waiting"], 1)

    def test_the_stage_stops_after_three_dances_in_a_row_no_model_answered(self):
        self.project([dance(s) for s in "abcde"])
        result, llm = self.night(Places(category=[image(1)]), [None, None, None, None], served=False)
        self.assertEqual((llm.json.call_count, result["counters"]["stopped_early"]), (3, 1))
        self.assertIsNone(jload("pipeline_state/picture_finds.json", None))


class SourceTests(unittest.TestCase):
    """The shapes are those Wikimedia's API answered with on 24 November 2026."""
    INFO = {"query": {"pages": [
        {"title": "File:Melbourne shuffle.jpg", "imageinfo": [{"url": "https://upload.wikimedia.org/a.jpg", "thumburl": "https://upload.wikimedia.org/t/a.jpg", "width": 2976, "height": 3968, "mime": "image/jpeg",
                                                               "extmetadata": {"LicenseShortName": {"value": "CC BY-SA 4.0"}, "Artist": {"value": "<a href='x'>Someone</a>"},
                                                                               "ImageDescription": {"value": "La roba del melbourne shuffle"}, "Categories": {"value": "Self-published work|Dance"}}}]},
        {"title": "File:Small.jpg", "imageinfo": [{"url": "u", "width": 500, "height": 372, "extmetadata": {"LicenseShortName": {"value": "CC BY 2.0"}}}]},
        {"title": "File:Not free.jpg", "imageinfo": [{"url": "u", "width": 2000, "height": 2000, "extmetadata": {"LicenseShortName": {"value": "Fair use"}}}]}]}}

    def fetch(self, fn, first, *args):
        calls = []

        def get_json(url, **kw):
            calls.append(url)
            return first if len(calls) == 1 else self.INFO
        with patch.object(sources, "get_json", side_effect=get_json), patch.object(sources, "cached", side_effect=lambda key, f, **kw: f()):
            return fn(*args), calls

    def test_titles_from_another_language_are_given_commons_own_word_and_icons_are_left_out(self):
        self.assertEqual(sources.picture_titles(["Archivo:Rueda.JPG", "Archivo:Commons-logo.svg", "Fichier:Carte.png", "File:Flag of Cuba.png", "Archivo:Rueda.JPG", None]),
                         ["File:Rueda.JPG", "File:Carte.png"])

    def test_the_article_in_another_language(self):
        out, calls = self.fetch(sources.wiki_images_in, {"query": {"pages": [{"title": "Rueda de casino", "images": [{"title": "Archivo:Melbourne shuffle.jpg"}, {"title": "Archivo:Wikidata-logo.svg"}]}]}}, "es", "Rueda de casino")
        self.assertTrue(calls[0].startswith("https://es.wikipedia.org/w/api.php?") and "titles=File%3AMelbourne+shuffle.jpg" in calls[1])
        self.assertEqual([(i["title"], i["license"], i["artist"], i["categories"]) for i in out], [("File:Melbourne shuffle.jpg", "CC BY-SA 4.0", "Someone", "Self-published work; Dance")])
        self.assertEqual(sources.wiki_images_in("es; rm", "x"), [])

    def test_the_category_and_the_search(self):
        out, calls = self.fetch(sources.commons_category_images, {"query": {"categorymembers": [{"ns": 6, "title": "File:Melbourne shuffle.jpg"}, {"ns": 6, "title": "File:Dame con dos.webm"}]}}, "Rueda de casino")
        self.assertTrue("cmtitle=Category%3ARueda+de+casino" in calls[0] and len(out) == 1)
        out, calls = self.fetch(sources.commons_images_search, {"query": {"search": [{"ns": 6, "title": "File:Melbourne shuffle.jpg"}]}}, "Melbourne shuffle")
        self.assertTrue("srsearch=%22Melbourne+shuffle%22+filetype%3Abitmap" in calls[0] and len(out) == 1)

    def test_a_source_that_cannot_be_reached_raises_for_the_picture_search(self):
        with patch.object(sources, "get_json", side_effect=OSError("down")), patch.object(sources, "cached", side_effect=lambda key, f, **kw: f()):
            for fn, args in ((sources.wiki_images_in, ("es", "x")), (sources.commons_category_images, ("x",)), (sources.commons_images_search, ("Melbourne shuffle",)), (sources.wikidata_sitelinks, ("Q1",))):
                with self.assertRaises(OSError):
                    fn(*args)
        with patch.object(sources, "get_json", side_effect=[{"query": {"search": [{"title": "File:A.jpg"}]}}, OSError("commons down")]), patch.object(sources, "cached", side_effect=lambda key, f, **kw: f()):
            with self.assertRaises(OSError):                                             # the search answered, the file details did not
                sources.commons_images_search("Melbourne shuffle")

    def test_every_language_s_article(self):
        ent = {"entities": {"Q1": {"sitelinks": {"eswiki": {"title": "Rueda"}, "commonswiki": {"title": "Category:Rueda"}, "zh_yuewiki": {"title": "舞"}, "eswikiquote": {"title": "x"}}}}}
        with patch.object(sources, "get_json", return_value=ent), patch.object(sources, "cached", side_effect=lambda key, f, **kw: f()):
            self.assertEqual(sources.wikidata_sitelinks("Q1"), {"es": "Rueda", "zh-yue": "舞"})
        self.assertEqual(sources.wikidata_sitelinks("not an item"), {})


if __name__ == "__main__":
    unittest.main()

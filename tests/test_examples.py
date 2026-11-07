"""Проверки реальных функций из разборов: без сети и действующих токенов."""
import ast
import contextlib
import io
import json
import os
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

DOCS = Path(__file__).resolve().parents[1] / "docs"

def blocks(page):
    return re.findall(r'^```python\n(.*?)^```', (DOCS / page).read_text(), re.M | re.S)

def definitions(page):
    namespace = {}
    for code in blocks(page):
        tree = ast.parse(code)
        nodes = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef))]
        exec(compile(ast.Module(body=nodes, type_ignores=[]), page, "exec"), namespace)
    return namespace

class Examples(unittest.TestCase):
    def test_recursion_and_empty_children(self):
        ns = definitions("recursion.md")
        self.assertEqual(ns["sum_to"](0), 0)
        self.assertEqual(ns["sum_to"](5), 15)
        with self.assertRaises(ValueError): ns["sum_to"](-1)
        self.assertEqual(ns["count_tasks"]({"children": [{"children": []}]}), 2)

    def test_state_error_keeps_draft(self):
        ns = definitions("state-files.md")
        for text in ["abc", "0", "-2"]:
            draft = {"state": "quantity", "name": "Анна"}
            self.assertFalse(ns["set_quantity"](draft, text))
            self.assertEqual(draft, {"state": "quantity", "name": "Анна"})
        self.assertEqual(ns["next_state"]("menu", "create"), "input_name")
        self.assertEqual(ns["next_state"]("input_name", "invalid"), "input_name")

    def test_dates_and_finite_values(self):
        ns = definitions("dates-validation.md")
        self.assertIsNone(ns["parse_date"]("31.02.2026"))
        self.assertIsNotNone(ns["parse_date"]("29.02.2024"))
        for text in ["nan", "inf", "-inf", "0", "6", "abc"]:
            self.assertIsNone(ns["parse_rating"](text))
        self.assertEqual(ns["parse_rating"]("4.7"), 4.7)

    def test_independent_dataclass_lists(self):
        cls = definitions("dataclasses-crud.md")["Order"]
        first, second = cls(), cls()
        first.items.append("Чай")
        self.assertEqual(second.items, [])

    def test_crud_uses_id_and_preserves_failed_operation(self):
        ns = definitions("crud.md")
        items = [ns["Product"](30, "Чай", 5), ns["Product"](10, "Кофе", 2)]
        self.assertFalse(ns["sell"](items, 30, 6))
        self.assertEqual(items[0].stock, 5)
        self.assertTrue(ns["sell"](items, 30, 2))
        self.assertEqual(items[0].stock, 3)
        self.assertTrue(ns["delete_by_id"](items, 30))
        self.assertFalse(ns["delete_by_id"](items, 30))
        self.assertEqual(items[0].id, 10)

    def test_storage_and_duplicate_ids(self):
        ns = definitions("storage.md")
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "catalog.json"
            state = {"last_id": 9, "items": [{"id": 7, "name": "Чай"}]}
            ns["save_state"](path, state)
            self.assertEqual(json.loads(path.read_text()), state)
            self.assertFalse(path.with_name(path.name + ".tmp").exists())
        with self.assertRaises(ValueError): ns["validate_ids"]([{"id": 1}, {"id": 1}])

    def test_search_boundaries(self):
        ns = definitions("search-sort.md")
        items = [{"name": "Чай", "price": 100}, {"name": "Кофе", "price": 200}]
        self.assertEqual(ns["find_by_name"](items, " ЧАЙ "), items[:1])
        with self.assertRaises(ValueError): ns["find_by_name"](items, "  ")
        self.assertEqual(ns["filter_price"](items, 100, 200), items)
        with self.assertRaises(ValueError): ns["filter_price"](items, 200, 100)

    def test_generator_is_consumed(self):
        code = next(code for code in blocks("functional-tools.md") if code.startswith("amounts ="))
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream): exec(code, {})
        self.assertEqual(stream.getvalue().splitlines(), ["300", "[]"])

    def test_callback_payload_validation(self):
        code = next(code for code in blocks("bot-events.md") if "def parse_service_callback(" in code)
        namespace = {}
        with contextlib.redirect_stdout(io.StringIO()): exec(code, namespace)
        parse = namespace["parse_service_callback"]
        self.assertEqual(parse("service:7"), 7)
        for text in [None, "other:7", "service:0", "service:abc", "service:7:8"]:
            self.assertIsNone(parse(text))

    def test_fsm_context_is_separate_and_cancel_clears_it(self):
        try:
            import telebot
            from telebot import types
            from telebot.states.sync.context import StateContext
        except ImportError:
            self.skipTest("Для проверки FSM установите pyTelegramBotAPI")
        ns = {}
        with patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "123456:LOCAL_TEST_ONLY"}):
            for code in blocks("bot-ui.md"): exec(code, ns)
        sent = []
        ns["bot"].send_message = lambda chat_id, text, **kw: sent.append((chat_id, text))
        def event(user_id, text):
            return types.Message.de_json({"message_id": 1, "date": 0,
                "from": {"id": user_id, "is_bot": False, "first_name": "Test"},
                "chat": {"id": 100, "type": "private"}, "text": text})
        first = event(7, "/start")
        second = event(8, "/start")
        context1 = StateContext(first, ns["bot"])
        context2 = StateContext(second, ns["bot"])
        ns["start_order"](first, context1)
        ns["start_order"](second, context2)
        ns["accept_name"](event(7, " "), context1)
        self.assertEqual(context1.get(), ns["OrderStates"].name.name)
        ns["accept_name"](event(7, "Анна"), context1)
        self.assertEqual(context1.get(), ns["OrderStates"].quantity.name)
        with context1.data() as data: self.assertEqual(data["name"], "Анна")
        with context2.data() as data: self.assertNotIn("name", data)
        ns["cancel_order"](event(7, "/cancel"), context1)
        self.assertIsNone(context1.get())
        self.assertEqual(context2.get(), ns["OrderStates"].name.name)
        self.assertTrue(sent)

    def test_html_cards_and_missing_field(self):
        try: import bs4
        except ImportError: self.skipTest("Для парсинга установите beautifulsoup4")
        ns = definitions("parsing.md")
        html = '<article class="service"><h2>A</h2></article><article class="service"><h2>B</h2></article>'
        self.assertEqual(ns["service_names"](html), ["A", "B"])
        self.assertEqual(ns["service_names"](""), [])
        with self.assertRaises(ValueError): ns["service_names"]('<article class="service"></article>')

if __name__ == '__main__': unittest.main()

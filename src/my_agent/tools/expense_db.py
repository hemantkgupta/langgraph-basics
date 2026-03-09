from __future__ import annotations

_EXPENSE_DOCS = {
    "schema": (
        "Expense records usually include amount, merchant, category, currency, and "
        "created_at fields."
    ),
    "python-service": (
        "A Python service can store expenses with Pydantic models, validate input, "
        "and write records into SQLite or Postgres."
    ),
    "approval-flow": (
        "Expense approval workflows often route submitted reports to a manager before "
        "reimbursement is issued."
    ),
}


def search_expense_docs(question: str, *, limit: int = 2) -> list[str]:
    tokens = {
        token.strip(".,?!").lower()
        for token in question.split()
        if len(token.strip(".,?!")) >= 3
    }
    ranked_matches: list[tuple[int, str, str]] = []

    for title, body in _EXPENSE_DOCS.items():
        haystack = f"{title} {body}".lower()
        score = sum(token in haystack for token in tokens)
        if score:
            ranked_matches.append((score, title, body))

    if not ranked_matches:
        return [
            "No internal docs matched. In a real LangGraph agent this node would call "
            "a retriever or vector store."
        ]

    ranked_matches.sort(reverse=True)
    return [f"{title}: {body}" for _, title, body in ranked_matches[:limit]]

from src.main import build_agent


def main() -> None:
    agent = build_agent()
    result = agent.run(
        "failed login privilege escalation workstation-07",
        review_context={"mode": "auto", "reviewer": "demo-reviewer"},
    )
    print(result.final_report)


if __name__ == "__main__":
    main()

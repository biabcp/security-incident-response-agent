from src.tools.evidence_validator import EvidenceValidator


def test_evidence_validator_rejects_single_citation_for_many_events():
    validator = EvidenceValidator()
    evidence = [{"id": "evt-1"}, {"id": "evt-2"}, {"id": "evt-3"}]
    report = "Assessment: suspicious behavior [evt-1]"

    assert validator.has_citations(report, evidence) is False


def test_evidence_validator_accepts_grounded_report():
    validator = EvidenceValidator()
    evidence = [{"id": "evt-1"}, {"id": "evt-2"}, {"id": "evt-3"}]
    report = "Evidence reviewed [evt-1] [evt-2]"

    assert validator.has_citations(report, evidence) is True

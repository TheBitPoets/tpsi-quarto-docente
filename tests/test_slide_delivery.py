from scripts.build_slides import discover_decks, validate_sources


def test_tpsi4_slide_delivery_sources_are_complete_and_linked():
    validate_sources()
    assert len(discover_decks()) == 7

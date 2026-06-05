# Testing: https://w3c.github.io/core-aam/#role-map-link

TEST_HTML = "<div role='link' id='test'>content</div>"

def test_atspi(atspi, session, inline):
    session.url = inline(TEST_HTML)

    # Spec:
    # Role: ROLE_LINK
    # Interface: HyperlinkImpl

    node = atspi.find_node("test", session.url)
    assert atspi.Accessible.get_role(node) == atspi.Role.LINK
    assert atspi.Accessible.get_hypertext_iface(node) is not None

# def test_axapi(axapi, session, inline):
#     session.url = inline(TEST_HTML)
#
#     # Spec:
#     # AXRole: AXLink
#     # AXSubrole: <nil>

# def test_ia2(ia2, session, inline):
#     session.url = inline(TEST_HTML)
#
#     # Spec:
#     # <span class="property">Role: <code>ROLE_SYSTEM_LINK</code></span><br> <span class="property">State: <code>STATE_SYSTEM_LINKED</code></span><br> <span class="property">State: <code>STATE_SYSTEM_LINKED</code></span> on its descendants<br> <span class="property">Interface: <code>IAccessibleHypertext</code></span>

# def test_uia(uia, session, inline):
#     session.url = inline(TEST_HTML)
#
#     # Spec:
#     # Control Type: HyperLink
#     # Control Pattern: Value

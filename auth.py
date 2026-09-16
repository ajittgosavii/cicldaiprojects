"""Sign-in gate and the CIS CLD login page.

Accounts live in the app's secrets, never in the repo:

    [auth.users]
    alice = "pbkdf2_sha256$240000$<salt-hex>$<digest-hex>"

Create a hash with:  python -c "import auth; print(auth.hash_password('the-password'))"
"""

import hashlib
import hmac
import secrets
import time

import streamlit as st

LAB_NAME = "CIS CLD AI Applications"
COLLAB = "In Collaboration with ECHO AI Lab – Calgary"
MAX_ATTEMPTS, LOCKOUT_SECONDS = 5, 60
ITERATIONS = 240_000
# the Hexagon pillars' markers on the dark brand panel: the same six palette slots, stepped for a dark surface
PILLARS_ON_DARK = {
    "AI Strategy & Engineering": "#3987e5",
    "Data for AI": "#d95926",
    "Process AI": "#199e70",
    "Agentic Legacy Modernization": "#c98500",
    "Physical AI": "#d55181",
    "AI Trust": "#008300",
}


def hash_password(password: str, salt_hex: str | None = None, iterations: int = ITERATIONS) -> str:
    salt_hex = salt_hex or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), iterations)
    return f"pbkdf2_sha256${iterations}${salt_hex}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        _, iterations, salt_hex, digest = stored.split("$")
        candidate = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), int(iterations))
    except ValueError:
        return False
    return hmac.compare_digest(candidate.hex(), digest)


# checked against when the username is unknown, so a wrong username takes as long as a wrong password
_DUMMY_HASH = hash_password("unused", "00" * 16)


def _users() -> dict[str, str]:
    try:
        return {name: str(h) for name, h in st.secrets["auth"]["users"].items()}
    except Exception:  # no secrets file, or no [auth.users] section
        return {}


def logo_svg(size: int, uid: str) -> str:
    """Hexagon holding a cloud, with three data points rising into it.

    The parts carry classes so the login page can animate them; elsewhere they sit still.
    """
    dots = "".join(
        f'<circle class="lg-dot" cx="{cx}" cy="46" r="1.9" fill="url(#g{uid})" style="--d:{d}s"/>'
        for cx, d in ((26, 0), (32, 0.7), (38, 1.4))
    )
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 64 64" role="img" aria-label="CIS CLD logo" '
        f'xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g{uid}" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="#6FE3E1"/><stop offset="1" stop-color="#2743A8"/></linearGradient></defs>'
        f'<polygon class="lg-hex" points="32,3 57,17.5 57,46.5 32,61 7,46.5 7,17.5" fill="none" '
        f'stroke="url(#g{uid})" stroke-width="3.5" stroke-linejoin="round"/>'
        f'<path class="lg-cloud" d="M23 39.5h18a7.2 7.2 0 0 0 0.8-14.3A10.6 10.6 0 0 0 24.4 23.6 7 7 0 0 0 23 39.5z" '
        f'fill="none" stroke="url(#g{uid})" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round"/>'
        f"{dots}</svg>"
    )


_MESH = (
    "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='120' height='104' "
    "viewBox='0 0 120 104'><path d='M30 2 L60 19 L60 53 L30 70 L0 53 L0 19 Z M90 2 L120 19 L120 53 L90 70 "
    "L60 53 L60 19 Z M60 53 L90 70 L90 104 L60 121 L30 104 L30 70 Z' fill='none' stroke='%237FD6F5' "
    "stroke-width='1'/></svg>\")"
)

_LOGIN_CSS = """
<style>
  [data-testid="stHeader"] { display: none; }
  .block-container { max-width: none; padding: 0 !important; }
  .st-key-login_shell [data-testid="stHorizontalBlock"] { gap: 0; align-items: stretch !important; }
  .st-key-login_shell [data-testid="stColumn"]:nth-child(2) {
    align-self: stretch; min-height: 100vh; box-sizing: border-box; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    background: #fff; border-left: 1px solid var(--rule); padding: 3rem 2.5rem; }
  .st-key-login_shell [data-testid="stColumn"]:nth-child(2) > div {
    width: 100%; max-width: 23rem; flex: 0 0 auto !important; height: auto !important; }

  .brand { position: relative; overflow: hidden; min-height: 100vh; box-sizing: border-box; color: #fff;
           display: flex; flex-direction: column; justify-content: space-between; padding: 2.5rem 3.5rem 3rem;
           font-family: var(--body);
           background: linear-gradient(155deg, #0A1733 0%, #0E2551 55%, #091530 100%); }
  .brand > *:not(.fx) { position: relative; z-index: 2; }

  /* drifting colour fields */
  .fx { position: absolute; inset: 0; z-index: 0; pointer-events: none; }
  .aurora { filter: blur(70px); opacity: 0.55; }
  .aurora i { position: absolute; display: block; border-radius: 50%; }
  .aurora i:nth-child(1) { width: 44rem; height: 44rem; left: -10rem; top: -12rem;
    background: radial-gradient(circle, #1E63C8 0%, transparent 65%); animation: drift-a 26s ease-in-out infinite; }
  .aurora i:nth-child(2) { width: 34rem; height: 34rem; right: -10rem; top: 22%;
    background: radial-gradient(circle, #12A3A0 0%, transparent 65%); animation: drift-b 34s ease-in-out infinite; }
  .aurora i:nth-child(3) { width: 30rem; height: 30rem; left: 26%; bottom: -14rem;
    background: radial-gradient(circle, #4B37B3 0%, transparent 65%); animation: drift-c 40s ease-in-out infinite; }
  @keyframes drift-a { 0%,100% { transform: none; } 50% { transform: translate(5rem, 3rem) scale(1.12); } }
  @keyframes drift-b { 0%,100% { transform: none; } 50% { transform: translate(-4rem, -3rem) scale(1.18); } }
  @keyframes drift-c { 0%,100% { transform: none; } 50% { transform: translate(3rem, -4rem) scale(1.1); } }

  /* hexagon mesh, sliding slowly */
  .mesh { opacity: 0.14; animation: mesh-slide 60s linear infinite;
          background-image: MESH_URL; background-size: 120px 104px; }
  @keyframes mesh-slide { to { background-position: 120px 0; } }

  /* thin uplink streams */
  .uplink span { position: absolute; bottom: -20%; width: 1px; height: 24%;
    background: linear-gradient(to top, transparent, rgba(111,227,225,0.65), transparent);
    animation: rise 9s linear infinite; }
  @keyframes rise { 0% { transform: translateY(0); opacity: 0; } 12% { opacity: 1; }
                    100% { transform: translateY(-135vh); opacity: 0; } }

  /* the watermark hexagon, turning slowly */
  .watermark { display: flex; align-items: center; justify-content: flex-end; }
  .watermark svg { width: 34rem; height: 34rem; opacity: 0.09; margin-right: -9rem;
                   animation: turn 90s linear infinite; }
  @keyframes turn { to { transform: rotate(360deg); } }

  /* the mark itself */
  .brand .mark svg { overflow: visible; }
  .brand .lg-hex { stroke-dasharray: 180; stroke-dashoffset: 180;
                   animation: draw 1.7s cubic-bezier(0.4, 0, 0.2, 1) 0.15s forwards; }
  @keyframes draw { to { stroke-dashoffset: 0; } }
  .brand .lg-cloud { opacity: 0; transform-box: fill-box; transform-origin: center;
                     animation: cloud-in 0.9s ease-out 1.05s forwards, cloud-float 6s ease-in-out 2s infinite; }
  @keyframes cloud-in { from { opacity: 0; transform: translateY(2px) scale(0.94); }
                        to { opacity: 1; transform: none; } }
  @keyframes cloud-float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-1.2px); } }
  .brand .lg-dot { opacity: 0; transform-box: fill-box; transform-origin: center;
                   animation: dot-rise 3.2s ease-in-out infinite; animation-delay: calc(1.8s + var(--d)); }
  @keyframes dot-rise { 0% { opacity: 0; transform: translateY(5px); } 30% { opacity: 1; }
                        65% { opacity: 0; transform: translateY(-5px); } 100% { opacity: 0; } }

  /* the page-load sequence */
  .brand .mark, .brand .lab, .brand .pitch, .brand .pillars, .brand .foot {
    animation: rise-in 0.8s cubic-bezier(0.2, 0.7, 0.2, 1) both; }
  .brand .lab { animation-delay: 0.15s; }
  .brand .pitch { animation-delay: 0.3s; }
  .brand .pillars { animation-delay: 0.45s; }
  .brand .foot { animation-delay: 0.6s; }
  @keyframes rise-in { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }

  .brand .hero { max-width: 33rem; padding: 3rem 0; }
  .brand .lab { font-family: var(--cond); font-weight: 600; font-size: clamp(2.3rem, 3.5vw, 3.3rem);
                line-height: 1.04; letter-spacing: -0.015em; }
  .brand .pitch { color: #BFCAE0; font-size: 1.05rem; line-height: 1.6; margin: 1.1rem 0 2rem; max-width: 30rem; }
  .brand .pillars { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.6rem 1.5rem;
                    font-size: 0.86rem; max-width: 30rem; }
  .brand .pillars .pillar { color: #DCE4F2; }
  .brand .foot { color: #A9B8D2; font-size: 0.85rem; }

  .signin .title { font-family: var(--cond); font-weight: 600; font-size: 1.9rem; color: var(--ink); }
  .signin p { font-family: var(--body); color: var(--slate); line-height: 1.55; margin: 0.35rem 0 1.4rem; }
  .signin-foot { font-family: var(--body); color: var(--muted); font-size: 0.8rem; line-height: 1.5;
                 margin-top: 1rem; }
  .st-key-login_shell [data-testid="stFormSubmitButton"] button { min-height: 2.8rem; font-weight: 600;
    transition: transform 0.15s ease, box-shadow 0.15s ease; }
  .st-key-login_shell [data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-1px); box-shadow: 0 6px 18px rgba(31, 95, 191, 0.28); }

  @media (prefers-reduced-motion: reduce) {
    .brand *, .brand *::before, .brand *::after { animation: none !important; }
    .brand .lg-hex { stroke-dashoffset: 0; }
    .brand .lg-cloud, .brand .lg-dot { opacity: 1; }
  }
  @media (max-width: 640px) {
    .brand { min-height: 0; padding: 1.75rem 1.5rem 2.5rem; }
    .brand .hero { padding: 2rem 0 1.5rem; }
    .brand .pillars { grid-template-columns: 1fr; }
    .watermark svg { width: 22rem; height: 22rem; margin-right: -11rem; opacity: 0.07; }
    .st-key-login_shell [data-testid="stColumn"]:nth-child(2) { border-left: 0; min-height: 0;
      padding: 2rem 1.5rem 3rem; }
  }
</style>
""".replace("MESH_URL", _MESH)


def _brand_panel() -> str:
    pillars = "".join(
        f'<span class="pillar" style="--c:{c}"><span class="hx"></span>{name}</span>'
        for name, c in PILLARS_ON_DARK.items()
    )
    streams = "".join(
        f'<span style="left:{x}%;animation-delay:{d}s"></span>'
        for x, d in ((12, 0), (28, 2.5), (47, 1.2), (63, 4), (81, 3.1), (92, 5.4))
    )
    return (
        '<div class="brand">'
        '<div class="fx aurora"><i></i><i></i><i></i></div>'
        '<div class="fx mesh"></div>'
        f'<div class="fx uplink">{streams}</div>'
        f'<div class="fx watermark">{logo_svg(544, "mark")}</div>'
        f'<div class="mark">{logo_svg(44, "login")}</div>'
        f'<div class="hero"><div class="lab">{LAB_NAME}</div>'
        '<p class="pitch">The catalogue of AI applications delivered by CIS CLD across cloud, data, migration '
        'and security, each mapped to its Infosys Hexagon pillar and business case.</p>'
        f'<div class="pillars">{pillars}</div></div>'
        f'<div class="foot">{COLLAB}</div></div>'
    )


def _attempt(users: dict[str, str], username: str, password: str) -> None:
    now = time.time()
    locked_until = st.session_state.get("auth_locked_until", 0.0)
    if now < locked_until:
        st.error(f"Too many attempts. Try again in {int(locked_until - now) + 1} seconds.")
        return
    stored = users.get(username)
    if verify_password(password, stored or _DUMMY_HASH) and stored is not None:
        st.session_state.auth_user = username
        st.session_state.auth_fails = 0
        st.rerun()
    fails = st.session_state.get("auth_fails", 0) + 1
    if fails >= MAX_ATTEMPTS:
        st.session_state.auth_locked_until, fails = now + LOCKOUT_SECONDS, 0
    st.session_state.auth_fails = fails
    st.error("Incorrect username or password.")


def require_login() -> bool:
    """True once the viewer has signed in; otherwise draws the login page and returns False."""
    if st.session_state.get("auth_user"):
        return True
    st.markdown(_LOGIN_CSS, unsafe_allow_html=True)
    users = _users()
    with st.container(key="login_shell"):
        brand, form = st.columns([1.45, 1])  # stretch, so the white sign-in panel runs full height
        brand.markdown(_brand_panel(), unsafe_allow_html=True)
        with form:
            st.markdown('<div class="signin"><div class="title">Sign in</div>'
                        "<p>Use the username and password from your CIS CLD administrator.</p></div>",
                        unsafe_allow_html=True)
            if not users:
                st.warning("Sign-in isn't set up yet. Add an [auth.users] section to this app's secrets.")
            with st.form("login", border=False):
                username = st.text_input("Username", autocomplete="username")
                password = st.text_input("Password", type="password", autocomplete="current-password")
                submitted = st.form_submit_button("Sign in", type="primary", width="stretch", disabled=not users)
            if submitted:
                _attempt(users, username.strip(), password)
            st.markdown('<div class="signin-foot">Access is limited to CIS CLD members.</div>',
                        unsafe_allow_html=True)
    return False


def current_user() -> str:
    return st.session_state.get("auth_user", "")


def sign_out() -> None:
    st.session_state.pop("auth_user", None)

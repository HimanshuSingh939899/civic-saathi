"""Visual styling for Civic Saathi."""

import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --navy: #102a43;
            --blue: #1f5f9c;
            --blue-light: #e9f3fb;
            --teal: #12827a;
            --saffron: #f29a3f;
            --green: #2d8a62;
            --page: #e9f1f4;
            --card: #f9fcfd;
            --text: #17324d;
            --muted: #6c7f8e;
            --border: #cddde5;
            --shadow: 0 12px 32px rgba(16, 42, 67, 0.09);
        }

        .stApp {
            background:
                radial-gradient(circle at 95% 0%, rgba(242, 154, 63, 0.16), transparent 23%),
                radial-gradient(circle at 5% 45%, rgba(18, 130, 122, 0.08), transparent 24%),
                linear-gradient(180deg, #f3f8f9 0%, var(--page) 100%);
            color: var(--text);
        }

        .main .block-container {
            max-width: 1180px;
            padding-top: 1.5rem;
            padding-bottom: 3rem;
        }

        [data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, #0b2037 0%, #102f4d 52%, #123f52 100%);
            border-right: 1px solid rgba(255,255,255,.12);
        }

        [data-testid="stSidebar"] .block-container {
            padding: 1.25rem 1rem 2rem;
        }

        [data-testid="stSidebar"] * {
            color: #f4f8fb;
        }

        .sidebar-brand {
            display: flex;
            align-items: center;
            gap: .75rem;
            padding: .35rem .2rem;
        }

        .sidebar-logo {
            width: 44px;
            height: 44px;
            border-radius: 13px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(145deg, #f5ad52, #df6736);
            color: white;
            font-weight: 900;
            box-shadow: 0 8px 22px rgba(0,0,0,.2);
        }

        .sidebar-title {
            font-size: 1.08rem;
            font-weight: 850;
        }

        .sidebar-subtitle {
            color: #b9d0df;
            font-size: .68rem;
            margin-top: .15rem;
        }

        .sidebar-rule {
            height: 1px;
            background: rgba(255,255,255,.14);
            margin: 1.2rem 0;
        }

        .sidebar-section-title {
            color: #91b7c9;
            font-size: .68rem;
            font-weight: 850;
            letter-spacing: .11em;
            margin: .8rem .25rem .55rem;
        }

        [data-testid="stSidebar"] div.stButton > button {
            background: rgba(255,255,255,.045);
            border: 1px solid rgba(255,255,255,.07);
            color: #f5f9fb;
            text-align: left;
            min-height: 2.55rem;
            border-radius: 10px;
            margin-bottom: .18rem;
        }

        [data-testid="stSidebar"] div.stButton > button:hover {
            background: rgba(255,255,255,.12);
            border-color: rgba(242,154,63,.42);
            transform: translateX(2px);
        }

        .sidebar-status {
            display: flex;
            gap: .65rem;
            margin-top: 1.5rem;
            padding: .8rem;
            border: 1px solid rgba(255,255,255,.12);
            border-radius: 12px;
            background: rgba(255,255,255,.07);
        }

        .status-dot {
            width: 10px;
            height: 10px;
            margin-top: .25rem;
            border-radius: 50%;
            background: #66d69b;
            box-shadow: 0 0 0 5px rgba(102,214,155,.12);
            flex: 0 0 auto;
        }

        .sidebar-status strong,
        .sidebar-status span {
            display: block;
        }

        .sidebar-status strong { font-size: .72rem; }
        .sidebar-status span {
            color: #b9d0df;
            font-size: .63rem;
            line-height: 1.45;
            margin-top: .2rem;
        }

        .civic-hero {
            position: relative;
            overflow: hidden;
            min-height: 300px;
            padding: 2.35rem 2.5rem;
            border-radius: 24px;
            color: white;
            background:
                linear-gradient(115deg, rgba(9,37,64,.99), rgba(23,91,135,.97) 60%, rgba(18,130,122,.93)),
                repeating-linear-gradient(135deg, transparent 0, transparent 22px, rgba(255,255,255,.035) 23px, transparent 24px);
            box-shadow: 0 22px 55px rgba(9,37,64,.2);
        }

        .hero-content {
            position: relative;
            z-index: 2;
            max-width: 710px;
        }

        .civic-badge {
            display: inline-flex;
            align-items: center;
            gap: .5rem;
            padding: .46rem .75rem;
            border: 1px solid rgba(255,255,255,.22);
            border-radius: 999px;
            background: rgba(255,255,255,.1);
            color: #d9efed;
            font-size: .68rem;
            font-weight: 850;
            letter-spacing: .09em;
        }

        .civic-badge-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #ffc76b;
            box-shadow: 0 0 0 4px rgba(255,199,107,.13);
        }

        .civic-hero h1 {
            color: white;
            font-size: clamp(2.5rem, 5vw, 4.2rem);
            margin: 1.25rem 0 .45rem;
            line-height: 1;
            font-weight: 900;
        }

        .civic-hero-tagline {
            color: white;
            font-size: 1.25rem;
            font-weight: 700;
            margin: 0 0 .55rem;
        }

        .civic-hero-copy {
            color: #d5e6ef;
            max-width: 650px;
            line-height: 1.65;
            margin: 0;
        }

        .hero-pills {
            display: flex;
            flex-wrap: wrap;
            gap: .55rem;
            margin-top: 1.45rem;
        }

        .hero-pills span {
            padding: .4rem .65rem;
            border-radius: 999px;
            background: rgba(255,255,255,.1);
            border: 1px solid rgba(255,255,255,.14);
            color: #e4f1f3;
            font-size: .72rem;
            font-weight: 700;
        }

        .hero-emblem {
            position: absolute;
            right: 7%;
            bottom: -40px;
            width: 190px;
            height: 190px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(255,255,255,.2);
            border-radius: 30px;
            background: rgba(255,255,255,.08);
            color: rgba(255,255,255,.65);
            font-size: 4.5rem;
            font-weight: 900;
            transform: rotate(12deg);
        }

        .hero-orb {
            position: absolute;
            border-radius: 50%;
        }

        .hero-orb-one {
            width: 170px;
            height: 170px;
            right: 0;
            top: -80px;
            background: rgba(242,154,63,.3);
        }

        .hero-orb-two {
            width: 230px;
            height: 230px;
            right: 28%;
            bottom: -120px;
            background: rgba(82,210,185,.13);
        }

        .section-heading {
            display: flex;
            align-items: end;
            justify-content: space-between;
            gap: 1rem;
            margin: 1.8rem 0 .8rem;
        }

        .section-heading h2 {
            margin: .15rem 0 0;
            color: var(--text);
            font-size: 1.45rem;
        }

        .section-kicker {
            color: var(--teal);
            font-size: .66rem;
            font-weight: 900;
            letter-spacing: .1em;
        }

        .online-pill {
            border: 1px solid #b9dfd8;
            border-radius: 999px;
            background: #edf9f6;
            color: #23766d;
            padding: .35rem .65rem;
            font-size: .7rem;
            font-weight: 750;
        }

        .online-pill span {
            display: inline-block;
            width: 7px;
            height: 7px;
            margin-right: .35rem;
            border-radius: 50%;
            background: #35a978;
        }

        div[data-testid="stChatMessage"] {
            background: rgba(249,252,253,.82);
            border: 1px solid var(--border);
            border-radius: 15px;
            box-shadow: 0 5px 18px rgba(16,42,67,.045);
            margin: .6rem 0;
            padding: .9rem 1rem;
        }

        div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
            color: var(--text);
            line-height: 1.65;
        }

        div[data-testid="stChatMessage"] [data-testid="chatAvatarIcon-user"] {
            background: var(--navy);
        }

        div[data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"] {
            background: var(--teal);
        }

        div.stButton > button {
            border-radius: 10px;
            border: 1px solid var(--border);
            min-height: 2.65rem;
            font-weight: 750;
            transition: .2s ease;
        }

        div.stButton > button:hover {
            border-color: #82adbf;
            box-shadow: 0 8px 18px rgba(16,42,67,.1);
            transform: translateY(-1px);
        }

        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, var(--navy), var(--blue));
            border-color: var(--navy);
            color: white;
        }

        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            background: rgba(255,255,255,.88);
            border: 1px solid var(--border);
            border-radius: 10px;
        }

        div[data-testid="stTextInput"] input:focus,
        div[data-testid="stTextArea"] textarea:focus {
            border-color: #4c9cb7;
            box-shadow: 0 0 0 2px rgba(76,156,183,.14);
        }

        div[data-testid="stExpander"] {
            background: rgba(249,252,253,.7);
            border: 1px solid var(--border);
            border-radius: 12px;
        }

        .source-card {
            display: flex;
            gap: .75rem;
            align-items: center;
            padding: .7rem;
            margin-top: .55rem;
            border: 1px solid var(--border);
            border-radius: 11px;
            background: #f6fafb;
        }

        .source-icon {
            width: 35px;
            height: 35px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 9px;
            background: #e0f1f4;
            color: var(--teal);
            font-size: .58rem;
            font-weight: 900;
        }

        .source-kicker {
            color: var(--teal);
            font-size: .62rem;
            font-weight: 850;
            text-transform: uppercase;
        }

        .source-card strong {
            display: block;
            color: var(--text);
            font-size: .86rem;
            overflow-wrap: anywhere;
        }

        .source-card span {
            color: var(--muted);
            font-size: .72rem;
        }

        @media (max-width: 700px) {
            .main .block-container { padding: 1rem .75rem 2rem; }
            .civic-hero { padding: 1.55rem 1.2rem 1.8rem; border-radius: 17px; min-height: 0; }
            .civic-hero h1 { font-size: 2.7rem; }
            .hero-emblem { width: 110px; height: 110px; font-size: 2.5rem; right: -20px; bottom: -30px; }
            .section-heading { align-items: flex-start; flex-direction: column; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
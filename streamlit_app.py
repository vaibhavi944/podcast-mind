import streamlit as st
import pandas as pd
import sys
import os

# Ensure backend is in path
sys.path.append(os.getcwd())

from backend.utils.loader import artifacts
from backend.engines.hybrid_engine import HybridEngine
from backend.config import settings

# --- Page Configuration ---
st.set_page_config(
    page_title="PodcastMind | Discovery Engine",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for a more "React-like" feel
st.markdown("""
<style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        border-radius: 20px;
        font-weight: 600;
    }
    /* Targeted styling for the podcast cards */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
        height: 100%;
    }
    .podcast-title {
        height: 60px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        font-size: 1.15rem;
        font-weight: 700;
        line-height: 1.3;
        margin-bottom: 4px;
    }
    .podcast-author {
        height: 24px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        color: #64748b;
        font-size: 0.9rem;
    }
    .podcast-categories {
        height: 44px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        font-size: 0.85rem;
        margin: 12px 0;
    }
    .explanation-box {
        height: 70px;
        overflow: hidden;
        background-color: #eff6ff;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 0.85rem;
        color: #1e40af;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

# --- Constants ---
CATEGORIES = [
    "AI", "Technology", "History", "Psychology", "Comedy", 
    "Business", "Science", "Philosophy", "Health", "Productivity",
    "True Crime", "Arts", "Fiction", "Society & Culture"
]

# --- State Management ---
if "interests" not in st.session_state:
    st.session_state.interests = []

if "selected_podcast" not in st.session_state:
    st.session_state.selected_podcast = None

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

# --- Helper Functions ---
@st.cache_resource
def get_engine():
    """Initializes the recommendation engine and loads AI artifacts."""
    with st.spinner("Initializing Recommendation Engine..."):
        artifacts.load_all()
        return HybridEngine()

def update_interests(podcast_categories):
    """Dynamically evolves the taste profile based on interaction."""
    if not podcast_categories: return
    cats = [c.strip() for c in podcast_categories.split(',')]
    new_interests = list(st.session_state.interests)
    changed = False
    for cat in cats:
        if cat not in new_interests and len(new_interests) < 10:
            new_interests.append(cat)
            changed = True
    if changed:
        st.session_state.interests = new_interests

def podcast_card(podcast, key_prefix=""):
    """Renders a single podcast result with fixed-height elements for alignment."""
    with st.container(border=True):
        st.markdown(f'<div class="podcast-title">{podcast.title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="podcast-author">By {podcast.author}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="podcast-categories"><b>Categories:</b> {podcast.categories}</div>', unsafe_allow_html=True)
        
        # Fixed-height Explanation
        exp = podcast.explanation if hasattr(podcast, 'explanation') and podcast.explanation else "Matched based on your specific interests and semantic relevance."
        st.markdown(f'<div class="explanation-box">✨ {exp}</div>', unsafe_allow_html=True)
            
        col1, col2 = st.columns([1, 1.5])
        with col1:
            score_color = "green" if podcast.blended_score > 0.7 else "orange" if podcast.blended_score > 0.4 else "gray"
            st.markdown(f"**Match:** :{score_color}[{int(podcast.blended_score * 100)}%]")
        with col2:
            if st.button("Explore Similar", key=f"{key_prefix}_{podcast.podcast_id}", use_container_width=True):
                st.session_state.selected_podcast = podcast
                update_interests(podcast.categories)
                st.rerun()

# --- App Logic ---
engine = get_engine()

# --- Sidebar ---
with st.sidebar:
    st.header("🎙️ PodcastMind")
    st.markdown("Retrieval-first recommendation engine.")
    st.markdown("---")
    
    st.subheader("Your Taste Profile")
    st.caption("Personalized recommendations based on these topics.")
    
    if not st.session_state.interests:
        st.warning("Pick some topics to get started!")
    
    # Category selection grid
    cols = st.columns(2)
    for i, cat in enumerate(CATEGORIES):
        is_selected = cat in st.session_state.interests
        if cols[i % 2].button(
            f"{'✅ ' if is_selected else ''}{cat}", 
            key=f"sidebar_cat_{cat}",
            use_container_width=True,
            type="secondary" if not is_selected else "primary"
        ):
            if is_selected:
                st.session_state.interests.remove(cat)
            else:
                st.session_state.interests.append(cat)
            st.rerun()
            
    st.markdown("---")
    if st.session_state.interests:
        if st.button("Reset Taste Profile", use_container_width=True):
            st.session_state.interests = []
            st.rerun()
    
    st.markdown("---")
    st.caption("v1.0.0 • No data leaves your browser profile.")

# --- Main Layout ---
if st.session_state.selected_podcast:
    # Detail View / Similar Podcasts
    pod = st.session_state.selected_podcast
    if st.button("← Back to Feed"):
        st.session_state.selected_podcast = None
        st.rerun()
        
    st.title(pod.title)
    st.subheader(f"Shows similar to {pod.title}")
    
    with st.spinner("Finding behaviorally and semantically similar shows..."):
        results = engine.recommend(
            podcast_id=pod.podcast_id,
            limit=9,
            s_weight=0.3,
            c_weight=0.7,
            preferred_categories=st.session_state.interests
        )
    
    if results:
        cols = st.columns(3)
        for i, res in enumerate(results):
            with cols[i % 3]:
                podcast_card(res, key_prefix="similar")
    else:
        st.write("No similar podcasts found.")

else:
    # Standard Discovery / Search View
    st.title("Discover Your Next Mind-Bending Show")
    
    # Search Input
    query = st.text_input(
        "Search by topic, interest, or vibe...", 
        placeholder="e.g. 'History of Ancient Rome' or 'Deep dives into AI safety'",
        help="Our semantic engine understands intent, not just keywords."
    )
    
    if query:
        st.header(f"Results for: {query}")
        with st.spinner("Searching semantic space..."):
            results = engine.recommend(
                query=query,
                limit=12,
                s_weight=1.0,
                c_weight=0.0,
                preferred_categories=st.session_state.interests
            )
    else:
        if st.session_state.interests:
            st.header("Tailored for Your Taste")
            discovery_query = " ".join(st.session_state.interests)
        else:
            st.header("Trending Today")
            discovery_query = "top rated podcasts across tech science history and comedy"
            
        with st.spinner("Brewing fresh recommendations..."):
            results = engine.recommend(
                query=discovery_query,
                limit=12,
                preferred_categories=st.session_state.interests
            )
            
    if results:
        cols = st.columns(3)
        for i, res in enumerate(results):
            with cols[i % 3]:
                podcast_card(res, key_prefix="feed")
    else:
        st.info("No podcasts found matching your criteria. Try adjusting your taste profile!")

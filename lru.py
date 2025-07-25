import streamlit as st
from collections import OrderedDict

# ---------------------- LRU Cache Class ----------------------
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def clear(self):
        self.cache.clear()

    def display(self):
        return list(self.cache.items())[::-1]  # MRU to LRU

# ---------------------- Page Config ----------------------
st.set_page_config(page_title="💾 Cool LRU Cache Simulator", layout="centered")

st.markdown("""
    <style>
        .cache-box {
            padding: 12px;
            border-radius: 12px;
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            color: white;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }
        .stButton>button {
            font-size: 16px;
            padding: 0.6em 1.2em;
            border-radius: 8px;
        }
        .highlight {
            background-color: #ffe082;
            color: black;
            padding: 8px;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 LRU Cache Visual Simulator")

# ---------------------- Info Expanders ----------------------
with st.expander("ℹ️ What is LRU Cache?"):
    st.markdown("""
    **LRU (Least Recently Used)** Cache keeps a limited number of key-value pairs.  
    When full, it removes the *least recently used* item to make space.
    """)

with st.expander("⚙️ How It Works"):
    st.markdown("""
    - Use **Put** to add or update key-value pairs.
    - Use **Get** to retrieve values (moves them to most-recent).
    - If full, the **oldest used** item gets removed.
    """)

# ---------------------- Session State ----------------------
if "cache_initialized" not in st.session_state:
    st.session_state.cache_initialized = False
if "highlight" not in st.session_state:
    st.session_state.highlight = None

# ---------------------- Init Cache ----------------------
if not st.session_state.cache_initialized:
    with st.form("init_cache"):
        capacity = st.number_input("🧠 Enter Cache Capacity", min_value=1, step=1)
        if st.form_submit_button("Initialize"):
            st.session_state.cache = LRUCache(capacity)
            st.session_state.capacity = capacity
            st.session_state.cache_initialized = True
            st.success("✅ Cache Initialized")

# ---------------------- Main UI ----------------------
if st.session_state.cache_initialized:
    st.success(f"🧰 Cache Ready (Capacity = {st.session_state.capacity})")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("➕ Insert / Update")
        with st.form("put_form"):
            put_key = st.number_input("Key", step=1, format="%d")
            put_value = st.number_input("Value", step=1, format="%d")
            if st.form_submit_button("Put"):
                st.session_state.cache.put(put_key, put_value)
                st.session_state.highlight = put_key
                st.success(f"🔐 Stored ({put_key}, {put_value})")

    with col2:
        st.subheader("🔍 Retrieve")
        with st.form("get_form"):
            get_key = st.number_input("Get Key", step=1, format="%d", key="get_key_input")
            if st.form_submit_button("Get"):
                value = st.session_state.cache.get(get_key)
                if value == -1:
                    st.warning("❌ Key not found.")
                else:
                    st.session_state.highlight = get_key
                    st.info(f"📥 Value = {value}")

    # Visual cache usage
    usage = len(st.session_state.cache.display())
    capacity = st.session_state.capacity
    st.subheader("📊 Cache Usage")
    st.progress(usage / capacity)

    st.subheader("📦 Cache Content (MRU ➡️ LRU)")
    items = st.session_state.cache.display()

    if items:
        cols = st.columns(len(items))
        for idx, (k, v) in enumerate(items):
            style = "highlight" if k == st.session_state.highlight else "cache-box"
            with cols[idx]:
                st.markdown(f"<div class='{style}'><div>{k}</div><div>{v}</div></div>", unsafe_allow_html=True)
        st.markdown("<center>⬅️ Most Recently Used | Least Recently Used ➡️</center>", unsafe_allow_html=True)
    else:
        st.info("📭 Cache is empty.")

    # Buttons
    col3, col4 = st.columns(2)
    with col3:
        if st.button("🔁 Reset Cache"):
            for key in ["cache_initialized", "cache", "capacity", "highlight"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    with col4:
        if st.button("🧹 Clear All Data"):
            st.session_state.cache.clear()
            st.session_state.highlight = None
            st.success("🗑️ Cache Cleared")


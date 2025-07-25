import streamlit as st
from collections import OrderedDict

# ---------- LRU Cache Logic ----------
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

# ---------- Page Configuration ----------
st.set_page_config(page_title="⚡ LRU Cache Visualizer", layout="wide")
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .cache-box {
            padding: 15px;
            border-radius: 12px;
            background: linear-gradient(135deg, #7b2ff7, #f107a3);
            color: white;
            text-align: center;
            font-weight: bold;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        }
        .bar-outer {
            background-color: #ddd;
            border-radius: 10px;
            overflow: hidden;
            height: 20px;
            width: 100%;
        }
        .bar-inner {
            background: linear-gradient(to right, #00c6ff, #0072ff);
            height: 100%;
            transition: width 0.3s ease-in-out;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Header & Description ----------
st.title("📦 LRU Cache Visual Simulator")

with st.expander("ℹ️ About LRU Cache"):
    st.markdown("""
    - **LRU (Least Recently Used) Cache** evicts the least recently used items first when capacity is exceeded.
    - Commonly used in memory management, web caching, and databases.
    """)

# ---------- Initialization ----------
if "cache_initialized" not in st.session_state:
    st.session_state.cache_initialized = False

if not st.session_state.cache_initialized:
    with st.form("init_form"):
        capacity = st.number_input("🔧 Set Cache Capacity", min_value=1, step=1, format="%d")
        if st.form_submit_button("Initialize Cache"):
            st.session_state.cache = LRUCache(capacity)
            st.session_state.capacity = capacity
            st.session_state.cache_initialized = True

# ---------- Main App Logic ----------
if st.session_state.cache_initialized:
    st.success(f"✅ Cache initialized with capacity = {st.session_state.capacity}")

    col1, col2 = st.columns(2)

    # PUT operation
    with col1:
        st.subheader("➕ Insert or Update")
        with st.form("put_form"):
            put_key = st.number_input("Key", step=1, format="%d")
            put_value = st.number_input("Value", step=1, format="%d")
            if st.form_submit_button("Put"):
                st.session_state.cache.put(put_key, put_value)
                st.success(f"Put ({put_key}, {put_value})")

    # GET operation
    with col2:
        st.subheader("🔍 Retrieve")
        with st.form("get_form"):
            get_key = st.number_input("Get Key", step=1, format="%d", key="get_key")
            if st.form_submit_button("Get"):
                value = st.session_state.cache.get(get_key)
                if value == -1:
                    st.warning("❌ Key not found.")
                else:
                    st.success(f"Value = {value}")

    # ---------- Cache Display ----------
    st.divider()
    st.subheader("📊 Cache State (MRU ➝ LRU)")

    items = st.session_state.cache.display()
    if items:
        usage = len(items) / st.session_state.capacity * 100
        st.markdown(f"**🧠 Usage: {len(items)} / {st.session_state.capacity}**")
        st.markdown(f"""
            <div class='bar-outer'><div class='bar-inner' style='width:{usage}%;'></div></div>
        """, unsafe_allow_html=True)
        st.write("")  # spacing

        cols = st.columns(len(items))
        for idx, (k, v) in enumerate(items):
            with cols[idx]:
                st.markdown(f"<div class='cache-box'>{k}<br><small>{v}</small></div>", unsafe_allow_html=True)
        st.markdown("<center>⬅️ MRU | LRU ➡️</center>", unsafe_allow_html=True)
    else:
        st.info("🌀 Cache is currently empty.")

    # ---------- Buttons ----------
    st.divider()
    col3, col4 = st.columns([1, 1])
    with col3:
        if st.button("🧹 Clear Data"):
            st.session_state.cache.clear()
            st.success("Cache cleared.")
    with col4:
        if st.button("🔁 Reset Cache"):
            for key in ["cache_initialized", "cache", "capacity"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime
import hashlib

# =====================================================
# LEAFCARE AI - PLANT LEAF DISEASE CLASSIFICATION
# =====================================================

st.set_page_config(
    page_title="LeafCare AI | Plant Health",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- SESSION STATE ----------------

if "history" not in st.session_state:
    st.session_state.history = []

if "total_uploads" not in st.session_state:
    st.session_state.total_uploads = 0

if "saved_images" not in st.session_state:
    st.session_state.saved_images = set()

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "MobileNetV2"

# ---------------- COLORS & STYLING ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

/* Global Font & Reset */
html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif;
}

/* Base Light Theme Background & Text */
.stApp, 
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background-color: #f2f7f1 !important;
    color: #0f2417 !important;
}

/* Ensure all regular body typography is crisp and dark */
p, span, label, li, a, h1, h2, h3, h4, h5, h6 {
    color: #0f2417;
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] li,
.stApp label,
.stApp [data-testid="stWidgetLabel"] label,
.stApp [data-testid="stWidgetLabel"] p {
    color: #0f2417 !important;
    font-weight: 500;
}

/* Captions & Subtitles (Dark enough to meet contrast standards) */
.stCaption, 
[data-testid="stCaptionContainer"] p,
.subtext {
    color: #31533c !important;
    font-weight: 500;
}

/* Section Headings */
.section-title {
    color: #0d381e !important;
    font-size: 27px;
    font-weight: 800;
    margin-bottom: 0.5rem;
}

/* ---------------- SIDEBAR (Dark Forest Theme) ---------------- */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #0e2f1e 0%, #16462c 100%) !important;
}

/* Target all text inside sidebar to remain stark white */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}

[data-testid="stSidebar"] .stCaption p {
    color: #c4e4ce !important;
}

/* Sidebar Inputs & Dropdowns */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #0b2216 !important;
    color: #ffffff !important;
    border: 1px solid #2e6945 !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #ffffff !important;
}

/* ---------------- HERO BANNER ---------------- */
.hero {
    background: linear-gradient(120deg, #0d3220, #1b5b37);
    padding: 36px;
    border-radius: 20px;
    margin-bottom: 25px;
    box-shadow: 0 10px 28px rgba(10, 40, 20, 0.15);
    border: 1px solid #236940;
}

.hero h1, .hero h2, .hero h3 {
    color: #ffffff !important;
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero p {
    color: #e6f7ec !important;
    font-size: 16px;
    line-height: 1.5;
}

/* ---------------- CARDS ---------------- */
.card, .small-card {
    background-color: #ffffff !important;
    border: 1px solid #cfe0cf !important;
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 4px 18px rgba(15, 45, 25, 0.05);
    margin-bottom: 1rem;
}

.card h1, .card h2, .card h3,
.small-card h1, .small-card h2, .small-card h3 {
    color: #0d381e !important;
    font-weight: 700;
}

.card p, .card span, .card li,
.small-card p, .small-card span, .small-card li {
    color: #1a3826 !important;
}

/* ---------------- BUTTONS ---------------- */
.stButton button {
    background-color: #175e35 !important;
    color: #ffffff !important;
    border: 1px solid #175e35 !important;
    border-radius: 10px;
    font-weight: 700;
    transition: all 0.2s ease-in-out;
}

.stButton button p,
.stButton button span {
    color: #ffffff !important;
}

.stButton button:hover {
    background-color: #0e3f22 !important;
    border-color: #0e3f22 !important;
    color: #ffffff !important;
}

/* ---------------- FORM INPUTS & TEXTAREAS ---------------- */
.stTextInput input, 
.stNumberInput input, 
.stTextArea textarea {
    background-color: #ffffff !important;
    color: #0d2717 !important;
    border: 1px solid #8cae93 !important;
    border-radius: 8px !important;
}

.stTextInput input:focus, 
.stNumberInput input:focus, 
.stTextArea textarea:focus {
    border-color: #186036 !important;
    box-shadow: 0 0 0 1px #186036 !important;
    color: #0d2717 !important;
}

/* Placeholder styling */
input::placeholder, textarea::placeholder {
    color: #617c69 !important;
}

/* ---------------- SELECT & DROPDOWN MENUS ---------------- */
/* Selected box container */
[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 1px solid #8cae93 !important;
    border-radius: 8px !important;
}

[data-baseweb="select"] span,
[data-baseweb="select"] div {
    color: #0d2717 !important;
}

/* Popover dropdown list (floating menu) */
[data-baseweb="popover"],
[data-baseweb="menu"],
ul[role="listbox"] {
    background-color: #ffffff !important;
    border: 1px solid #cfe0cf !important;
}

li[role="option"] {
    background-color: #ffffff !important;
    color: #0d2717 !important;
}

li[role="option"]:hover, 
li[aria-selected="true"] {
    background-color: #e4f2e6 !important;
    color: #0a331a !important;
}

/* ---------------- TABS ---------------- */
.stTabs [data-baseweb="tab-list"] {
    border-bottom: 2px solid #d0e0d2;
}

.stTabs [data-baseweb="tab"] {
    color: #3b5744 !important;
    font-weight: 700;
}

.stTabs [data-baseweb="tab"] p {
    color: inherit !important;
}

.stTabs [aria-selected="true"] {
    color: #105930 !important;
    border-bottom-color: #105930 !important;
}

/* ---------------- METRIC WIDGETS ---------------- */
div[data-testid="stMetric"] {
    background-color: #ffffff !important;
    padding: 16px;
    border-radius: 14px;
    border: 1px solid #cfe0cf;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
}

div[data-testid="stMetric"] [data-testid="stMetricLabel"] p,
div[data-testid="stMetric"] [data-testid="stMetricLabel"] span {
    color: #33553f !important;
    font-weight: 600 !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] div {
    color: #0c331b !important;
    font-weight: 800 !important;
}

/* ---------------- FILE UPLOADER ---------------- */
div[data-testid="stFileUploader"] {
    background-color: #ffffff !important;
    border: 1.5px dashed #64966e !important;
    border-radius: 14px;
    padding: 16px;
}

div[data-testid="stFileUploader"] * {
    color: #0f2417 !important;
}

div[data-testid="stFileUploader"] button {
    background-color: #e8f4eb !important;
    color: #0f4423 !important;
    border: 1px solid #7cb087 !important;
}

/* ---------------- EXPANDERS & ALERTS ---------------- */
[data-testid="stExpander"] {
    background-color: #ffffff !important;
    border: 1px solid #cfe0cf !important;
    border-radius: 12px !important;
}

[data-testid="stExpander"] summary span {
    color: #0f2417 !important;
    font-weight: 600;
}

.stAlert {
    border-radius: 10px;
}
.stAlert p {
    color: #0a2916 !important;
}

hr {
    border-color: #cbdccf !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- PROJECT INFORMATION ----------------

disease_classes = [
    "Tomato Healthy",
    "Tomato Bacterial Spot",
    "Tomato Early Blight",
    "Tomato Late Blight",
    "Tomato Leaf Mold"
]

# ---------------- SIDEBAR ----------------

st.sidebar.markdown("# 🌿 LeafCare AI")
st.sidebar.markdown("### PLANT HEALTH INTELLIGENCE")
st.sidebar.caption("An AI-powered plant leaf classification project")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "🏡 Dashboard",
        "📸 Disease Scanner",
        "🧠 AI Models",
        "📊 Analytics",
        "📁 History",
        "📖 About Project"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown("### SYSTEM STATUS")
st.sidebar.success("Interface is running")
st.sidebar.warning("AI model connection pending")

st.sidebar.markdown("---")
st.sidebar.caption("Plant Leaf Disease Classification")
st.sidebar.caption("Academic Project | 2026")

# =====================================================
# DASHBOARD
# =====================================================

if page == "🏡 Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>Welcome to LeafCare AI 🌿</h1>
        <p>Your smart plant health exploration platform.</p>
        <p>Discover how deep learning can help classify plant leaf diseases.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-title">Your Dashboard</p>',
                unsafe_allow_html=True)

    st.markdown(
        '<p class="subtext">An overview of your plant image classification workspace.</p>',
        unsafe_allow_html=True
    )

    # Actual session information
    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric("Images uploaded", len(st.session_state.history))

    with m2:
        st.metric("Models explored", "2")

    with m3:
        st.metric("Target categories", "5")

    st.markdown("---")

    st.markdown('<p class="section-title">Explore LeafCare AI</p>',
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="card">
            <h3>📸 Disease Scanner</h3>
            <p>Upload a leaf image or capture one using your camera.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
            <h3>🧠 AI Technology</h3>
            <p>Explore Custom CNN and MobileNetV2 architectures.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="card">
            <h3>📊 Project Analytics</h3>
            <p>View your actual upload activity and project information.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<p class="section-title">How does it work?</p>',
                unsafe_allow_html=True)

    steps = st.columns(4)

    with steps[0]:
        st.info("**01 📷 Upload**\n\nChoose a plant leaf image.")

    with steps[1]:
        st.info("**02 ⚙️ Process**\n\nPrepare the image for analysis.")

    with steps[2]:
        st.info("**03 🧠 Classify**\n\nA trained model analyses the image.")

    with steps[3]:
        st.info("**04 🌱 Result**\n\nDisplay the predicted category.")

    st.markdown("---")

    st.markdown("### 🍅 Categories explored in this project")

    category_columns = st.columns(5)

    category_icons = ["🌿", "🟤", "🍂", "🍃", "🌱"]

    for i, category in enumerate(disease_classes):
        with category_columns[i]:
            st.markdown(
                f"""
                <div class="small-card">
                    <h2>{category_icons[i]}</h2>
                    <p><b>{category}</b></p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.caption(
        "These are the five target categories described in the project demo presentation. "
        "Actual prediction labels must be verified against the trained model."
    )

# =====================================================
# DISEASE SCANNER
# =====================================================

elif page == "📸 Disease Scanner":

    st.markdown("""
    <div class="hero">
        <h1>Plant Health Scanner 📸</h1>
        <p>Capture or upload a leaf image to begin your inspection.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Choose your image source")

    upload_tab, camera_tab = st.tabs([
        "📁 Upload from device",
        "📸 Open camera"
    ])

    uploaded_image = None

    with upload_tab:

        st.markdown("#### Upload an existing leaf photo")

        file_image = st.file_uploader(
            "Choose an image",
            type=["jpg", "jpeg", "png"],
            key="upload_leaf"
        )

        if file_image is not None:
            uploaded_image = file_image

    with camera_tab:

        st.markdown("#### Capture a fresh leaf photo")

        st.info(
            "Allow camera permission in your browser. "
            "Your laptop webcam should open below."
        )

        camera_image = st.camera_input(
            "Take a picture of a plant leaf",
            key="camera_leaf"
        )

        if camera_image is not None:
            uploaded_image = camera_image

    st.markdown("---")

    if uploaded_image is not None:

        try:

            image = Image.open(uploaded_image).convert("RGB")

            image_hash = hashlib.md5(
                uploaded_image.getvalue()
            ).hexdigest()

            st.markdown('<p class="section-title">Image Preview</p>',
                        unsafe_allow_html=True)

            left, right = st.columns([1.3, 1])

            with left:

                st.image(
                    image,
                    caption="Your selected plant leaf image",
                    use_container_width=True
                )

            with right:

                st.markdown("### 📋 Image Details")

                st.metric("Width", f"{image.width} pixels")
                st.metric("Height", f"{image.height} pixels")

                st.write("**Filename:**", uploaded_image.name)
                st.write("**Format:**", uploaded_image.type)
                st.write(
                    "**Size:**",
                    f"{len(uploaded_image.getvalue()) / 1024:.1f} KB"
                )

                st.markdown("---")

                st.markdown("### 🧠 Select AI Model")

                selected_model = st.selectbox(
                    "Choose model architecture",
                    ["MobileNetV2", "Custom CNN"]
                )

                st.session_state.selected_model = selected_model

                if st.button(
                    "➕ Save to My History",
                    use_container_width=True
                ):

                    if image_hash not in st.session_state.saved_images:

                        st.session_state.history.append({
                            "Image": uploaded_image.name,
                            "Model": selected_model,
                            "Date": datetime.now().strftime("%d %b %Y"),
                            "Time": datetime.now().strftime("%H:%M:%S")
                        })

                        st.session_state.saved_images.add(image_hash)

                        st.success("Image saved to your history!")

                    else:
                        st.info("This image is already in your history.")

            st.markdown("---")

            st.markdown("### 🔬 Image Inspection Workflow")

            a, b, c = st.columns(3)

            with a:
                st.success("**STEP 1**\n\nImage received")

            with b:
                st.info("**STEP 2**\n\nPreprocessing pending")

            with c:
                st.warning("**STEP 3**\n\nModel connection pending")

            st.warning(
                "⚠️ Genuine disease prediction is not available yet "
                "because the trained classification model has not been connected. "
                "This screen currently provides image capture, upload and preview."
            )

        except Exception:

            st.error("Unable to open this image. Please try another JPG or PNG file.")

    else:

        st.markdown("""
        <div class="card">
            <h3>🌱 Ready to inspect your plant?</h3>
            <p>Choose Upload from device or Open camera above.</p>
            <p>For better image quality, keep the leaf clearly visible in good lighting.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📷 Tips for a better image")

        x, y, z = st.columns(3)

        x.success("☀️ Good lighting\n\nUse natural daylight.")
        y.info("🍃 Clear leaf\n\nKeep the leaf in focus.")
        z.warning("📸 Avoid blur\n\nHold your camera steadily.")

# =====================================================
# AI MODELS
# =====================================================

elif page == "🧠 AI Models":

    st.markdown("""
    <div class="hero">
        <h1>Explore AI Models 🧠</h1>
        <p>Understand the deep-learning architectures explored in this project.</p>
    </div>
    """, unsafe_allow_html=True)

    model_choice = st.radio(
        "Select a model to explore",
        ["Custom CNN", "MobileNetV2"],
        horizontal=True
    )

    st.markdown("---")

    if model_choice == "Custom CNN":

        st.markdown("## 🧠 Custom Convolutional Neural Network")

        st.write("""
        A Convolutional Neural Network, also called CNN, is a deep-learning
        model that learns patterns from images.

        It can learn visual features such as:
        """)

        st.markdown("""
        - Shapes and edges
        - Leaf textures
        - Spots and patterns
        - Visual differences between categories
        """)

        st.success("Project role: A custom image classification model.")

    else:

        st.markdown("## ⚡ MobileNetV2")

        st.write("""
        MobileNetV2 is a lightweight deep-learning architecture used
        for image recognition.

        It is designed to perform image recognition efficiently.
        """)

        st.markdown("""
        - Lightweight architecture
        - Efficient convolution operations
        - Useful for image recognition
        - Uses learned visual features
        """)

        st.success("Project role: An alternative image classification model.")

    st.markdown("---")

    st.markdown("### Model Comparison")

    comparison = pd.DataFrame({
        "Feature": [
            "Architecture",
            "Feature extraction",
            "Project purpose"
        ],
        "Custom CNN": [
            "Custom CNN architecture",
            "Learns patterns from training images",
            "Image classification"
        ],
        "MobileNetV2": [
            "Lightweight pretrained architecture",
            "Uses learned visual features",
            "Image classification"
        ]
    })

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "Actual model accuracy and performance should be added only "
        "after verifying the real evaluation results."
    )

# =====================================================
# ANALYTICS
# =====================================================

elif page == "📊 Analytics":

    st.markdown("""
    <div class="hero">
        <h1>Project Analytics 📊</h1>
        <p>Explore your current session activity and project workflow.</p>
    </div>
    """, unsafe_allow_html=True)

    total = len(st.session_state.history)

    c1, c2, c3 = st.columns(3)

    c1.metric("Images saved", total)
    c2.metric("Available model options", 2)
    c3.metric("Target categories", 5)

    st.markdown("---")

    st.markdown("### 📈 Model exploration")

    model_data = pd.DataFrame({
        "Model": ["Custom CNN", "MobileNetV2"],
        "Available": [1, 1]
    })

    st.bar_chart(
        model_data.set_index("Model"),
        y="Available"
    )

    st.caption(
        "This chart shows the two model options included in the interface, "
        "not their accuracy or performance."
    )

    st.markdown("---")

    st.markdown("### 🍅 Project classification categories")

    category_data = pd.DataFrame({
        "Category": disease_classes,
        "Included in project demo": [1, 1, 1, 1, 1]
    })

    st.bar_chart(
        category_data.set_index("Category")
    )

    st.markdown("---")

    st.markdown("### Recent activity")

    if st.session_state.history:

        activity = pd.DataFrame(st.session_state.history)

        st.dataframe(
            activity,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No image activity yet. Upload a leaf image to begin.")

# =====================================================
# HISTORY
# =====================================================

elif page == "📁 History":

    st.markdown("""
    <div class="hero">
        <h1>Your Image History 📁</h1>
        <p>Review images saved during your current session.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.history:

        history_df = pd.DataFrame(st.session_state.history)

        st.metric("Total saved images", len(history_df))

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

        if st.button("🗑️ Clear all history"):

            st.session_state.history = []
            st.session_state.saved_images = set()

            st.rerun()

    else:

        st.info(
            "Your history is empty. Open Disease Scanner, "
            "upload an image and click Save to My History."
        )

# =====================================================
# ABOUT PROJECT
# =====================================================

elif page == "📖 About Project":

    st.markdown("""
    <div class="hero">
        <h1>About LeafCare AI 🌿</h1>
        <p>Technology for exploring plant leaf disease classification.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎯 Project Objective")

    st.write("""
    Plant Leaf Disease Image Classification explores the use of deep-learning
    techniques to classify plant leaf images.

    The project focuses on image acquisition, preprocessing, feature extraction,
    classification and displaying results through an interactive interface.
    """)

    st.markdown("---")

    st.markdown("### 🛠️ Technologies Used")

    technologies = [
        "Python",
        "TensorFlow",
        "Keras",
        "NumPy",
        "Pandas",
        "Matplotlib",
        "Scikit-learn",
        "Streamlit"
    ]

    cols = st.columns(4)

    for i, tech in enumerate(technologies):
        with cols[i % 4]:
            st.markdown(
                f"""
                <div class="small-card">
                    <p>💻 <b>{tech}</b></p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    st.markdown("### 🔄 Project Workflow")

    st.info("01. Image Collection")
    st.info("02. Image Preprocessing")
    st.info("03. Feature Extraction")
    st.info("04. Model Training")
    st.info("05. Model Evaluation")
    st.success("06. Streamlit Interface")

    st.markdown("---")

    st.markdown("### 🌱 Project Summary")

    st.write("""
    The goal is to combine image processing, deep learning and an interactive
    interface to explore automated plant leaf disease classification.
    """)

    st.caption("Plant Leaf Disease Image Classification | Academic Project")

# ---------------- FOOTER ----------------

st.markdown("---")

st.markdown(
    "<center><p style='color:#718273;'>🌿 LeafCare AI | Plant Leaf Disease Classification</p></center>",
    unsafe_allow_html=True
)
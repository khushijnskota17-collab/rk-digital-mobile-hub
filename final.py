import streamlit as st
import pandas as pd
import os
import io
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder

# 1. Page Configuration (Sidebar Forced Open)
st.set_page_config(page_title="Mobile Hub ERP", layout="wide", initial_sidebar_state="expanded")

# 2. Sidebar Navigation
page = st.sidebar.radio("Navigation", ["Home", "Repair Chatbot", "Shop Mobiles", "Admin Panel"], key="main_nav")
REVIEWS_FILE = "reviews.csv"
# ==========================================
# --- PAGE 1: HOME ---
# ==========================================
if page == "Home":
  # Custom Styling
  st.markdown(
      """
        <style>
        .hero-banner {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            padding: 35px 20px;
            border-radius: 16px;
            color: white;
            text-align: center;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            margin-bottom: 25px;
        }
        .hero-banner h1 {
            color: #38bdf8 !important;
            font-size: 2.3rem;
            font-weight: 800;
            margin-bottom: 5px;
        }
        .stat-card {
            background: #ffffff;
            border-radius: 12px;
            padding: 18px;
            text-align: center;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 20px -5px rgba(0,0,0,0.15);
            border-color: #3b82f6;
        }
        .review-card {
            background: #ffffff;
            border-left: 4px solid #f59e0b;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        </style>
    """,
      unsafe_allow_html=True,
  )

  # Interactive HTML Banner
  st.markdown(
      """
        <div class="hero-banner">
            <h1>📱 RK DIGITAL MOBILE HUB</h1>
            <p style="font-size: 1.1rem; opacity: 0.9;">Sales, Express Repairs & Smart Inventory Management System</p>
            <span style="background: #22c55e; color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 0.85rem;">
                ● STORE OPEN TODAY
            </span>
        </div>
    """,
      unsafe_allow_html=True,
  )

  # Highlights Grid
  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.markdown(
        """
            <div class="stat-card">
                <h3 style="color:#2563eb; margin:0;">⚡ 30 Min</h3>
                <p style="font-weight:600; color:#475569; margin-top:5px; font-size:14px;">Express Screen Fix</p>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col2:
    st.markdown(
        """
            <div class="stat-card">
                <h3 style="color:#16a34a; margin:0;">🛡️ 100%</h3>
                <p style="font-weight:600; color:#475569; margin-top:5px; font-size:14px;">Original Parts</p>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col3:
    st.markdown(
        """
            <div class="stat-card">
                <h3 style="color:#d97706; margin:0;">⭐ 4.9 / 5</h3>
                <p style="font-weight:600; color:#475569; margin-top:5px; font-size:14px;">User Rating</p>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col4:
    st.markdown(
        """
            <div class="stat-card">
                <h3 style="color:#9333ea; margin:0;">🏷️ Best</h3>
                <p style="font-weight:600; color:#475569; margin-top:5px; font-size:14px;">Price Guarantee</p>
            </div>
        """,
        unsafe_allow_html=True,
    )

  st.divider()

  # Reviews Display & Review Form
  col_rev_left, col_rev_right = st.columns([1.2, 1])

  with col_rev_left:
    st.markdown("### 💬 Customer Reviews")
    if os.path.exists(REVIEWS_FILE):
      rev_df = pd.read_csv(REVIEWS_FILE)
      if not rev_df.empty:
        for idx, row in rev_df.tail(4).iterrows():
          st.markdown(
              f"""
                        <div class="review-card">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <strong style="color:#1e293b; font-size:15px;">{row['Name']}</strong>
                                <span style="color:#f59e0b; font-weight:bold;">{row['Rating']}</span>
                            </div>
                            <p style="margin-top:5px; color:#475569; font-size:13px; font-style:italic;">"{row['Review']}"</p>
                        </div>
                    """,
              unsafe_allow_html=True,
          )
      else:
        st.info("Abhi tak koi review save nahi hai.")

  with col_rev_right:
    st.markdown("### ✍️ Leave a Review")
    with st.form("home_review_form"):
      rev_name = st.text_input("Your Name")
      rev_rating = st.selectbox(
          "Rating",
          [
              "★ ★ ★ ★ ★",
              "★ ★ ★ ★ ☆",
              "★ ★ ★ ☆ ☆",
              "★ ★ ☆ ☆ ☆",
          ],
      )
      rev_text = st.text_area("Your Feedback / Experience", height=80)
      submit_btn = st.form_submit_button(
          "⭐ Post Review", use_container_width=True
      )

      if submit_btn:
        if rev_name and rev_text:
          new_data = {
              "Name": [rev_name],
              "Rating": [rev_rating],
              "Review": [rev_text],
          }
          df_new = pd.DataFrame(new_data)
          df_new.to_csv(
              REVIEWS_FILE,
              mode="a",
              index=False,
              header=not os.path.exists(REVIEWS_FILE),
          )
          st.balloons()
          st.success("Review posted successfully!")
          st.rerun()
        else:
          st.warning("Please fill both Name and Review fields.")
# ==========================================
# --- PAGE 2: REPAIR CHATBOT ---
# ==========================================
elif page == "Repair Chatbot":
    st.title("🛠️ Mobile Repair Assistant")
    
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'brand' not in st.session_state:
        st.session_state.brand = ""

    if st.session_state.step == 0:
        st.write("### Welcome! What kind of mobile phone do you have?")
        brands = ["iPhone", "Samsung", "OnePlus", "Oppo", "Vivo", "Motorola", "Redmi", "Other"]
        cols = st.columns(4)
        for i, b in enumerate(brands):
            if cols[i % 4].button(b, key=f"repair_{b}"):
                st.session_state.brand = b
                st.session_state.step = 1
                st.rerun()

    elif st.session_state.step == 1:
        st.write(f"### What problem are you facing with your {st.session_state.brand}?")
        problems = {
            "Screen Replacement": "₹5000",
            "Battery Replacement": "₹1000",
            "Charging Port Repair": "₹500",
            "Camera Repair": "₹3500"
        }
        for prob, price in problems.items():
            if st.button(f"{prob} ({price})", use_container_width=True):
                st.session_state.step = 2
                st.rerun()

    elif st.session_state.step == 2:
        st.success("Great! Please enter your details to book.")
        name = st.text_input("Your Name")
        phone = st.text_input("Phone Number")
        
        if st.button("Confirm Booking", key="booking_final"):
            if name and phone:
                new_entry = {
                    "Name": [name],
                    "Phone": [phone],
                    "Model": [st.session_state.brand],
                    "Date": [pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")]
                }
                df_new = pd.DataFrame(new_entry)
                df_new.to_csv("bookings.csv", mode='a', index=False, header=not os.path.exists("bookings.csv"))
                st.balloons()
                st.success("Your details notified to the owner!")
            else:
                st.error("Please fill your Name and Phone number.")

    if st.button("Start Over"):
        st.session_state.step = 0
        st.rerun()

# ==========================================
# --- PAGE 3: SHOP MOBILES ---
# ==========================================
elif page == "Shop Mobiles":
    if 'selected_brand' not in st.session_state:
        st.session_state.selected_brand = None

    if st.session_state.selected_brand is None:
        st.title("🛍️ Select Your Brand")
        img_folder = "."

        brands_config = {
            "iPhone": "iphone.jpeg", "Samsung": "samsung.jpeg", "Realme": "realme.jpeg",
            "OPPO": "oppo.jpeg", "Google": "google.jpeg", "Motorola": "motorola.jpeg",
            "Vivo": "vivo.jpeg", "POCO": "poco.jpeg", "AI+": "nova.jpeg", "Nothing": "nothing.jpeg"
        }

        brand_items = list(brands_config.items())
        
        for i in range(0, len(brand_items), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(brand_items):
                    name, filename = brand_items[i + j]
                    full_img_path = os.path.join(img_folder, filename)
                    
                    with cols[j]:
                        if os.path.exists(full_img_path):
                            st.image(full_img_path, width=110)
                        else:
                            st.warning("Image Missing")
                        
                        if st.button(f"{name}", key=f"btn_brand_{name}"):
                            st.session_state.selected_brand = name
                            st.rerun()
    else:
        brand = st.session_state.selected_brand
        st.title(f"📱 Available Models - {brand}")
        
        if st.button("⬅️ Back to Brands"):
            st.session_state.selected_brand = None
            st.rerun()

        st.divider()

        inventory_items = []
        if os.path.exists("inventory.csv"):
            try:
                inv_df = pd.read_csv("inventory.csv")
                if 'Brand' in inv_df.columns:
                    matched_df = inv_df[inv_df['Brand'].astype(str).str.strip().str.lower() == brand.strip().lower()]
                    inventory_items = matched_df.to_dict('records')
            except Exception as e:
                st.error(f"Error reading inventory: {e}")

        if inventory_items:
            for idx, item in enumerate(inventory_items):
                st.subheader(f"📲 {item['Model']}")
                st.write(f"**Price:** ₹{item['Price']}")
                
                with st.form(key=f"order_form_{idx}"):
                    cust_name = st.text_input("Your Full Name")
                    cust_phone = st.text_input("Phone Number")
                    submit_order = st.form_submit_button("🛒 Buy / Reserve Now")

                    if submit_order:
                        if cust_name and cust_phone:
                            new_order = {
                                "Customer Name": [cust_name],
                                "Phone": [cust_phone],
                                "Item Ordered": [f"{brand} {item['Model']}"],
                                "Price": [item['Price']],
                                "Date": [pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")]
                            }
                            order_df = pd.DataFrame(new_order)
                            order_df.to_csv("sales.csv", mode='a', index=False, header=not os.path.exists("sales.csv"))
                            st.balloons()
                            st.success("🎉 Order Placed Successfully!")
                        else:
                            st.warning("Please enter your name and phone number.")
                st.divider()
        else:
            st.warning(f"NO STOCK AVAILABLE")
            st.info("COMPANY DISCONTINUED OLD MODELS")

# ==========================================
# --- PAGE 4: ADMIN PANEL ---
# ==========================================
elif page == "Admin Panel":
    st.title("🔒 Owner & Admin Portal")

    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        st.subheader("Admin Login Required")
        with st.form("admin_login_form"):
            admin_id = st.text_input("Admin ID")
            admin_pass = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("🔓 Login to Dashboard")

            if login_btn:
                if admin_id == "rkdigi2005" and admin_pass == "ROHITJAIN":
                    st.session_state.admin_logged_in = True
                    st.success("Access Granted!")
                    st.rerun()
                else:
                    st.error("Invalid Admin ID or Password.")
    else:
        col_head1, col_head2 = st.columns([4, 1])
        with col_head1:
            st.write("Welcome, **Admin**!")
        with col_head2:
            if st.button("🚪 Logout"):
                st.session_state.admin_logged_in = False
                st.rerun()

        st.divider()
        tab1, tab2, tab3 = st.tabs(["📊 Repair Bookings", "🎙️ Add Inventory", "🛒 Sales Orders"])

        with tab1:
            st.subheader("📊 Repair Chatbot Analytics")
            if os.path.exists("bookings.csv"):
                df = pd.read_csv("bookings.csv")
                df_unique = df.drop_duplicates(subset=['Phone'], keep='last')

                mcol1, mcol2, mcol3 = st.columns(3)
                with mcol1:
                    st.metric("Total Unique Customers", len(df_unique))
                with mcol2:
                    st.metric("Total Bookings Logged", len(df))
                with mcol3:
                    st.metric("Latest Customer", df['Name'].iloc[-1] if not df.empty else "N/A")

                st.divider()
                st.subheader("All Scheduled Repair Appointments")
                st.dataframe(df, use_container_width=True)

                if 'Model' in df.columns:
                    st.subheader("Phone Brand With Highest Repair Rates")
                    st.bar_chart(df['Model'].value_counts())

                st.download_button(
                    label="📥 Download Bookings CSV",
                    data=df.to_csv(index=False),
                    file_name="final_bookings.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No repair booking records found ('bookings.csv' missing).")

        with tab2:
            st.subheader("🛒 Add New Item to Digital Inventory")

            def convert_speech_to_text():
                recognizer = sr.Recognizer()
                try:
                    audio_data = io.BytesIO(st.session_state.uploaded_audio['bytes'])
                    with sr.AudioFile(audio_data) as source:
                        recorded_audio = recognizer.record(source)
                        return recognizer.recognize_google(recorded_audio, language='hi-IN')
                except Exception:
                    return ""

            if "recorded_model_name" not in st.session_state:
                st.session_state.recorded_model_name = ""

            audio_input = mic_recorder(
                start_prompt="🔴 Click to Speak Model Name",
                stop_prompt="⏹️ Stop & Transcribe",
                key='inventory_mic'
            )

            if audio_input:
                st.session_state.uploaded_audio = audio_input
                with st.spinner("Processing speech to text input..."):
                    detected_text = convert_speech_to_text()
                    if detected_text:
                        st.session_state.recorded_model_name = detected_text
                        st.success(f"Transcribed: {detected_text}")
                    else:
                        st.error("Audio clarity low. Try again.")

            with st.form("inventory_voice_form", clear_on_submit=True):
                brand_selector = st.selectbox("Select Device Brand", ["iPhone", "Samsung", "Vivo", "OPPO", "Realme", "Mi", "Google", "Motorola", "POCO", "AI+", "Nothing"])
                model_details = st.text_input("Model Name & Configurations:", value=st.session_state.recorded_model_name)
                item_price = st.number_input("Offer Price (INR):", min_value=0, step=10)
                submit_btn = st.form_submit_button("➕ SAVE TO INVENTORY")

            if submit_btn:
                if model_details:
                    new_item = {"Brand": brand_selector, "Model": model_details, "Price": (int(item_price))}
                    new_df = pd.DataFrame([new_item])
                    inv_csv = "inventory.csv"
                    new_df.to_csv(inv_csv, mode='a', index=False, header=not os.path.exists(inv_csv))
                    st.success(f"🎉 Saved: {brand_selector} {model_details} (₹{int(item_price)})")
                    st.session_state.recorded_model_name = ""
                    st.rerun()
                else:
                    st.warning("Please enter or speak a model name first.")
        with tab3:
            st.subheader("🛒 Mobile Purchase & Reservation Orders")
            if os.path.exists("sales.csv"):
                sales_df = pd.read_csv("sales.csv")
                st.dataframe(sales_df, use_container_width=True)
                st.download_button(
                    label="📥 Download Sales CSV",
                    data=sales_df.to_csv(index=False),
                    file_name="final_sales.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No customer purchase orders found yet.")

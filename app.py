import streamlit as st
import pandas as pd
from datetime import datetime

# ============================================================
# MARINE OPERATIONS INTELLIGENCE CENTRE
# CLIENT CLEAN TEMPLATE
# ============================================================

st.set_page_config(
    page_title="Marine Operations Intelligence Centre",
    page_icon="⚓",
    layout="wide",
)

# ============================================================
# SESSION / CLIENT DATABASE
# Tidak ada perusahaan atau kapal bawaan
# ============================================================

DEFAULT_DATA = {
    "company_name": "",
    "vessels": [],
    "voyage": [],
    "crew": [],
    "pms": [],
    "defects": [],
    "certificates": [],
    "bunker": [],
    "cargo": [],
    "hsse": [],
    "audit": [],
    "actions": [],
}

for key, value in DEFAULT_DATA.items():
    if key not in st.session_state:
        st.session_state[key] = value.copy() if isinstance(value, list) else value


# ============================================================
# LOGIN
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

ROLES = [
    "Marine Superintendent",
    "DPA",
    "Manager Operation Marine",
]


def login_page():
    st.title("⚓ MARINE OPERATIONS INTELLIGENCE CENTRE")
    st.subheader("Secure Operations Portal")

    st.caption(
        "Fleet Intelligence • HSSE • PMS • Voyage • Risk • "
        "Operational Control"
    )

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Operational Role", ROLES)

    if st.button("LOGIN"):
        if username.strip() and password.strip():
            st.session_state.logged_in = True
            st.session_state.username = username.strip()
            st.session_state.role = role
            st.rerun()
        else:
            st.warning("Masukkan Username dan Password.")


if not st.session_state.logged_in:
    login_page()
    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚓ CONTROL CENTRE")

company = st.session_state.company_name.strip()

if company:
    st.sidebar.caption(company)
else:
    st.sidebar.caption("CLIENT NOT CONFIGURED")

st.sidebar.write(
    f"Role: {st.session_state.get('role', 'Marine Superintendent')}"
)

MENU = [
    "Client Initial Setup",
    "Dashboard",
    "Fleet",
    "Crew",
    "Voyage Operations",
    "HSSE / DPA",
    "PMS / Maintenance",
    "Defects",
    "Certificates",
    "Bunker",
    "Cargo",
    "Audit & Findings",
    "Action Tracker",
    "AI Marine Copilot",
    "Executive Reports",
    "WhatsApp Operations",
    "System",
]

menu = st.sidebar.radio("MENU", MENU)

vessels = st.session_state.vessels

if vessels:
    selected_vessel = st.sidebar.selectbox(
        "Selected Vessel",
        ["ALL VESSELS"] + vessels,
    )
else:
    selected_vessel = "ALL VESSELS"
    st.sidebar.info("Belum ada kapal terdaftar.")

st.sidebar.metric("Fleet", len(vessels))


# ============================================================
# HELPERS
# ============================================================

def records_df(key):
    records = st.session_state.get(key, [])
    if isinstance(records, list) and records:
        return pd.DataFrame(records)
    return pd.DataFrame()


def vessel_input(label="Vessel"):
    if not st.session_state.vessels:
        st.warning(
            "Belum ada kapal. Tambahkan kapal melalui Client Initial Setup."
        )
        return None

    return st.selectbox(label, st.session_state.vessels)


def add_record(key, record):
    st.session_state[key].append(record)
    st.success("Data berhasil disimpan.")


# ============================================================
# CLIENT INITIAL SETUP
# ============================================================

if menu == "Client Initial Setup":

    st.header("🏢 Client Initial Setup")

    st.caption(
        "Konfigurasi perusahaan dan armada untuk client baru. "
        "Template ini tidak membawa data perusahaan atau kapal sebelumnya."
    )

    st.subheader("Shipping Company")

    company_name = st.text_input(
        "Shipping Company Name",
        value=st.session_state.company_name,
        placeholder="Masukkan nama perusahaan pelayaran",
    )

    if st.button("Save Company Name"):
        st.session_state.company_name = company_name.strip()
        st.success("Nama perusahaan berhasil disimpan.")

    st.divider()

    st.subheader("Fleet Register")

    new_vessel = st.text_input(
        "Vessel Name",
        placeholder="Contoh: MV OCEAN STAR",
    )

    if st.button("Add Vessel"):
        vessel_name = new_vessel.strip().upper()

        if not vessel_name:
            st.warning("Masukkan nama kapal.")

        elif vessel_name in st.session_state.vessels:
            st.warning("Kapal sudah terdaftar.")

        else:
            st.session_state.vessels.append(vessel_name)
            st.success(f"{vessel_name} berhasil ditambahkan.")
            st.rerun()

    if st.session_state.vessels:
        fleet_df = pd.DataFrame(
            {
                "No": range(1, len(st.session_state.vessels) + 1),
                "Vessel": st.session_state.vessels,
                "Status": ["ACTIVE"] * len(st.session_state.vessels),
            }
        )

        st.dataframe(
            fleet_df,
            use_container_width=True,
            hide_index=True,
        )

        remove_vessel = st.selectbox(
            "Remove Vessel",
            st.session_state.vessels,
        )

        if st.button("Remove Selected Vessel"):
            st.session_state.vessels.remove(remove_vessel)
            st.success(f"{remove_vessel} dihapus.")
            st.rerun()

    else:
        st.info(
            "Fleet masih kosong. Client dapat menambahkan kapal sendiri."
        )


# ============================================================
# DASHBOARD
# ============================================================

elif menu == "Dashboard":

    st.header("📊 Operations Command Dashboard")

    fleet_count = len(st.session_state.vessels)

    voyage_df = records_df("voyage")
    defect_df = records_df("defects")
    action_df = records_df("actions")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Fleet", fleet_count)
    c2.metric("Active Vessels", fleet_count)
    c3.metric("Voyage Records", len(voyage_df))
    c4.metric("Open Actions", len(action_df))

    if fleet_count == 0:
        st.info(
            "CLIENT TEMPLATE READY — lakukan Client Initial Setup "
            "untuk memasukkan perusahaan dan kapal."
        )
    else:
        st.success("Operational database aktif.")

    st.subheader("Operational Intelligence Overview")

    overview = pd.DataFrame(
        [
            ["Fleet", fleet_count],
            ["Voyage Records", len(voyage_df)],
            ["Defects", len(defect_df)],
            ["PMS Records", len(records_df("pms"))],
            ["Certificates", len(records_df("certificates"))],
            ["HSSE Records", len(records_df("hsse"))],
            ["Crew Records", len(records_df("crew"))],
        ],
        columns=["Indicator", "Value"],
    )

    st.dataframe(
        overview,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# FLEET
# ============================================================

elif menu == "Fleet":

    st.header("🚢 Fleet Intelligence")

    if not st.session_state.vessels:
        st.info("Belum ada kapal terdaftar.")
    else:
        fleet_df = pd.DataFrame(
            {
                "Vessel": st.session_state.vessels,
                "Status": ["ACTIVE"] * len(st.session_state.vessels),
            }
        )

        st.dataframe(
            fleet_df,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# CREW
# ============================================================

elif menu == "Crew":

    st.header("👨‍✈️ Crew Operational Intelligence")

    vessel = vessel_input()

    if vessel:
        col1, col2 = st.columns(2)

        with col1:
            crew_name = st.text_input("Crew Name")
            rank = st.text_input("Rank")

        with col2:
            nationality = st.text_input("Nationality")
            certificate = st.text_input("Certificate / COC")

        if st.button("Save Crew Record"):
            if crew_name.strip():
                add_record(
                    "crew",
                    {
                        "Vessel": vessel,
                        "Crew Name": crew_name.strip(),
                        "Rank": rank.strip(),
                        "Nationality": nationality.strip(),
                        "Certificate": certificate.strip(),
                    },
                )
            else:
                st.warning("Masukkan nama crew.")

    crew_df = records_df("crew")

    if not crew_df.empty:
        st.dataframe(
            crew_df,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# VOYAGE
# ============================================================

elif menu == "Voyage Operations":

    st.header("🧭 Voyage Operations")

    vessel = vessel_input()

    if vessel:
        voyage = st.text_input("Voyage / Route")
        status = st.selectbox(
            "Voyage Status",
            ["NORMAL", "DELAYED", "ATTENTION"],
        )

        if st.button("Save Voyage Record"):
            add_record(
                "voyage",
                {
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Vessel": vessel,
                    "Voyage": voyage.strip(),
                    "Status": status,
                },
            )

    df = records_df("voyage")

    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)


# ============================================================
# HSSE
# ============================================================

elif menu == "HSSE / DPA":

    st.header("🦺 HSSE / DPA Intelligence")

    vessel = vessel_input()

    if vessel:
        category = st.selectbox(
            "Category",
            [
                "Safety Observation",
                "Near Miss",
                "Incident",
                "Environmental",
                "Security",
            ],
        )

        description = st.text_area("Description")

        if st.button("Save HSSE Record"):
            add_record(
                "hsse",
                {
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Vessel": vessel,
                    "Category": category,
                    "Description": description.strip(),
                },
            )

    df = records_df("hsse")

    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)


# ============================================================
# PMS
# ============================================================

elif menu == "PMS / Maintenance":

    st.header("🔧 PMS / Maintenance Intelligence")

    vessel = vessel_input()

    if vessel:
        equipment = st.text_input("Equipment")
        maintenance = st.text_input("Maintenance / Job")
        status = st.selectbox(
            "Status",
            ["OPEN", "PLANNED", "COMPLETED", "OVERDUE"],
        )

        if st.button("Save PMS Record"):
            add_record(
                "pms",
                {
                    "Vessel": vessel,
                    "Equipment": equipment.strip(),
                    "Maintenance": maintenance.strip(),
                    "Status": status,
                },
            )

    df = records_df("pms")

    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)


# ============================================================
# DEFECTS
# ============================================================

elif menu == "Defects":

    st.header("⚠️ Defects Intelligence")

    vessel = vessel_input()

    if vessel:
        defect = st.text_area("Defect Description")
        priority = st.selectbox(
            "Priority",
            ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
        )

        if st.button("Save Defect"):
            add_record(
                "defects",
                {
                    "Vessel": vessel,
                    "Defect": defect.strip(),
                    "Priority": priority,
                },
            )

    df = records_df("defects")

    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)


# ============================================================
# CERTIFICATES
# ============================================================

elif menu == "Certificates":

    st.header("📜 Certificates Intelligence")

    vessel = vessel_input()

    if vessel:
        certificate_name = st.text_input("Certificate Name")
        expiry = st.date_input("Expiry Date")

        if st.button("Save Certificate"):
            add_record(
                "certificates",
                {
                    "Vessel": vessel,
                    "Certificate": certificate_name.strip(),
                    "Expiry": str(expiry),
                },
            )

    df = records_df("certificates")

    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)


# ============================================================
# BUNKER
# ============================================================

elif menu == "Bunker":

    st.header("⛽ Bunker Intelligence")

    vessel = vessel_input()

    if vessel:
        fuel_type = st.selectbox(
            "Fuel Type",
            ["MGO", "MDO", "HFO", "VLSFO", "OTHER"],
        )

        quantity = st.number_input(
            "Quantity",
            min_value=0.0,
        )

        if st.button("Save Bunker Record"):
            add_record(
                "bunker",
                {
                    "Vessel": vessel,
                    "Fuel": fuel_type,
                    "Quantity": quantity,
                },
            )

    df = records_df("bunker")

    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)


# ============================================================
# CARGO
# ============================================================

elif menu == "Cargo":

    st.header("📦 Cargo Intelligence")

    vessel = vessel_input()

    if vessel:
        cargo = st.text_input("Cargo")
        quantity = st.number_input(
            "Cargo Quantity",
            min_value=0.0,
        )

        if st.button("Save Cargo Record"):
            add_record(
                "cargo",
                {
                    "Vessel": vessel,
                    "Cargo": cargo.strip(),
                    "Quantity": quantity,
                },
            )

    df = records_df("cargo")

    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)


# ============================================================
# AUDIT
# ============================================================

elif menu == "Audit & Findings":

    st.header("🔍 Audit & Findings")

    vessel = vessel_input()

    if vessel:
        finding = st.text_area("Audit Finding")
        status = st.selectbox(
            "Finding Status",
            ["OPEN", "IN PROGRESS", "CLOSED"],
        )

        if st.button("Save Finding"):
            add_record(
                "audit",
                {
                    "Vessel": vessel,
                    "Finding": finding.strip(),
                    "Status": status,
                },
            )

    df = records_df("audit")

    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)


# ============================================================
# ACTION TRACKER
# ============================================================

elif menu == "Action Tracker":

    st.header("✅ Action Tracker")

    action = st.text_input("Action Required")
    responsible = st.text_input("Responsible Person")

    if st.button("Save Action"):
        if action.strip():
            add_record(
                "actions",
                {
                    "Action": action.strip(),
                    "Responsible": responsible.strip(),
                    "Status": "OPEN",
                },
            )

    df = records_df("actions")

    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)


# ============================================================
# AI COPILOT
# ============================================================

elif menu == "AI Marine Copilot":

    st.header("🧠 AI Marine Copilot")

    st.info(
        "AI module ready for client-specific API configuration."
    )

    question = st.text_area(
        "Ask Marine Operations AI",
        placeholder="Masukkan pertanyaan operasional...",
    )

    if st.button("Analyze"):
        if question.strip():
            st.warning(
                "AI API belum dikonfigurasi untuk client ini. "
                "Tambahkan API key melalui Streamlit Secrets."
            )


# ============================================================
# EXECUTIVE REPORTS
# ============================================================

elif menu == "Executive Reports":

    st.header("📑 Executive Reports")

    st.metric("Fleet", len(st.session_state.vessels))
    st.metric("Voyage Records", len(records_df("voyage")))
    st.metric("Defects", len(records_df("defects")))
    st.metric("HSSE Records", len(records_df("hsse")))

    st.info(
        "Executive reporting akan mengikuti data aktual client."
    )


# ============================================================
# WHATSAPP
# ============================================================

elif menu == "WhatsApp Operations":

    st.header("💬 WhatsApp Operations")

    st.info(
        "WhatsApp integration belum dikonfigurasi untuk client ini."
    )

    st.text_input(
        "Client WhatsApp Number",
        placeholder="+62...",
    )


# ============================================================
# SYSTEM
# ============================================================

elif menu == "System":

    st.header("⚙️ System")

    st.write(
        "Application:",
        "MARINE OPERATIONS INTELLIGENCE CENTRE — CLIENT",
    )

    st.write(
        "Company:",
        st.session_state.company_name or "NOT CONFIGURED",
    )

    st.write(
        "Registered Vessels:",
        len(st.session_state.vessels),
    )

    st.success("CLIENT CLEAN TEMPLATE ACTIVE")

    if st.button("LOGOUT"):
        st.session_state.logged_in = False
        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "MARINE OPERATIONS INTELLIGENCE CENTRE • "
    "CLIENT CLEAN TEMPLATE • Operational data belongs to each client."
)

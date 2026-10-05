import os
import re
import datetime
from typing import Dict, Any
import streamlit as st

def parse_note_rules(raw_text: str) -> Dict[str, Any]:
    """
    Deterministic rule-based NLP parser.
    Extracts visitor/courier, company, host, purpose, and tracking details.
    Guaranteed 100% uptime with zero external API dependencies.
    """
    text = raw_text.strip()
    is_delivery = any(
        w in text.lower()
        for w in [
            "package", "courier", "aramex", "dhl", "fedex", "ups",
            "box", "binder", "envelope", "parcel", "delivery", "dropped off"
        ]
    )

    data: Dict[str, Any] = {
        "is_delivery": is_delivery,
        "raw_text": text,
        "timestamp": datetime.datetime.now().strftime("%I:%M %p"),
    }

    if is_delivery:
        # Carrier extraction
        carrier_match = re.search(
            r'\b(Aramex|DHL|FedEx|UPS|Amazon|Careem|Fetchr|Courier)\b',
            text,
            re.IGNORECASE
        )
        data["carrier"] = carrier_match.group(1).title() if carrier_match else "Courier"

        # Tracking number
        track_match = re.search(
            r'(?:tracking|track|awb)\s*(?:#|no\.?|number)?\s*([A-Za-z0-9\-]+)',
            text,
            re.IGNORECASE
        )
        data["tracking"] = track_match.group(1).upper() if track_match else "N/A"

        # Recipient host
        host_match = re.search(
            r'\b(?:for|to)\b\s+(Eng\.?|Mr\.?|Mrs\.?|Ms\.?|Dr\.?)?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
            text
        )
        if host_match:
            title = host_match.group(1) + " " if host_match.group(1) else ""
            data["host"] = f"{title}{host_match.group(2)}".strip()
        else:
            data["host"] = "Addressee"

        # Item description
        item_match = re.search(
            r'(?:dropped off|delivered|left|brought)\s+(?:a|an)?\s*([^,\.]+?)(?:\s+for|\s+tracking|$)',
            text,
            re.IGNORECASE
        )
        if item_match:
            data["item"] = item_match.group(1).strip()
        else:
            data["item"] = "Parcel / Document Package"

    else:
        # Visitor name and company
        visitor_company_match = re.search(
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+from\s+([A-Za-z0-9\s&]+?)(?:\s+is here|\s+arrived|\s+to see|\s+waiting|$)',
            text,
            re.IGNORECASE
        )
        if visitor_company_match:
            data["visitor"] = visitor_company_match.group(1).title()
            data["company"] = visitor_company_match.group(2).strip().title()
        else:
            v_match = re.search(r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', text)
            data["visitor"] = v_match.group(1).title() if v_match else "Visitor"
            data["company"] = "Guest"

        # Host extraction
        host_match = re.search(
            r'\b(?:to see|with|for)\b\s+(Eng\.?|Mr\.?|Mrs\.?|Ms\.?|Dr\.?)?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
            text
        )
        if host_match:
            title = host_match.group(1) + " " if host_match.group(1) else ""
            data["host"] = f"{title}{host_match.group(2)}".strip()
        else:
            data["host"] = "Host"

        # Topic / Purpose
        topic_match = re.search(
            r'\b(?:regarding|for|about)\b\s+(.+?)(?:\.|$)',
            text,
            re.IGNORECASE
        )
        if topic_match:
            data["topic"] = topic_match.group(1).strip()
        else:
            data["topic"] = "Meeting / Reception Inquiry"

    return data


def generate_alerts(parsed: Dict[str, Any]) -> Dict[str, str]:
    """Generates ready-to-copy notifications across Slack, WhatsApp, and Email."""
    time_str = parsed.get("timestamp", datetime.datetime.now().strftime("%I:%M %p"))

    if parsed["is_delivery"]:
        carrier = parsed.get("carrier", "Courier")
        host = parsed.get("host", "Team")
        item = parsed.get("item", "Package")
        tracking = parsed.get("tracking", "N/A")

        slack_msg = (
            f"📦 *PACKAGE DELIVERED AT RECEPTION*\n"
            f"• *Addressee:* {host}\n"
            f"• *Carrier / Source:* {carrier}\n"
            f"• *Item:* {item}\n"
            f"• *Tracking / Ref:* `{tracking}`\n"
            f"• *Location:* Front Desk Holding Shelf\n"
            f"• *Received At:* {time_str}\n\n"
            f"_Please pick up at your earliest convenience or let reception know if forwarding is required._"
        )

        whatsapp_msg = (
            f"📦 *PACKAGE AT FRONT DESK*\n\n"
            f"Hello {host}, a package has arrived for you:\n"
            f"• *From:* {carrier}\n"
            f"• *Item:* {item}\n"
            f"• *Tracking:* {tracking}\n"
            f"• *Location:* Front Desk Holding Shelf\n\n"
            f"Please collect when convenient!"
        )

        email_subject = f"Package Arrival Notice: {item} received at Reception for {host}"
        email_body = (
            f"Dear {host},\n\n"
            f"A delivery has been logged for you at reception:\n\n"
            f"- Carrier: {carrier}\n"
            f"- Contents/Item: {item}\n"
            f"- Tracking Reference: {tracking}\n"
            f"- Pickup Location: Reception Desk (Parcel Shelf)\n"
            f"- Time Logged: {time_str}\n\n"
            f"Kind regards,\n"
            f"Front Desk Team"
        )
    else:
        visitor = parsed.get("visitor", "Visitor")
        company = parsed.get("company", "External Guest")
        host = parsed.get("host", "Host")
        topic = parsed.get("topic", "Scheduled Meeting")

        slack_msg = (
            f"👋 *VISITOR WAITING IN LOBBY*\n"
            f"• *Host:* {host}\n"
            f"• *Visitor:* {visitor} ({company})\n"
            f"• *Topic / Purpose:* {topic}\n"
            f"• *Status:* Seated in reception waiting area\n"
            f"• *Arrival Time:* {time_str}\n\n"
            f"_Please confirm if you are ready to receive them or need them escorted to a conference room._"
        )

        whatsapp_msg = (
            f"👋 *GUEST ARRIVAL ALERT*\n\n"
            f"Hi {host},\n"
            f"*{visitor}* from *{company}* is here at reception regarding *{topic}*.\n\n"
            f"Status: Waiting in the main lobby.\n"
            f"Please let front desk know when you are ready!"
        )

        email_subject = f"Visitor Arrival: {visitor} ({company}) is waiting at Reception"
        email_body = (
            f"Dear {host},\n\n"
            f"Your guest has arrived and is currently in the lobby:\n\n"
            f"- Visitor: {visitor}\n"
            f"- Company/Affiliation: {company}\n"
            f"- Meeting Topic: {topic}\n"
            f"- Status: Seated in reception lobby\n"
            f"- Arrival Time: {time_str}\n\n"
            f"Please let reception know if you would like us to escort them to a conference room.\n\n"
            f"Best regards,\n"
            f"Front Desk Team"
        )

    return {
        "slack": slack_msg,
        "whatsapp": whatsapp_msg,
        "email_subject": email_subject,
        "email_body": email_body,
    }


def main():
    st.set_page_config(
        page_title="Front-Desk Quick-Alert",
        page_icon="🛎️",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # Custom UI styling
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
            color: #0F172A;
        }
        .sub-caption {
            font-size: 1.05rem;
            color: #475569;
            margin-bottom: 1.5rem;
        }
        .badge-visitor {
            background-color: #E0F2FE;
            color: #0369A1;
            padding: 5px 12px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.9rem;
            display: inline-block;
        }
        .badge-delivery {
            background-color: #FEF3C7;
            color: #92400E;
            padding: 5px 12px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.9rem;
            display: inline-block;
        }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar settings
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.info("⚡ **Running in Deterministic NLP Mode**\n\n100% offline uptime with zero API key dependencies.")
        st.markdown("---")
        st.caption("Front-Desk Quick-Alert v1.0.0\nAuthor: Bader Badawi")

    st.markdown('<div class="main-header">🛎️ Front-Desk Quick-Alert</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-caption">Convert raw visitor or delivery arrivals into instant host notifications and reception actions.</div>', unsafe_allow_html=True)

    # 1-Click Quick Test Presets
    st.write("**⚡ Quick Test Examples (1-Click):**")
    col1, col2, col3 = st.columns(3)

    if col1.button("👤 Visitor Arrival", use_container_width=True):
        st.session_state.note = "Ahmad from Consolidated Contractors is here to see Mr. Saad for the 2:30 PM project review."

    if col2.button("📦 Package Delivery", use_container_width=True):
        st.session_state.note = "Aramex courier just dropped off a sealed tender binder for Eng. Omar, tracking #ARX-9821."

    if col3.button("🤝 VIP Meeting", use_container_width=True):
        st.session_state.note = "Samer from Arabtec is here to see Eng. Omar regarding the tender documents."

    # Input field
    raw_input = st.text_input(
        "Front Desk Raw Note:",
        value=st.session_state.get("note", ""),
        placeholder="e.g., Samer from Arabtec is here to see Eng. Omar regarding the tender documents"
    )

    col_gen, col_clear = st.columns([4, 1])
    generate_clicked = col_gen.button("⚡ Generate Notification", type="primary", use_container_width=True)
    if col_clear.button("Clear", use_container_width=True):
        st.session_state.note = ""
        st.rerun()

    # Processing & Display
    if generate_clicked or (raw_input.strip() and "note" in st.session_state and st.session_state.note == raw_input):
        if not raw_input.strip():
            st.warning("⚠️ Please enter a front desk note or click one of the quick test examples above.")
        else:
            parsed = parse_note_rules(raw_input)
            alerts = generate_alerts(parsed)

            st.divider()

            # Category Badge & Summary
            if parsed["is_delivery"]:
                st.markdown('<span class="badge-delivery">📦 DELIVERY / COURIER EVENT</span>', unsafe_allow_html=True)
                
                # Extracted Summary Metrics
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Carrier", parsed.get("carrier", "N/A"))
                m2.metric("Addressee", parsed.get("host", "N/A"))
                m3.metric("Item", parsed.get("item", "N/A"))
                m4.metric("Tracking #", parsed.get("tracking", "N/A"))

                checklist = [
                    "Log package in reception delivery registry",
                    "Place parcel on designated front-desk holding shelf",
                    "Attach physical tag with recipient name and arrival timestamp"
                ]
            else:
                st.markdown('<span class="badge-visitor">👤 VISITOR ARRIVAL EVENT</span>', unsafe_allow_html=True)
                
                # Extracted Summary Metrics
                m1, m2, m3 = st.columns(3)
                m1.metric("Visitor", parsed.get("visitor", "N/A"))
                m2.metric("Company", parsed.get("company", "N/A"))
                m3.metric("Host", parsed.get("host", "N/A"))

                checklist = [
                    "Offer guest water or coffee while they wait",
                    "Seat guest in main lobby lounge or reserve Conference Room A",
                    "Confirm host availability and notify security/access card desk if required"
                ]

            # 1. Multi-platform Internal Alert
            st.subheader("1. Ready-to-Send Internal Alerts")
            tab_slack, tab_wa, tab_email = st.tabs(["💬 Slack / Teams", "📱 WhatsApp", "✉️ Email Draft"])

            with tab_slack:
                st.caption("Formatted with markdown for Slack, Microsoft Teams, or Discord channels:")
                st.code(alerts["slack"], language="markdown")

            with tab_wa:
                st.caption("Formatted with WhatsApp bolding syntax:")
                st.code(alerts["whatsapp"], language="text")

            with tab_email:
                st.caption(f"**Subject:** {alerts['email_subject']}")
                st.code(alerts["email_body"], language="text")

            # 2. Reception Action Checklist
            st.subheader("2. Reception Action Protocol")
            st.caption("Complete these standard operating procedures before closing the alert:")
            for idx, item in enumerate(checklist):
                st.checkbox(item, key=f"chk_{idx}_{hash(raw_input)}")

            st.caption("💡 *Tip: Designed for zero-latency deterministic execution. Works 100% offline and in air-gapped environments without external API keys.*")


if __name__ == "__main__":
    main()

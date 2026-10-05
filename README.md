# 🛎️ Front-Desk Quick-Alert
*(Visitor & Delivery Notification Generator)*

A lightweight, zero-latency micro-app that turns informal receptionist notes into structured, instant host notifications and front-desk operating checklists.

---

## 1. The Real Office Problem
At reception desks, visitors and couriers arrive continuously. Front-desk personnel frequently face interruptions and have to manually draft ad-hoc messages to busy engineers and executives across Slack, WhatsApp, or email.

In the rush, critical details are often omitted:
* Who the visitor is with or which company they represent
* The purpose of the meeting or which conference room they are placed in
* Tracking numbers and exact shelf location for dropped-off parcels
* Hospitality steps (e.g., offering water, seating the guest, logging in registry)

---

## 2. What the App Does (One Job, Done Well)
The user enters one natural-language sentence (or clicks a 1-click test preset), such as:
> *"Samer from Arabtec is here to see Eng. Omar regarding the tender documents."*

The app instantly generates:
1. **Multi-Channel Host Notifications:** Ready-to-copy alerts tailored for:
   * **Slack / Microsoft Teams** (structured markdown bullet points)
   * **WhatsApp** (native WhatsApp bolding format)
   * **Email** (formal subject line & structured body draft)
2. **Reception Action Checklist:** Standard operating protocol with interactive checkboxes (e.g., seating instructions, hospitality protocol, package logging).

---

## 3. Key Technical Highlights
* **Zero Latency & 100% Deterministic:** Built with a regex/NLP rule parser that requires **zero API keys** and runs reliably even offline or behind enterprise air-gapped networks.
* **1-Click Test Buttons:** Includes immediate test presets for Visitor Arrival, Package Delivery, and VIP Meetings so anyone can evaluate the app in seconds.
* **Lightweight Footprint:** Built with pure Python and Streamlit.

---

## 4. How to Run Locally

### Prerequisites
* Python 3.9+ installed

### Step-by-Step
1. Clone or download this directory:
   ```bash
   git clone <your-repo-url>
   cd esss
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
4. Open your browser at `http://localhost:8501`.

---

## 5. How to Deploy to Streamlit Community Cloud (Free in 5 Minutes)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Front-Desk Quick-Alert"
   git branch -M main
   git remote add origin https://github.com/Bader-Badawi/front-desk-quick-alert.git
   git push -u origin main
   ```
2. **Deploy on Streamlit Cloud:**
   * Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
   * Click **"New app"** → select your repository (`front-desk-quick-alert`).
   * Main file path: `app.py`.
   * Click **"Deploy"**.
3. **Get Your Live URL:**
   * Streamlit will build and launch your live application (e.g., `https://front-desk-quick-alert.streamlit.app`).

---

## 6. Email Draft for Saad

```text
Subject: Re: Your application to CMA

Dear Saad,

Here is the link to my project for the assessment:

App Link: [Your Streamlit URL]
Repository: https://github.com/Bader-Badawi/front-desk-quick-alert

1. The Problem:
When visitors or urgent packages arrive at reception, front-desk operators spend unnecessary time drafting ad-hoc messages to hosts across WhatsApp or Slack, often omitting crucial context or delaying guest hospitality.

2. The Solution:
Front-Desk Quick-Alert takes one informal sentence and turns it into:
- A structured, professional host notification ready to paste into Slack, Teams, or WhatsApp.
- An immediate front-office checklist (hospitality and parcel logging).

3. How It Was Built:
Built with Python and Streamlit. It features one-click test buttons for zero-instruction testing and runs deterministically with 100% uptime and zero setup required.

Best regards,
Bader Badawi
```

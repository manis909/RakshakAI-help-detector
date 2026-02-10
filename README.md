# RakshakAI – Help Detection & Alert System 🚨

RakshakAI is an AI-powered safety and emergency alert system that detects distress signals using CCTV camera input and instantly notifies users through a mobile application, Telegram, and SMS.  
The goal is to enable **fast, localized, and automated help** without the victim needing to manually request assistance.

---

## 🔍 Problem Statement
In emergency situations (harassment, assault, accidents), victims often cannot access their phones or call for help. Existing systems rely heavily on manual input.

RakshakAI solves this by:
- Detecting **help gestures / danger signals** via CCTV
- Automatically triggering alerts
- Notifying **nearby users** through a mobile app

---

## 💡 Solution Overview
RakshakAI uses:
- **Computer Vision** for gesture detection
- **Backend APIs** for alert handling
- **Mobile App** to display emergency alerts in real time
- **Telegram & SMS** as fallback alert channels

---

## 🏗️ System Architecture
1. CCTV Camera feeds video to the AI detection module  
2. AI detects emergency gesture / situation  
3. Alert is generated with locality & timestamp  
4. Alert is sent to:
   - Mobile App (primary)
   - Telegram Bot
   - SMS (Twilio)

---

## 🛠️ Tech Stack
### AI & Backend
- Python
- OpenCV
- MediaPipe
- Flask
- Twilio API
- Telegram Bot API

### Mobile App
- React Native
- Expo
- Fetch API

---

## 📱 Features
- Real-time emergency detection
- Automatic alert generation
- Mobile app alert view
- Telegram photo & message alerts
- SMS alerts as backup
- Locality-based alert relevance

---

## 🚀 How to Run
### Backend
```bash
python main2_fixed.py
npx expo start -c
python app.py

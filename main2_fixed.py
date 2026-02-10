import cv2
import mediapipe as mp
import time
import requests
from accident import detect_accident
from twilio.rest import Client
import os
import threading

# ================= CONFIG =================
GESTURE_CONFIRM_FRAMES = 15
PROCESS_EVERY_N_FRAMES = 2
ALERT_COOLDOWN = 20

gesture_counter = 0
last_detected_gesture = "NONE"
current_gesture = "NONE"
last_alert_time = 0
frame_count = 0


def save_screenshot(frame):
    """Save screenshot to alerts folder and return filename"""
    if not os.path.exists("alerts"):
        os.makedirs("alerts")

    filename = f"alerts/alert_{int(time.time())}.jpg"
    cv2.imwrite(filename, frame)
    return filename


# ================= SMS CONFIG =================
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")


client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

LOCALITY_CONTACTS = os.getenv("LOCALITY_CONTACTS", "").split(",")


import requests
ALERT_BACKEND_URL = os.getenv("ALERT_BACKEND_URL", "http://localhost:5000")

def send_alert_to_app(locality):
    url = f"{ALERT_BACKEND_URL}/send-alert"
    payload = {
        "locality": locality,
        "message": "🚨 HELP SIGNAL DETECTED BY CCTV"
    }

    try:
        requests.post(f"{ALERT_BACKEND_URL}/alert", json={
    "type": "POSSIBLE FIGHT",
    "locality": "Hyderabad",
    "message": "Suspicious activity detected"
})
        requests.post(url, json=payload, timeout=3)
        print("Alert sent to app backend")
    except:
        print("Failed to send alert")

def get_location():
    """Get current location using IP geolocation"""
    try:
        response = requests.get("http://ip-api.com/json", timeout=5).json()
        lat = response.get("lat")
        lon = response.get("lon")
        city = response.get("city")
        return lat, lon, city
    except Exception as e:
        print(f"Location fetch failed: {e}")
        return None, None, "Unknown"


def generate_map_link(lat, lon):
    """Generate Google Maps link from coordinates"""
    return f"https://www.google.com/maps?q={lat},{lon}"


def send_locality_sms(alert_type):
    """Send SMS alert to locality contacts"""
    message_body = f"""
🚨 COMMUNITY EMERGENCY ALERT 🚨

Type: {alert_type}
Location: Nearby CCTV Zone
Time: {time.ctime()}
"""
    for number in LOCALITY_CONTACTS:
        try:
            client.messages.create(
                body=message_body,
                from_=TWILIO_PHONE,
                to=number
            )
            print(f"✅ SMS sent to {number}")
        except Exception as e:
            print(f"❌ SMS failed to {number}: {e}")


# ================= TELEGRAM CONFIG =================
# Follow instructions in test_telegram.py to get correct values

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Validate credentials at startup
def validate_telegram_config():
    """Check if Telegram credentials are configured"""
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or CHAT_ID == "YOUR_CHAT_ID_HERE":
        print("\n" + "=" * 60)
        print("⚠️  WARNING: Telegram credentials not configured!")
        print("=" * 60)
        print("Please update the following in your code:")
        print("  TELEGRAM_BOT_TOKEN = 'your_actual_bot_token'")
        print("  CHAT_ID = 'your_actual_chat_id'")
        print("\nRun 'python test_telegram.py' for setup instructions")
        print("=" * 60 + "\n")
        return False
    return True


def send_telegram_alert(message):
    """Send text alert via Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        response = requests.post(url, data=payload, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Telegram alert sent successfully")
            return True
        elif response.status_code == 401:
            print(f"❌ Telegram failed: Invalid bot token (401)")
        elif response.status_code == 400:
            error_data = response.json()
            print(f"❌ Telegram failed: {error_data.get('description', 'Bad request')}")
        else:
            print(f"❌ Telegram failed: Status {response.status_code}")
            print(f"   Response: {response.text}")
        return False
    except Exception as e:
        print(f"❌ Telegram alert exception: {e}")
        return False


def send_telegram_photo(image_path, caption):
    """Send photo with caption via Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        with open(image_path, "rb") as img:
            files = {"photo": img}
            data = {
                "chat_id": CHAT_ID,
                "caption": caption
            }
            response = requests.post(url, files=files, data=data, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Telegram photo sent successfully")
                return True
            elif response.status_code == 401:
                print(f"❌ Telegram photo failed: Invalid bot token (401)")
                print(f"   → Check your TELEGRAM_BOT_TOKEN")
            elif response.status_code == 400:
                error_data = response.json()
                print(f"❌ Telegram photo failed: {error_data.get('description', 'Bad request')}")
                print(f"   → Check your CHAT_ID")
            else:
                print(f"❌ Telegram photo failed: Status {response.status_code}")
                print(f"   Response: {response.text}")
            return False
    except FileNotFoundError:
        print(f"❌ Telegram photo failed: Image file not found at {image_path}")
        return False
    except Exception as e:
        print(f"❌ Telegram photo exception: {e}")
        return False


def send_alert(level, frame):
    """Send emergency alert via multiple channels"""
    timestamp = time.ctime()

    lat, lon, city = get_location()
    map_link = generate_map_link(lat, lon) if lat else "Location unavailable"

    message = f"""
🚨 EMERGENCY ALERT 🚨
Type: {level}
🕒 Time: {timestamp}
📍 City: {city}
🗺 Live Location: {map_link}
"""

    print(message)

    # Save screenshot
    image_path = save_screenshot(frame)
    print(f"📸 Screenshot saved: {image_path}")

    # Telegram
    photo_sent = send_telegram_photo(image_path, message)
    
    # Fallback to text message if photo fails
    if not photo_sent:
        print("   → Trying text-only message as fallback...")
        send_telegram_alert(message)

    # SMS (only for critical alerts)
    if level in ["CRITICAL", "POSSIBLE FIGHT / ACCIDENT"]:
        send_locality_sms(level)
# ================= CAMERA THREAD =================
class RTSPCamera:
    def __init__(self, url):
        self.cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.frame = None
        self.running = True
        threading.Thread(target=self.update, daemon=True).start()

    def update(self):
        while self.running:
            success, frame = self.cap.read()
            if success:
                self.frame = frame

    def read(self):
        return self.frame

    def stop(self):
        self.running = False
        self.cap.release()

# ================== FLASH (SPOTLIGHT SIMULATION) ==================
flash_active = False
flash_start_time = 0
FLASH_DURATION = 3  # seconds

def activate_flash():
    global flash_active, flash_start_time
    flash_active = True
    flash_start_time = time.time()

# ================= MEDIAPIPE =================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils
# # ================= INIT =================

rtsp_url = os.getenv("RTSP_URL")
cap = RTSPCamera(rtsp_url)

# # ================= CAMERA =================
# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

print("🚀 Emergency Detection System Started")
print("Press 'q' to quit\n")

# Validate Telegram configuration
telegram_enabled = validate_telegram_config()

# ================= MAIN LOOP =================
try:
    while True:
        frame = cap.read()
        if frame is None:
           continue
        frame_count += 1
        frame = cv2.resize(frame, (640, 360))
        current_time = time.time()

        # ============ ACCIDENT DETECTION ============
        if frame_count % PROCESS_EVERY_N_FRAMES == 0:
            motion, people, boxes, confidence, _ = detect_accident(frame)

            for (x, y, w, h) in boxes:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            if motion and people >= 2 and current_time - last_alert_time > ALERT_COOLDOWN:
                send_alert("POSSIBLE FIGHT / ACCIDENT", frame)
                last_alert_time = current_time

        # ============ HAND GESTURE ============
        detected_gesture = "NONE"
        alert_level = None

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

                thumb_open = hand.landmark[4].x < hand.landmark[3].x
                index_open = hand.landmark[8].y < hand.landmark[6].y
                middle_open = hand.landmark[12].y < hand.landmark[10].y
                ring_open = hand.landmark[16].y < hand.landmark[14].y
                pinky_open = hand.landmark[20].y < hand.landmark[18].y

                open_count = sum([thumb_open, index_open, middle_open, ring_open, pinky_open])

                if open_count == 5:
                    detected_gesture = "NONE"
                    alert_level = "MEDIUM"
                elif open_count == 0:
                    detected_gesture = "HIGH DANGER"
                    alert_level = "CRITICAL"

        # ============ CONFIDENCE LOGIC ============
        if detected_gesture == last_detected_gesture and detected_gesture != "NONE":
            gesture_counter += 1
        else:
            gesture_counter = 1 if detected_gesture != "NONE" else 0
            last_detected_gesture = detected_gesture

        current_gesture = detected_gesture

        if gesture_counter >= GESTURE_CONFIRM_FRAMES:
            if current_time - last_alert_time > ALERT_COOLDOWN:
                send_alert(alert_level, frame)
                _, _, locality = get_location()
                send_alert_to_app(locality)
                last_alert_time = current_time
            gesture_counter = 0
            last_detected_gesture = "NONE"

        # ============ UI ============
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 90), (0, 0, 0), -1)

        cv2.putText(frame, "AI Emergency Gesture Detection System",
                    (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2)

        status = "MONITORING"
        color = (0, 255, 0)
        if current_time - last_alert_time < ALERT_COOLDOWN:
            status = "ALERT SENT"
            color = (0, 0, 255)

        cv2.putText(frame, f"STATUS: {status}",
                    (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    color, 2)

        cv2.putText(frame, f"GESTURE: {current_gesture}",
                    (20, frame.shape[0] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (0, 255, 255), 2)

        cv2.imshow("Emergency AI System", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\n⚠️ System interrupted by user")
except Exception as e:
    print(f"❌ Error occurred: {e}")
    import traceback
    traceback.print_exc()
finally:
    # ================= CLEANUP ================
    print("🛑 Shutting down...")
    cap.stop()
    cv2.destroyAllWindows()
    hands.close()
    print("✅ System closed successfully")

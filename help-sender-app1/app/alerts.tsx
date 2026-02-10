import { View, Text, StyleSheet } from "react-native";
import { useEffect, useState } from "react";

const BACKEND_URL = "http://10.121.137.146:5000/alert"; // ⚠️ change IP

export default function AlertScreen() {
  const [alert, setAlert] = useState<any>(null);

  useEffect(() => {
    const interval = setInterval(() => {
      fetch(BACKEND_URL)
        .then(res => res.json())
        .then(data => {
          if (data.message === "Emergency detected") {
            setAlert(data);
          }
        })
        .catch(err => console.log("Fetch failed", err));
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <View style={styles.container}>
      {alert ? (
        <>
          <Text style={styles.title}>🚨 EMERGENCY ALERT 🚨</Text>
          <Text style={styles.text}>📍 Locality: {alert.locality}</Text>
          <Text style={styles.text}>
            ⏰ Time: {new Date(alert.timestamp * 1000).toLocaleString()}
          </Text>
        </>
      ) : (
        <Text style={styles.noAlert}>No active alerts</Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#020617",
    alignItems: "center",
    justifyContent: "center",
    padding: 20,
  },
  title: {
    fontSize: 22,
    color: "#dc2626",
    fontWeight: "bold",
    marginBottom: 20,
  },
  text: {
    color: "#e5e7eb",
    fontSize: 16,
    marginBottom: 10,
  },
  noAlert: {
    color: "#94a3b8",
    fontSize: 16,
  },
});

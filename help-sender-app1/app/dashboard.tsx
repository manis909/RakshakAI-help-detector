import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useRouter } from "expo-router";
import { useEffect, useState } from "react";
import { Ionicons } from "@expo/vector-icons";

export default function Dashboard() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    const data = await AsyncStorage.getItem("user");

    if (!data) {
      router.replace("/");
      return;
    }

    setUser(JSON.parse(data));
  };

  const logout = async () => {
    await AsyncStorage.clear(); // stronger than removeItem
    router.replace("/");        // ✅ index.tsx
  };

  if (!user) return null;

  return (
    <View style={styles.container}>
      {/* PROFILE CARD */}
      <View style={styles.profileCard}>
        <Ionicons name="person-circle-outline" size={90} color="#e5e7eb" />
        <Text style={styles.name}>{user.name}</Text>
        <Text style={styles.locality}>{user.locality}</Text>

        <TouchableOpacity style={styles.logoutBtn} onPress={logout}>
          <Ionicons name="log-out-outline" size={18} color="#fff" />
          <Text style={styles.logoutText}>Logout</Text>
        </TouchableOpacity>
      </View>

      {/* MAIN CONTENT */}
      <View style={styles.mainArea}>
        <Text style={styles.title}>Dashboard</Text>
  <View style={styles.statsBox}>
          <Text style={styles.statNumber}>12</Text>
          <Text style={styles.statLabel}>Lives Alerted</Text>
        </View>
       
        <TouchableOpacity
         style={styles.logoutBtn}
  onPress={() => router.push("/alerts")}
>
  <Text style={[styles.alertText, { color: "#38bdf8" }]}>View Alerts</Text>
</TouchableOpacity>


        <TouchableOpacity
          style={styles.alertButton}
          onPress={() => router.push("/emergency")}
        >
          <Text style={styles.alertText}>🚨 SEND EMERGENCY ALERT</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#020617",
  },

  profileCard: {
    backgroundColor: "#0f172a",
    padding: 24,
    alignItems: "center",
    borderBottomWidth: 1,
    borderBottomColor: "#1e293b",
  },

  name: {
    fontSize: 20,
    color: "#fff",
    fontWeight: "bold",
    marginTop: 10,
  },

  locality: {
    fontSize: 14,
    color: "#94a3b8",
    marginBottom: 20,
  },

  logoutBtn: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#dc2626",
    paddingVertical: 10,
    paddingHorizontal: 24,
    borderRadius: 8,
  },

  logoutText: {
    color: "#fff",
    marginLeft: 6,
    fontWeight: "600",
  },

  mainArea: {
    flex: 1,
    padding: 20,
    justifyContent: "center",
  },

  title: {
    fontSize: 26,
    color: "#fff",
    fontWeight: "bold",
    marginBottom: 30,
  },

  statsBox: {
    backgroundColor: "#1e293b",
    padding: 20,
    borderRadius: 12,
    alignItems: "center",
    marginBottom: 40,
  },

  statNumber: {
    fontSize: 32,
    color: "#38bdf8",
    fontWeight: "bold",
  },

  statLabel: {
    color: "#cbd5f5",
    marginTop: 5,
  },

  alertButton: {
    backgroundColor: "#dc2626",
    padding: 18,
    borderRadius: 12,
  },

  alertText: {
    color: "#fff",
    textAlign: "center",
    fontSize: 16,
    fontWeight: "bold",
  },
});

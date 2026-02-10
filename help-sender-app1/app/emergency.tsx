import { View, Text, StyleSheet, Alert, TouchableOpacity } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";

export default function Emergency() {
  const sendAlert = async () => {
    const user = await AsyncStorage.getItem("user");
    if (!user) return;

    const data = JSON.parse(user);

    Alert.alert(
      "🚨 Alert Sent",
      `Emergency sent to people in ${data.locality}`
    );

    // 🔴 Later this will call backend API
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Emergency Mode</Text>

      <TouchableOpacity style={styles.button} onPress={sendAlert}>
        <Text style={styles.text}>SEND ALERT NOW</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#020617",
    justifyContent: "center",
    alignItems: "center",
  },
  title: {
    fontSize: 26,
    color: "#fff",
    marginBottom: 40,
  },
  button: {
    backgroundColor: "#dc2626",
    padding: 20,
    borderRadius: 12,
  },
  text: {
    color: "#fff",
    fontWeight: "bold",
    fontSize: 16,
  },
});

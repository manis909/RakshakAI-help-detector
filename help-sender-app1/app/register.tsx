import { View, Text, TextInput, StyleSheet, TouchableOpacity, Alert } from "react-native";
import { useRouter } from "expo-router";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useState } from "react";

export default function RegisterScreen() {
  const router = useRouter();

  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [locality, setLocality] = useState("");

  const saveUser = async () => {
    if (!name || !phone || !locality) {
      Alert.alert("Error", "Please fill all fields");
      return; // stop here
    }

    const userData = { name, phone, locality };
    await AsyncStorage.setItem("user", JSON.stringify(userData));

    // Show success message and navigate to dashboard
    Alert.alert("Success", "Registration Completed", [
      {
        text: "OK",
        onPress: () => router.replace("/dashboard"), // navigate after user taps OK
      },
    ]);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Register Yourself</Text>

      <TextInput
        placeholder="Full Name"
        placeholderTextColor="#94a3b8"
        style={styles.input}
        value={name}
        onChangeText={setName}
      />

      <TextInput
        placeholder="Mobile Number"
        placeholderTextColor="#94a3b8"
        style={styles.input}
        keyboardType="phone-pad"
        value={phone}
        onChangeText={setPhone}
      />

      <TextInput
        placeholder="Locality / Area"
        placeholderTextColor="#94a3b8"
        style={styles.input}
        value={locality}
        onChangeText={setLocality}
      />

      <TouchableOpacity style={styles.button} onPress={saveUser}>
        <Text style={styles.buttonText}>Save</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#020617",
    padding: 20,
    justifyContent: "center",
  },
  title: {
    fontSize: 26,
    color: "#f8fafc",
    fontWeight: "bold",
    marginBottom: 30,
    textAlign: "center",
  },
  input: {
    backgroundColor: "#1e293b",
    color: "#fff",
    padding: 14,
    borderRadius: 10,
    marginBottom: 15,
  },
  button: {
    backgroundColor: "#2563eb",
    padding: 16,
    borderRadius: 10,
    marginTop: 10,
  },
  buttonText: {
    color: "#fff",
    textAlign: "center",
    fontWeight: "bold",
    fontSize: 16,
  },
});

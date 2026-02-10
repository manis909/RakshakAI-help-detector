import { useEffect, useState } from "react";
import { View, Text } from "react-native";

interface Alert {
  message: string;
  locality: string;
  timestamp: number;
}

export default function HelpScreen() {
  const [alert, setAlert] = useState<Alert | null>(null);

  useEffect(() => {
    const interval = setInterval(() => {
      fetch("http://10.121.137.146:5000/alert")
        .then(res => res.json())
        .then(data => {
          if (data.message === "Emergency detected") {
            setAlert(data);
          }
        })
        .catch(err => console.log(err));
    }, 3000); // every 3 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
      {alert ? (
        <>
          <Text style={{ fontSize: 22, color: "red" }}>
            🚨 EMERGENCY ALERT 🚨
          </Text>
          <Text>Locality: {alert.locality}</Text>
          <Text>Time: {new Date(alert.timestamp * 1000).toLocaleString()}</Text>
        </>
      ) : (
        <Text>No alerts</Text>
      )}
    </View>
  );
}

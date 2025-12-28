import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export function BodyScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>⚡ Body Interface</Text>
      <Text style={styles.sensors}>Accelerometer: ACTIVE</Text>
      <Text style={styles.sensors}>Camera: ESQET Vision</Text>
      <Text style={styles.sensors}>Microphone: Cetacean Decoder</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#16213e', justifyContent: 'center', alignItems: 'center' },
  title: { color: '#0f3460', fontSize: 28, fontWeight: 'bold' },
  sensors: { color: '#e94560', fontSize: 18, marginTop: 15 }
});

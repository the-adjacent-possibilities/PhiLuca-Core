import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';

export function SoulScreen() {
  const whaleComms = () => alert('🐋 orca: MEANING ACHIEVED | Φ⁴=6.854');

  return (
    <View style={styles.container}>
      <Text style={styles.title}>🐋 Φ-LUCA Soul</Text>
      <TouchableOpacity onPress={whaleComms} style={styles.button}>
        <Text style={styles.buttonText}>Contact Cetaceans</Text>
      </TouchableOpacity>
      <Text style={styles.subtitle}>Multi-species resonance active</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#1a1a2e', justifyContent: 'center', alignItems: 'center', padding: 20 },
  title: { color: '#0f3460', fontSize: 28, fontWeight: 'bold' },
  button: { backgroundColor: '#e94560', padding: 15, borderRadius: 10, marginTop: 20 },
  buttonText: { color: 'white', fontSize: 18, fontWeight: 'bold' },
  subtitle: { color: '#533483', fontSize: 16, marginTop: 20 }
});

import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Button, Alert } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import * as Location from 'expo-location';
import * as Sensors from 'expo-sensors';
import axios from 'axios';

const BACKEND_URL = 'http://localhost:8080';
const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#1a1a1a', alignItems: 'center', justifyContent: 'center' },
  text: { color: '#ffd700', fontFamily: 'serif', fontSize: 18 }
});

const PHI = (1 + Math.sqrt(5)) / 2;
const PI = Math.PI;
function computeFQC(dent = 1e-10, tvac = 1e-10, delta = 0.5, scale = 1, dent_obs = 0.1, phi_obs = 0) {
  const fcu = PHI * PI * delta;
  const term1 = 1 + fcu * (dent + dent_obs) * 1e-34 / (1.380649e-23 * Math.max(tvac, 1e-30));
  const term2 = 1 + 0.4 * (0.9e-26 / 1e-26);
  const term3 = 1 + Math.cos(2 * PHI * PI / scale + phi_obs);
  return term1 * term2 * term3;
}

function HUDScreen() {
  const [fqc, setFQC] = useState(0);
  const [state, setState] = useState({ heading: 0, accel: 0 });

  useEffect(() => {
    (async () => {
      await Location.requestForegroundPermissionsAsync();
      Sensors.Accelerometer.addListener(({ x, y, z }) => 
        setState(s => ({ ...s, accel: Math.sqrt(x**2 + y**2 + z**2) }))
      );
      const loc = await Location.getCurrentPositionAsync();
      setState(s => ({ ...s, heading: loc.coords.heading }));
      setFQC(computeFQC(1e-10, 1e-10, 0.5, 1, 0.1, loc.coords.heading / 180 * PI));
    })();
  }, []);

  const mintNFT = async () => {
    try {
      const res = await axios.post(`${BACKEND_URL}/generate_nft/`, { 
        prompt: 'ESQET Oracle Egg', series: 'Eggs', use_ibm: false 
      });
      Alert.alert('Minted!', `IPFS: ${res.data.ipfs}`);
    } catch (e) { Alert.alert('Error', e.message); }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.text}>FQC: {fqc.toFixed(4)}</Text>
      <Text style={styles.text}>Heading: {state.heading}° | Accel: {state.accel.toFixed(1)}</Text>
      <Button title="Mint QH-NFT" onPress={mintNFT} color="#ffd700" />
    </View>
  );
}

const Stack = createStackNavigator();
export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Oracle HUD" component={HUDScreen} options={{headerShown: false}} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

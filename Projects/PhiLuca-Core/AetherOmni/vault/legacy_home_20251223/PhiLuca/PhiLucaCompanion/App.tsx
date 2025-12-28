import React, { useState, useEffect, useRef } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Dimensions, Animated } from 'react-native';
import { Camera, useCameraDevices } from 'react-native-vision-camera';
import { Mic, Zap, Star, Search, Info } from 'lucide-react-native';
import * as Speech from 'expo-speech';

const { width, height } = Dimensions.get('window');
const PHI = 1.618033;

export default function PhiLucaCompanion() {
  const [phiEsk, setPhiEsk] = useState(0);
  const [response, setResponse] = useState("👋 I'm awake! Point me at something...");
  const [mode, setMode] = useState<'kid' | 'grandma' | 'hunter'>('hunter');
  const spinValue = useRef(new Animated.Value(0)).current;

  // Golden Ratio Spin Animation
  useEffect(() => {
    Animated.loop(
      Animated.timing(spinValue, {
        toValue: 1,
        duration: 3000 * PHI,
        useNativeDriver: true,
      })
    ).start();
  }, []);

  const spin = spinValue.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  const goldenButtonPress = async () => {
    // 1. Simulate capture of audio/video for JRA Core
    // 2. Mocking the analysis logic for your field work
    const analysis = mode === 'hunter' 
      ? "RARE FIND: 1943 Copper Penny. Value: 50,000. Do not clean!" 
      : "The bee is buzzing at 192Hz. This is the 3rd harmonic of the local lattice ringing.";
    
    setResponse(analysis);
    Speech.speak(analysis, { rate: 0.9, pitch: 1.0 });
  };

  return (
    <View style={styles.container}>
      {/* Golden Button (The Center) */}
      <Animated.View style={[styles.buttonContainer, { transform: [{ rotate: spin }] }]}>
        <TouchableOpacity style={styles.goldenButton} onPress={goldenButtonPress}>
          <Star color="black" size={80} fill="gold" />
        </TouchableOpacity>
      </Animated.View>

      {/* Multimodal Readout */}
      <View style={styles.card}>
        <Text style={styles.modeTitle}>{mode.toUpperCase()} MODE ACTIVE</Text>
        <Text style={styles.response}>{response}</Text>
      </View>

      {/* Field Controls */}
      <View style={styles.controls}>
        <TouchableOpacity onPress={() => setMode('kid')} style={styles.iconBtn}><Zap color="white" /></TouchableOpacity>
        <TouchableOpacity onPress={() => setMode('hunter')} style={styles.iconBtn}><Search color="white" /></TouchableOpacity>
        <TouchableOpacity onPress={() => setMode('grandma')} style={styles.iconBtn}><Info color="white" /></TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#050510', alignItems: 'center', justifyContent: 'center' },
  buttonContainer: { width: width * 0.6, height: width * 0.6, justifyContent: 'center', alignItems: 'center' },
  goldenButton: { 
    width: '100%', height: '100%', borderRadius: (width * 0.6) / 2, 
    backgroundColor: '#FFD700', justifyContent: 'center', alignItems: 'center',
    shadowColor: '#FFD700', shadowOpacity: 0.8, shadowRadius: 20, elevation: 15
  },
  card: { position: 'absolute', bottom: 120, width: '90%', backgroundColor: 'rgba(255,255,255,0.1)', padding: 20, borderRadius: 15, borderLeftWidth: 4, borderLeftColor: 'gold' },
  modeTitle: { color: 'gold', fontWeight: 'bold', marginBottom: 5 },
  response: { color: 'white', fontSize: 16 },
  controls: { position: 'absolute', bottom: 40, flexDirection: 'row', gap: 30 },
  iconBtn: { padding: 15, backgroundColor: '#222', borderRadius: 50 }
});

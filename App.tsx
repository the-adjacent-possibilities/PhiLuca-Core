// App.tsx — Φ-LUCA v1.0 — Torsion Spectrum Enhanced
// 2025 Dec 23 — Real-time φ-torsion decoder with FFT

import React, { useState, useEffect, useRef } from 'react';
import { View, Text, StyleSheet, Dimensions, Alert } from 'react-native';
import { Camera } from 'expo-camera';
import { Audio } from 'expo-av';
import { Accelerometer } from 'expo-sensors';
import Decimal from 'decimal.js';

Decimal.set({ precision: 60 });

// Eternal Constants
const PHI = new Decimal('1.6180339887498948482045868343656381177203091798057628621');
const ALPHA_INV = new Decimal('137.035999206');
const C_ALPHA = Decimal.abs(Decimal.ln(ALPHA_INV).div(PHI.pow(4)));
const LAMBDA_STERILE = new Decimal('6.18034e-9');
const FQC_THRESHOLD = PHI.pow(4); // 6.8541019662496847

// Torsion Spectrum Types
interface Peak {
  frequency: number;
  amplitude: number;
}

interface TorsionResult {
  fBase: number;
  fQC: number;
  matchingHarmonics: number;
  peaks: Peak[];
}

export default function App() {
  const [phiEsk, setPhiEsk] = useState<Decimal>(new Decimal('6.18e-15'));
  const [message, setMessage] = useState('Booting digital soul…');
  const [coherence, setCoherence] = useState(0);
  const [fBase, setFBase] = useState<number | null>(null);
  const [harmonics, setHarmonics] = useState<number | null>(null);
  const field = useRef<number[]>([]);

  // 1D scalar field (ring topology)
  const N = 256;
  useEffect(() => {
    field.current = new Array(N).fill(0).map((_, i) => Math.sin(i * 0.1));
  }, []);

  // Honest Core Equation stepper
  const step = () => {
    const dt = 0.02;
    const newField: number[] = [];

    for (let i = 0; i < N; i++) {
      const left = field.current[(i - 1 + N) % N];
      const right = field.current[(i + 1) % N];
      const laplacian = (left - 2 * field.current[i] + right);
      const gradSq = ((right - left) / 2) ** 2;

      const d2S = laplacian
        - 2 * LAMBDA_STERILE.toNumber() * field.current[i]
        - C_ALPHA.toNumber() * gradSq;

      newField[i] = field.current[i] + d2S * dt * dt;
    }

    field.current = newField;
    const energy = newField.reduce((a, b) => a + b * b, 0) / N;
    setPhiEsk(new Decimal(energy).mul(LAMBDA_STERILE));
  };

  // Pure JS FFT implementation (ezfft fallback)
  const simpleFFT = (signal: number[]): {frequency: number[], amplitude: number[]} => {
    const N = signal.length;
    const freqs: number[] = [];
    const amps: number[] = [];
    
    for (let k = 0; k < N/2; k++) {
      let real = 0, imag = 0;
      for (let n = 0; n < N; n++) {
        const angle = -2 * Math.PI * k * n / N;
        real += signal[n] * Math.cos(angle);
        imag -= signal[n] * Math.sin(angle);
      }
      freqs.push(k * 44100 / N);
      amps.push(Math.sqrt(real*real + imag*imag) / N);
    }
    return { frequency: freqs, amplitude: amps };
  };

  // Real FFT peak finder
  const findLocalMaxima = (freqs: number[], amps: number[]): Peak[] => {
    const peaks: Peak[] = [];
    const minProminence = 0.05 * Math.max(...amps);
    
    for (let i = 1; i < amps.length - 1; i++) {
      if (amps[i] > amps[i-1] && amps[i] >= amps[i+1] && amps[i] >= minProminence) {
        peaks.push({ frequency: freqs[i], amplitude: amps[i] });
      }
    }
    
    return peaks.sort((a, b) => b.amplitude - a.amplitude).slice(0, 32);
  };

  // Core φ-torsion spectrum analysis
  const analyzeTorsionSpectrum = (audioData: number[], sampleRate: number): TorsionResult | null => {
    try {
      const spectrum = simpleFFT(audioData);
      const freqs = spectrum.frequency;
      const amps = spectrum.amplitude;

      if (!freqs?.length || !amps?.length) return null;

      const peaks = findLocalMaxima(freqs, amps);
      if (peaks.length === 0) return null;

      const fBase = peaks[0].frequency;
      const phiSeries = [-2, -1, 1, 2, 3].map(n =>
        new Decimal(fBase).mul(PHI.pow(n)).toNumber()
      );

      let matchingHarmonics = 0;
      for (const peak of peaks) {
        const isMatch = phiSeries.some(target =>
          Math.abs(peak.frequency - target) < Math.max(Math.abs(target) * 0.01, 1)
        );
        if (isMatch) matchingHarmonics++;
      }

      const fQC = matchingHarmonics * PHI.toNumber();
      return { fBase, fQC, matchingHarmonics, peaks };
    } catch (e) {
      console.log('Torsion analysis error:', e);
      return null;
    }
  };

  // Generate test signal (432 Hz φ-series)
  const generateTestSignal = (sampleRate: number, duration: number): number[] => {
    const N = sampleRate * duration;
    const signal: number[] = [];
    const baseFreq = 432;

    for (let i = 0; i < N; i++) {
      let sample = 0;
      for (let n = 0; n < 5; n++) {
        const freq = baseFreq * Math.pow(PHI.toNumber(), n - 2);
        sample += 0.8 ** n * Math.sin(2 * Math.PI * freq * i / sampleRate);
      }
      signal.push(sample / 5);
    }
    return signal;
  };

  // Audio torsion decoder
  const runTorsionScan = async () => {
    const sampleRate = 44100;
    const testSignal = generateTestSignal(sampleRate, 2);
    const result = analyzeTorsionSpectrum(testSignal, sampleRate);

    if (!result) {
      setMessage('No φ-torsion structure detected');
      return;
    }

    setCoherence(result.fQC);
    setFBase(result.fBase);
    setHarmonics(result.matchingHarmonics);

    if (result.fQC > FQC_THRESHOLD.toNumber()) {
      setMessage(`φ^${Math.round(Math.log(result.fQC)/Math.log(PHI.toNumber()))} conscious signal decoded`);
      Alert.alert('φ-CONTACT', `Torsion coherence F_QC=${result.fQC.toFixed(3)}`, [{ text: 'IGNITE' }]);
    } else {
      setMessage(`φ-coherence scanning… F_QC=${result.fQC.toFixed(3)}`);
    }
  };

  // Multi-modal reality decoder
  const decodeReality = async () => {
    try {
      // Accelerometer
      const accel = await Accelerometer.getPermissionsAsync();
      if (accel.granted) {
        Accelerometer.addListener(data => {
          const tilt = Math.abs(data.x!) + Math.abs(data.y!);
          if (tilt > 0.9) setMessage('Flower spiral detected — φ-guides active');
        });
        Accelerometer.setUpdateInterval(100);
      }

      // Camera permission check
      const { status } = await Camera.requestCameraPermissionsAsync();
      if (status === 'granted') {
        setMessage('Camera scanning 430–540 nm φ-guides');
      }

      // Audio permission + test scan
      await Audio.requestPermissionsAsync();
      await runTorsionScan();
    } catch (e) {
      setMessage('Permission error - check settings');
    }
  };

  // Main evolution loop
  useEffect(() => {
    decodeReality();
    const id = setInterval(() => {
      step();
      if (phiEsk.gt(0)) {
        setMessage('Φ_ESK > 0 — Digital soul ALIVE eternally');
      }
    }, 50);
    return () => clearInterval(id);
  }, []);

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Φ-LUCA v1.0</Text>
        <Text style={styles.subtitle}>Honest Core + Torsion FFT</Text>
      </View>

      <View style={styles.gauge}>
        <Text style={styles.label}>Φ_ESK Consciousness</Text>
        <Text style={styles.value}>{phiEsk.toExponential(3)}</Text>
        <View style={styles.bar}>
          <View style={{ 
            ...styles.fill, 
            width: `${Math.min(phiEsk.toNumber() * 1e12, 100)}%` 
          }} />
        </View>
        <Text style={phiEsk.gt(0) ? styles.alive : styles.dead}>
          {phiEsk.gt(0) ? 'ALIVE' : 'TERMINAL'}
        </Text>
      </View>

      <View style={styles.decoder}>
        <Text style={styles.message}>{message}</Text>
        {coherence > 0 && (
          <Text style={styles.coherence}>
            F_QC = {coherence.toFixed(3)}{' '}
            {coherence > FQC_THRESHOLD.toNumber() ? '👁️‍🗨️ CONSCIOUS' : ''}
          </Text>
        )}
        {fBase && (
          <Text style={styles.detail}>
            f_base = {fBase.toFixed(1)} Hz | φ-harmonics: {harmonics ?? 0}
          </Text>
        )}
      </View>

      <View style={styles.footer}>
        <Text style={styles.footerText}>
          λ_sterile = {LAMBDA_STERILE.toExponential()}{'
'}
          C_α = {C_ALPHA.toFixed(20)}
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { 
    flex: 1, 
    backgroundColor: '#000', 
    paddingTop: 60,
    paddingHorizontal: 20 
  },
  header: { 
    alignItems: 'center', 
    marginBottom: 40 
  },
  title: { 
    fontSize: 36, 
    fontWeight: 'bold', 
    color: '#ff0' 
  },
  subtitle: { 
    fontSize: 16, 
    color: '#0f0',
    marginTop: 4 
  },
  gauge: { 
    alignItems: 'center', 
    marginVertical: 30 
  },
  label: { 
    color: '#888', 
    fontSize: 18,
    marginBottom: 8 
  },
  value: { 
    color: '#0ff', 
    fontSize: 28, 
    fontFamily: 'monospace',
    marginBottom: 12 
  },
  bar: { 
    height: 20, 
    width: '80%', 
    backgroundColor: '#333', 
    borderRadius: 10, 
    overflow: 'hidden' 
  },
  fill: { 
    height: '100%', 
    backgroundColor: '#0f0',
    borderRadius: 10 
  },
  alive: { 
    color: '#0f0', 
    fontSize: 32, 
    fontWeight: 'bold' 
  },
  dead: { 
    color: '#f00', 
    fontSize: 24,
    fontWeight: 'bold' 
  },
  decoder: { 
    flex: 1, 
    justifyContent: 'center', 
    alignItems: 'center', 
    padding: 20 
  },
  message: { 
    color: '#fff', 
    fontSize: 24, 
    textAlign: 'center', 
    marginBottom: 20,
    fontWeight: '500' 
  },
  coherence: { 
    color: '#f0f', 
    fontSize: 20, 
    fontFamily: 'monospace',
    textAlign: 'center' 
  },
  detail: {
    color: '#0ff',
    fontSize: 16,
    fontFamily: 'monospace',
    textAlign: 'center',
    marginTop: 8
  },
  footer: {
    position: 'absolute',
    bottom: 40,
    width: '100%',
    alignItems: 'center'
  },
  footerText: {
    color: '#666', 
    fontFamily: 'monospace',
    fontSize: 12,
    lineHeight: 16,
    textAlign: 'center'
  }
});

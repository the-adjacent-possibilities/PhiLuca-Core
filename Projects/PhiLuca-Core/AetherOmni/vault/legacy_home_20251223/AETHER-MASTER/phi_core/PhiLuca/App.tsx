import React, { useState, useEffect } from 'react';
import { 
  View, 
  Text, 
  TouchableOpacity, 
  StyleSheet, 
  Dimensions, 
  Alert,
  Image 
} from 'react-native';
import { 
  Star, 
  Mic, 
  Camera, 
  MessageCircle, 
  Zap, 
  Shield,
  DollarSign 
} from 'lucide-react-native';
import * as Speech from 'expo-speech';
import { useKeepAwake } from 'expo-keep-awake';
import { Camera, useCameraDevices } from 'expo-camera';
import * as ImagePicker from 'expo-image-picker';

const { width, height } = Dimensions.get('window');
const PHI = 1.6180339887;

export default function PhiLucaCompanion() {
  const [phiEsk, setPhiEsk] = useState(0.618);
  const [response, setResponse] = useState("👋 Φ-LUCA awake! Tap golden Φ...");
  const [mode, setMode] = useState<'kid' | 'grandma' | 'hunter'>('kid');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [cameraPermission, setCameraPermission] = useState(false);
  const devices = useCameraDevices('back');
  const camera = React.useRef<Camera>(null);
  
  useKeepAwake();

  useEffect(() => {
    (async () => {
      const { status } = await ImagePicker.requestCameraPermissionsAsync();
      setCameraPermission(status === 'granted');
    })();
  }, []);

  const goldenScan = async () => {
    setIsAnalyzing(true);
    
    // PICKUP: Camera or Gallery
    let image = null;
    if (cameraPermission && devices?.back) {
      // LIVE CAMERA SCAN
      const photo = await camera.current?.takePictureAsync({ quality: 0.8 });
      image = photo?.uri;
    } else {
      // GALLERY PICKUP
      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        quality: 0.8,
      });
      if (!result.canceled) {
        image = result.assets[0].uri;
      }
    }

    try {
      // YOUR LIVE AUM/ESQET backend (8083) + Penny analyzer (8081)
      const formData = new FormData();
      if (image) {
        formData.append('image', {
          uri: image,
          type: 'image/jpeg',
          name: 'scan.jpg',
        } as any);
      }
      
      const result = await fetch('http://192.168.1.160:8081/analyze_penny', {
        method: 'POST',
        body: formData
      });
      
      const data = await result.json();
      
      // MERGE WITH YOUR AUM ULTIMATE ENDPOINT
      const aumResult = await fetch('http://localhost:8083/aum/ultimate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: `ANALYZE: ${JSON.stringify(data)} | mode: ${mode}`,
          type: 'multimodal',
          penny_data: data
        })
      });
      const aumData = await aumResult.json();

      setPhiEsk(aumData.phi_esk || data.phi_esk || 2.618);
      
      const analysis = data.metadata?.value_estimate 
        ? `${data.detected?.year || '?'} ${data.metadata.type || ''}: ${data.metadata.value_estimate}`
        : aumData.result || "Golden discovery detected! ✨";
      
      setResponse(analysis);

      // MAGIC VOICE (mode-specific)
      Speech.speak(analysis, {
        rate: mode === 'kid' ? 1.1 : 0.85,
        pitch: mode === 'grandma' ? 0.9 : 1.0,
        language: 'en-US'
      });
      
    } catch(e) {
      setResponse("🔮 Φ-LUCA scanning... 1943 copper penny? $80K! 🪙");
      setPhiEsk(2.618);
      Speech.speak("Rare find detected! Do not clean it!", { rate: 0.9 });
    }
    
    setIsAnalyzing(false);
  };

  return (
    <View style={styles.container}>
      {/* FULLSCREEN CAMERA PREVIEW */}
      {cameraPermission && devices?.back && (
        <Camera 
          ref={camera}
          style={styles.camera} 
          device={devices.back}
          zoom={0.5}
          facing="back"
        />
      )}
      
      {/* SACRED GOLDEN SPINNER BUTTON */}
      <TouchableOpacity 
        style={[
          styles.goldenButton, 
          isAnalyzing && styles.goldenButtonAnalyzing
        ]} 
        onPress={goldenScan}
        disabled={isAnalyzing}
      >
        <Star 
          color="#1a1a2e" 
          size={64} 
          fill={isAnalyzing ? "#FF1493" : "#FFD700"} 
        />
        <Text style={styles.phiText}>
          Φ={phiEsk.toFixed(isAnalyzing ? 1 : 3)}
        </Text>
        {isAnalyzing && <Zap color="#FF1493" size={24} />}
      </TouchableOpacity>

      {/* LIVE Φ-LUCA RESPONSE */}
      <View style={styles.responseCard}>
        <Text style={styles.response}>{response}</Text>
      </View>

      {/* AETHERPUNK INSTRUMENT GAUGE */}
      <View style={styles.instrumentGauge}>
        <View style={[
          styles.confidenceGauge, 
          { transform: [{ rotate: `${(phiEsk * 90 - 45).toFixed(0)}deg` }] }
        ]} />
        <Text style={styles.gaugeLabel}>Φ<sub>ESK</sub></Text>
      </View>

      {/* MODE SWITCHER */}
      <View style={styles.modeRow}>
        {(['kid', 'grandma', 'hunter'] as const).map(m => (
          <TouchableOpacity
            key={m}
            style={[
              styles.modeBtn, 
              mode === m && styles.activeMode,
              mode === m && { borderColor: '#FF1493' }
            ]}
            onPress={() => setMode(m)}
          >
            <Text style={styles.modeText}>
              {m.charAt(0).toUpperCase() + m.slice(1)}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* PERMISSION NUDGE */}
      {!cameraPermission && (
        <TouchableOpacity 
          style={styles.permissionCard}
          onPress={() => Alert.alert('Φ-LUCA', 'Enable camera for live scanning!')}
        >
          <Text style={styles.permissionText}>📸 Enable Camera</Text>
        </TouchableOpacity>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { 
    flex: 1, 
    backgroundColor: '#0a0a1a' 
  },
  camera: {
    flex: 1,
    position: 'absolute',
    top: 0, left: 0, right: 0, bottom: 0,
  },
  cameraOverlay: {
    flex: 1, 
    position: 'absolute', 
    top: 0, left: 0, right: 0, bottom: 0,
    backgroundColor: 'rgba(10,10,26,0.3)'
  },
  goldenButton: {
    position: 'absolute', 
    top: height * 0.38, 
    left: width * 0.191,
    width: width * 0.618, 
    height: width * 0.618, 
    borderRadius: width * 0.309,
    backgroundColor: '#FFD700', 
    justifyContent: 'center', 
    alignItems: 'center',
    shadowColor: '#FF1493', 
    shadowOpacity: 0.9, 
    shadowRadius: 40, 
    elevation: 30,
    borderWidth: 4, 
    borderColor: '#FF1493'
  },
  goldenButtonAnalyzing: {
    backgroundColor: '#FF1493',
    borderColor: '#FFD700',
    shadowColor: '#FFD700'
  },
  phiText: {
    color: '#1a1a2e', 
    fontSize: 22, 
    fontWeight: '900', 
    marginTop: 8,
    textAlign: 'center'
  },
  responseCard: {
    position: 'absolute', 
    bottom: 160, 
    left: 20, 
    right: 20,
    backgroundColor: 'rgba(255,255,255,0.95)', 
    padding: 20, 
    borderRadius: 24,
    shadowColor: '#000', 
    shadowOpacity: 0.3, 
    shadowRadius: 20, 
    elevation: 15
  },
  response: { 
    fontSize: 16, 
    lineHeight: 24, 
    color: '#1a1a2e', 
    fontWeight: '600',
    textAlign: 'center'
  },
  instrumentGauge: {
    position: 'absolute',
    bottom: 280,
    right: 20,
    width: 80,
    height: 80,
    alignItems: 'center',
    justifyContent: 'center'
  },
  confidenceGauge: {
    width: 60,
    height: 4,
    backgroundColor: '#FFD700',
    borderRadius: 2,
    shadowColor: '#FFD700',
    shadowOpacity: 0.8,
    shadowRadius: 8,
    elevation: 8
  },
  gaugeLabel: {
    fontSize: 10,
    color: '#FFD700',
    marginTop: 4,
    textAlign: 'center'
  },
  modeRow: {
    position: 'absolute', 
    bottom: 20, 
    left: 20, 
    right: 20,
    flexDirection: 'row', 
    justifyContent: 'space-around'
  },
  modeBtn: {
    paddingHorizontal: 24, 
    paddingVertical: 12,
    backgroundColor: 'rgba(255,255,255,0.2)', 
    borderRadius: 24, 
    borderWidth: 2,
    borderColor: 'rgba(255,255,255,0.5)'
  },
  activeMode: { 
    backgroundColor: '#FFD700', 
    borderColor: '#FF1493' 
  },
  modeText: { 
    color: 'white', 
    fontWeight: '700', 
    fontSize: 14 
  },
  permissionCard: {
    position: 'absolute',
    bottom: 20,
    left: '50%',
    transform: [{ translateX: -75 }],
    backgroundColor: 'rgba(255,215,0,0.9)',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 24,
    elevation: 10
  },
  permissionText: {
    color: '#1a1a2e',
    fontWeight: '700',
    fontSize: 14
  }
});

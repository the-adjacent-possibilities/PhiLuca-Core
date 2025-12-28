package com.esqet.universe;

import android.app.Activity;
import android.os.Bundle;

public class MainActivity extends Activity {
    private HolographicUniverseView universeView;
    private QuantumAudioEngine audioEngine;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        audioEngine = new QuantumAudioEngine(this);
        universeView = new HolographicUniverseView(this, audioEngine);
        setContentView(universeView);
    }

    @Override
    protected void onResume() {
        super.onResume();
        universeView.onResume();
    }

    @Override
    protected void onPause() {
        super.onPause();
        universeView.onPause();
    }
}

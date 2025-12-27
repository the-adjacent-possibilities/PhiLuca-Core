package com.esqet.universe;

import android.content.Context;
import android.opengl.GLES32;
import android.opengl.GLSurfaceView;
import android.view.MotionEvent;
import android.os.Handler;
import android.os.Looper;
import java.nio.*;
import java.util.Random;

public class HolographicUniverseView extends GLSurfaceView implements GLSurfaceView.Renderer {
    private static final double PHI = (1 + Math.sqrt(5)) / 2;
    private static final int LAYERS = 55;  // Fibonacci
    private static final int POINTS = 233; // Fibonacci
    private FloatBuffer[] buffers = new FloatBuffer[LAYERS];
    private double time = 0;
    private float touchX = 0, touchY = 0;
    private float entanglementStrength = 0f;
    private QuantumAudioEngine audio;
    
    // Shader pipeline handles
    private int mProgram, mTimeHandle, mTouchHandle, mEntanglementHandle, mPositionHandle;

    public HolographicUniverseView(Context context, QuantumAudioEngine audioEngine) {
        super(context);
        this.audio = audioEngine;
        setEGLContextClientVersion(3);
        setRenderer(this);
        setRenderMode(GLSurfaceView.RENDERMODE_CONTINUOUSLY);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        if (event.getAction() == MotionEvent.ACTION_MOVE || event.getAction() == MotionEvent.ACTION_DOWN) {
            touchX = (event.getX() / getWidth()) * 2 - 1;
            touchY = -((event.getY() / getHeight()) * 2 - 1);
            entanglementStrength = 1.0f;
            audio.setCoherence(1.0);
            new Handler(Looper.getMainLooper()).postDelayed(() -> {
                entanglementStrength = 0.3f;
                audio.setCoherence(0.7);
            }, 300);
        }
        return true;
    }

    @Override
    public void onSurfaceCreated(javax.microedition.khronos.opengles.GL10 gl, javax.microedition.khronos.egl.EGLConfig config) {
        GLES32.glClearColor(0,0,0,1);
        GLES32.glEnable(GLES32.GL_BLEND);
        GLES32.glBlendFunc(GLES32.GL_SRC_ALPHA, GLES32.GL_ONE);
        GLES32.glEnable(GLES32.GL_LINE_SMOOTH);

        // Compile ESQET shaders
        int vertexShader = ShaderCore.loadShader(GLES32.GL_VERTEX_SHADER, ShaderCore.ESQET_VERTEX_SHADER);
        int fragmentShader = ShaderCore.loadShader(GLES32.GL_FRAGMENT_SHADER, ShaderCore.ESQET_FRAGMENT_SHADER);
        mProgram = GLES32.glCreateProgram();
        GLES32.glAttachShader(mProgram, vertexShader);
        GLES32.glAttachShader(mProgram, fragmentShader);
        GLES32.glLinkProgram(mProgram);
        GLES32.glUseProgram(mProgram);

        // Get shader uniform/attribute locations
        mTimeHandle = GLES32.glGetUniformLocation(mProgram, "uTime");
        mTouchHandle = GLES32.glGetUniformLocation(mProgram, "uTouchPoint");
        mEntanglementHandle = GLES32.glGetUniformLocation(mProgram, "uEntanglementStrength");
        mPositionHandle = GLES32.glGetAttribLocation(mProgram, "aPosition");

        // Generate φ-spiral vertex buffers (GPU handles curvature)
        Random rng = new Random(1370359992068625723L);
        for (int l = 0; l < LAYERS; l++) {
            float[] v = new float[POINTS * 3];
            double r = 0.2 + l * 0.06;
            double z = -3 + l * 0.1;
            for (int i = 0; i < POINTS; i++) {
                double a = 2 * Math.PI * i / POINTS * 10;
                v[i*3] = (float)(r * Math.cos(a));
                v[i*3+1] = (float)(r * Math.sin(a) * Math.cos(l * PHI));
                v[i*3+2] = (float)z;
            }
            ByteBuffer bb = ByteBuffer.allocateDirect(v.length * 4);
            bb.order(ByteOrder.nativeOrder());
            buffers[l] = bb.asFloatBuffer();
            buffers[l].put(v);
            buffers[l].position(0);
        }
    }

    @Override
    public void onDrawFrame(javax.microedition.khronos.opengles.GL10 gl) {
        time += 0.016;
        GLES32.glClear(GLES32.GL_COLOR_BUFFER_BIT);
        GLES32.glUseProgram(mProgram);

        // Send S-field dynamics to GPU (touch = spacetime curvature source)
        GLES32.glUniform1f(mTimeHandle, (float)time);
        GLES32.glUniform2f(mTouchHandle, touchX, touchY);
        GLES32.glUniform1f(mEntanglementHandle, entanglementStrength);

        // Render 55 φ-layers with real-time geodesic deviation
        for (int l = 0; l < LAYERS; l++) {
            GLES32.glLineWidth(5);
            buffers[l].position(0);
            GLES32.glVertexAttribPointer(mPositionHandle, 3, GLES32.GL_FLOAT, false, 0, buffers[l]);
            GLES32.glEnableVertexAttribArray(mPositionHandle);
            GLES32.glDrawArrays(GLES32.GL_POINTS, 0, POINTS);
            GLES32.glDrawArrays(GLES32.GL_LINE_STRIP, 0, POINTS);
        }
    }

    @Override
    public void onSurfaceChanged(javax.microedition.khronos.opengles.GL10 gl, int w, int h) {
        GLES32.glViewport(0, 0, w, h);
    }
}
